"""
Serializers for the Somnologia application's API.

These serializers define how Python objects (models) are converted to and from
JSON representations for API requests and responses, facilitating data exchange
between the Django backend and frontend clients.
"""

from rest_framework import serializers
from .models import Person, Dream, Tag

class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Person` model.
    Converts `Person` model instances to JSON and vice-versa, exposing all fields.
    """
    class Meta:
        model = Person
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Tag` model.
    Converts `Tag` model instances to JSON and vice-versa, exposing all fields.
    """
    class Meta:
        model = Tag
        fields = '__all__' # Includes 'id', 'name', 'description'


class DreamSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Dream` model.

    Handles nested serialization for 'persons' and 'tags' Many-to-Many relationships,
    making them read-only for input as they are managed manually in the view's
    `perform_create` and `perform_update` methods.

    Includes `extra_kwargs` for optional fields and `read_only_fields` for
    system-generated or AI-populated data.
    """
    persons = PersonSerializer(many=True, read_only=True)
    # The 'tags' field uses TagSerializer for read operations, displaying full Tag objects.
    # It's set to read_only=True because the M2M relationship is handled in the view logic.
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Dream
        fields = '__all__'
        extra_kwargs = {
            'dream_date': {'required': False}, # Allows dream_date to be optional on input
        }
        # Fields that are set automatically by the system or AI and should not be settable by client input.
        read_only_fields = ['ai_interpretation', 'generated_image_url', 'entry_created_at']