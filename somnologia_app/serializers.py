# somnologia_app/serializers.py

from rest_framework import serializers
from .models import Person, Dream, Tag # <--- Import Tag model

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

# New TagSerializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__' # Includes 'id', 'name', 'description'


class DreamSerializer(serializers.ModelSerializer):
    persons = PersonSerializer(many=True, read_only=True)
    # Change 'tags' to use TagSerializer for read operations (displaying full tag objects)
    tags = TagSerializer(many=True, read_only=True) # <--- IMPORTANT CHANGE

    class Meta:
        model = Dream
        fields = '__all__'
        extra_kwargs = {
            'dream_date': {'required': False},
        }
        read_only_fields = ['ai_interpretation', 'generated_image_url', 'entry_created_at']