# somnologia_app/serializers.py

from rest_framework import serializers
from .models import Person, Dream

class PersonSerializer(serializers.ModelSerializer):
    # We can optionally include a custom field here if needed,
    # but for now, '__all__' will suffice for basic Person fields.
    class Meta:
        model = Person
        fields = '__all__' # Includes 'id', 'name', 'photo'


class DreamSerializer(serializers.ModelSerializer):
    # By default, ManyToManyField (like 'persons') would show a list of IDs.
    # To show full Person objects when retrieving a Dream, we can nest the serializer.
    # 'read_only=True' means this field is not expected in POST/PUT requests;
    # we'll handle adding persons to a dream separately in the view or by ID.
    persons = PersonSerializer(many=True, read_only=True)

    # We might want to allow setting persons by their IDs in write operations
    # A separate field for write operations or a custom create/update method might be needed
    # For simplicity initially, let's just make 'persons' read-only in the main serializer
    # and handle the many-to-many relationship in the view's create/update logic.

    class Meta:
        model = Dream
        # Include all fields from the Dream model.
        # 'id' is automatically added by ModelSerializer
        fields = '__all__'
        
        # Add 'dream_date' to extra_kwargs to make it not required for input
        extra_kwargs = {
            'dream_date': {'required': False},
        }

        # Make ai_interpretation and generated_image_url read-only as they are set by the backend
        read_only_fields = ['ai_interpretation', 'generated_image_url', 'entry_created_at']