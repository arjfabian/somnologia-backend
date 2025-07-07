from datetime import date, timedelta
from django.db.models import Count

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person, Dream, Tag
from .serializers import PersonSerializer, DreamSerializer, TagSerializer
from .plugins.interpreters.artemidorus import artemidorus_interpreter

# -----------------------------------------------------
# API ViewSets for CRUD Operations
# -----------------------------------------------------

class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Person objects.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class DreamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Dream objects.
    Includes custom logic for handling Many-to-Many relationships with Persons and Tags,
    and setting a default dream_date if not provided.
    """
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer

    def _parse_ids(self, ids_data):
        """
        Helper method to parse IDs from request data, handling string or list formats.
        Returns a list of integers, or None if the input was None (allowing for explicit clearing/no change).
        """
        if ids_data is None:
            return None # Allows explicit None to mean "no change to this M2M field"
        if isinstance(ids_data, str):
            # Split by comma, strip whitespace, filter out empty strings, and convert to int
            return [int(item.strip()) for item in ids_data.split(',') if item.strip().isdigit()]
        elif isinstance(ids_data, (list, tuple)):
            # Ensure all items in the list/tuple are integers, filter out non-integers
            return [int(item) for item in ids_data if isinstance(item, (int, str)) and str(item).strip().isdigit()]
        return [] # Default to empty list if format is unexpected but not None


    def perform_create(self, serializer):
        """
        Custom creation logic for Dream instances.
        - Sets a default `dream_date` if not provided in the request.
        - Handles Many-to-Many relationships for `persons` and `tags` using the `_parse_ids` helper.
        """
        # Get data, defaulting to empty list if not present, to ensure _parse_ids handles it
        person_ids_raw = self.request.data.get('persons', [])
        tag_ids_raw = self.request.data.get('tags', [])

        # Set default dream_date if it's not provided or is empty
        if not serializer.validated_data.get('dream_date'):
            serializer.validated_data['dream_date'] = date.today() - timedelta(days=1)

        dream = serializer.save() # Save the dream instance first to get an ID for M2M relationships

        # Parse and set Persons Many-to-Many
        parsed_person_ids = self._parse_ids(person_ids_raw)
        if parsed_person_ids is not None: # Check if data for persons was explicitly provided (e.g., an empty list [])
            persons_to_add = Person.objects.filter(id__in=parsed_person_ids)
            dream.persons.set(persons_to_add)

        # Parse and set Tags Many-to-Many
        parsed_tag_ids = self._parse_ids(tag_ids_raw)
        if parsed_tag_ids is not None: # Check if data for tags was explicitly provided
            tags_to_add = Tag.objects.filter(id__in=parsed_tag_ids)
            dream.tags.set(tags_to_add)


    def perform_update(self, serializer):
        """
        Custom update logic for Dream instances.
        - Handles Many-to-Many relationships for `persons` and `tags` using the `_parse_ids` helper.
        - Allows explicit clearing of M2M relationships by sending an empty list,
          or leaving them unchanged by sending `null` or omitting the field.
        """
        # Use None as default for get() to distinguish between field not present vs. empty list
        person_ids_raw = self.request.data.get('persons', None)
        tag_ids_raw = self.request.data.get('tags', None)

        dream = serializer.save() # Save the dream instance first

        # Parse and set Persons Many-to-Many
        parsed_person_ids = self._parse_ids(person_ids_raw)
        if parsed_person_ids is not None: # Only update if the field was explicitly provided in the request
            persons_to_set = Person.objects.filter(id__in=parsed_person_ids)
            dream.persons.set(persons_to_set)

        # Parse and set Tags Many-to-Many
        parsed_tag_ids = self._parse_ids(tag_ids_raw)
        if parsed_tag_ids is not None: # Only update if the field was explicitly provided in the request
            tags_to_set = Tag.objects.filter(id__in=parsed_tag_ids)
            dream.tags.set(tags_to_set)

# -----------------------------------------------------
# Custom API Endpoints (Function-Based Views)
# -----------------------------------------------------

@api_view(['GET'])
def dashboard_data_api(request):
    """
    API endpoint for aggregated dashboard data:
    - Latest 3 dream entries.
    - List of persons with their dream counts.
    - Chart data for persons and their dream counts.
    """
    # Get latest 3 dream entries (by entry_created_at to reflect recent additions)
    latest_dreams = Dream.objects.all().order_by('-entry_created_at')[:3]
    latest_dreams_serializer = DreamSerializer(latest_dreams, many=True)

    # Get persons with their dream counts, efficiently using annotation
    persons_with_count = Person.objects.annotate(qty_dreams=Count('dream')).order_by('name')

    persons_data = []
    for person in persons_with_count:
        persons_data.append({
            'id': person.id,
            'name': person.name,
            'photo': request.build_absolute_uri(person.photo.url) if person.photo else None,
            'qty_dreams': person.qty_dreams
        })

    # Prepare data for potential charts (names and counts separately)
    chart_labels = [person.name for person in persons_with_count]
    chart_data = [person.qty_dreams for person in persons_with_count]

    return Response({
        'latest_dreams': latest_dreams_serializer.data,
        'persons_summary': persons_data,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def interpret_dream_api(request):
    """
    API endpoint to send a dream description for AI interpretation and
    to suggest persons, tags, and a generated image based on the content.
    Accepts a POST request with 'description' in the body.
    Returns interpretation, suggested persons (full objects),
    suggested new person names, suggested tags (full objects),
    and a generated image URL (from AI, or placeholder).
    """
    dream_description = request.data.get('description', '')

    if not dream_description:
        return Response(
            {'error': 'Dream description is required for interpretation.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Call the instantiated interpreter for analysis
    analysis_results = artemidorus_interpreter.analyze_dream_description(dream_description)

    # Fetch and serialize full Person and Tag objects based on suggested IDs
    suggested_persons_qs = Person.objects.filter(id__in=analysis_results['suggested_person_ids'])
    suggested_persons_data = PersonSerializer(suggested_persons_qs, many=True).data

    suggested_tags_qs = Tag.objects.filter(id__in=analysis_results['suggested_tag_ids'])
    suggested_tags_data = TagSerializer(suggested_tags_qs, many=True).data

    # Call the interpreter for image generation, passing both description and interpretation
    generated_image_url = artemidorus_interpreter.generate_dream_image(
        dream_description=dream_description,
        interpretation=analysis_results['interpretation']
    )

    return Response(
        {
            'interpretation': analysis_results['interpretation'],
            'suggested_persons': suggested_persons_data,
            'suggested_new_person_names': analysis_results['suggested_new_person_names'],
            'suggested_tags': suggested_tags_data,
            'generated_image_url': generated_image_url
        },
        status=status.HTTP_200_OK
    )
