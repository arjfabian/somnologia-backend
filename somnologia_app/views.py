from datetime import date, timedelta
from django.db.models import Count # For aggregation in dashboard

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person, Dream
from .serializers import PersonSerializer, DreamSerializer

# -----------------------------------------------------
# API ViewSets for CRUD Operations
# -----------------------------------------------------

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows persons to be viewed or edited.
    Provides CRUD for the Person model.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # You might add permissions here later, e.g.,
    # permission_classes = [IsAuthenticated]


class DreamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dreams to be viewed or edited.
    Provides CRUD for the Dream model.
    """
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom create logic for Dream model.
        Handles setting dream_date to yesterday if not provided.
        Handles associating persons by IDs.
        """
        # Get list of person IDs from request data, if provided
        person_ids = self.request.data.get('persons', []) # Frontend might send a list of IDs

        # Set dream_date to yesterday if not provided in the request
        if 'dream_date' not in self.request.data or not self.request.data['dream_date']:
            serializer.validated_data['dream_date'] = date.today() - timedelta(days=1)

        # Save the dream instance first, so we can add M2M relations
        dream = serializer.save()

        # Handle persons Many-to-Many relationship (if person_ids is a list of IDs)
        # This part needs adjustment based on how your frontend will send persons data.
        # Common patterns: sending a list of IDs, or nested objects (more complex for write).
        # For now, let's assume 'persons' in request.data is a list of person IDs.
        if person_ids:
            # Ensure person_ids is iterable (e.g., list)
            if isinstance(person_ids, str): # Handle comma-separated string if that's the input
                person_ids = [int(p_id.strip()) for p_id in person_ids.split(',') if p_id.strip().isdigit()]
            elif not isinstance(person_ids, list): # Ensure it's a list if not already
                 person_ids = [person_ids] # Wrap single ID in a list

            # Filter for existing Person objects
            persons_to_add = Person.objects.filter(id__in=person_ids)
            dream.persons.set(persons_to_add) # .set() replaces existing ManyToMany relations

        dream.save() # Save again after adding persons (though .set() usually saves M2M immediately)

    def perform_update(self, serializer):
        """
        Custom update logic for Dream model.
        Handles updating persons by IDs.
        """
        # Get list of person IDs from request data, if provided for update
        person_ids = self.request.data.get('persons', None) # Use None to distinguish if key is present but empty

        # Update the dream instance
        dream = serializer.save()

        # Only update persons if the 'persons' key was explicitly sent in the request
        if person_ids is not None:
            if isinstance(person_ids, str):
                person_ids = [int(p_id.strip()) for p_id in person_ids.split(',') if p_id.strip().isdigit()]
            elif not isinstance(person_ids, list):
                 person_ids = [person_ids]

            persons_to_set = Person.objects.filter(id__in=person_ids)
            dream.persons.set(persons_to_set) # .set() replaces existing ManyToMany relations

        dream.save() # Save again after updating persons


# -----------------------------------------------------
# Custom API Endpoints (Function-Based Views)
# -----------------------------------------------------

@api_view(['GET'])
def dashboard_data_api(request):
    """
    API endpoint for aggregated dashboard data:
    - Latest 3 dream entries.
    - List of persons with their dream counts.
    """
    # Get latest 3 dream entries (by entry_created_at to reflect recent additions)
    latest_dreams = Dream.objects.all().order_by('-entry_created_at')[:3]
    latest_dreams_serializer = DreamSerializer(latest_dreams, many=True)

    # Get persons with their dream counts
    # annotate(qty_dreams=Count('dream')) adds a 'qty_dreams' attribute to each Person object
    persons_with_count = Person.objects.annotate(qty_dreams=Count('dream')).order_by('name')

    # Serialize persons. We'll add 'qty_dreams' to PersonSerializer fields temporarily for this.
    # Or, we can manually construct the response if PersonSerializer shouldn't always have qty_dreams.
    # For simplicity, let's create a custom list for the response:
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
    API endpoint to send a dream description for AI interpretation.
    Accepts a POST request with 'description' in the body.
    Returns the AI-generated interpretation.
    """
    dream_description = request.data.get('description')

    if not dream_description:
        return Response(
            {'error': 'Dream description is required for interpretation.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: Integrate your actual AI model here for interpretation.
    # This is currently a placeholder.
    # Example:
    # ai_model_response = your_ai_model.interpret(dream_description)
    # interpretation_text = ai_model_response.get('interpretation_text', 'No interpretation available.')

    # Placeholder interpretation
    interpretation_text = f"AI Interpretation for '{dream_description[:100]}...': This dream suggests deep subconscious processing related to [themes like freedom, anxiety, transformation, etc.]."

    # Optional: You might want to save this interpretation back to a Dream model if the dream exists
    # dream_id = request.data.get('dream_id')
    # if dream_id:
    #     try:
    #         dream = Dream.objects.get(id=dream_id)
    #         dream.ai_interpretation = interpretation_text
    #         dream.save()
    #     except Dream.DoesNotExist:
    #         pass # Or return an error if dream_id is mandatory

    return Response(
        {'interpretation': interpretation_text},
        status=status.HTTP_200_OK
    )

# -----------------------------------------------------
# Helper for media file serving in development (NOT for production)
# -----------------------------------------------------
from django.conf import settings
from django.conf.urls.static import static

# This is not a view but a helper for main urls.py (we'll move it there)
# It ensures media files are served in development mode.
# In production, a web server like Nginx/Apache handles this.
# For now, just note it's related to serving 'photo' fields.