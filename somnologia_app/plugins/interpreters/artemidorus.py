# somnologia_app/plugins/interpreters/artemidorus.py

import re
from django.contrib.staticfiles.storage import staticfiles_storage
from ...models import Person, Tag
from .base import DreamInterpreter

class ArtemidorusInterpreter(DreamInterpreter):
    def analyze_dream_description(self, dream_description: str) -> dict:
        """
        Analyzes a dream description using rule-based heuristics (simulated AI).
        Implements the analyze_dream_description method from DreamInterpreter ABC.
        """
        if not dream_description:
            return {
                'interpretation': '',
                'suggested_person_ids': [],
                'suggested_new_person_names': [],
                'suggested_tag_ids': []
            }

        # --- 1. Placeholder AI Interpretation ---
        interpretation_text = (
            f"AI Interpretation for '{dream_description[:100]}...': "
            "This dream suggests deep subconscious processing related to "
            "[themes like freedom, anxiety, transformation, etc.]."
        )

        # --- 2. Person Name Extraction & Matching ---
        all_persons = Person.objects.all()
        person_names_map = {p.name.lower(): p.id for p in all_persons}
        person_ids_in_dream = []
        new_person_names = set()

        potential_names = re.findall(r'\b[A-Z][a-z]+\b', dream_description)

        for name in potential_names:
            lower_name = name.lower()
            if lower_name in person_names_map:
                person_ids_in_dream.append(person_names_map[lower_name])
            else:
                new_person_names.add(name)

        # --- 3. Tag Suggestion ---
        tag_keywords = {
            'lucid': ['lucid', 'aware', 'control', 'realize', 'wake up'],
            'nightmare': ['nightmare', 'scary', 'fear', 'monster', 'chase', 'anxiety'],
            'fantasy': ['flying', 'magic', 'mythical', 'dragon', 'unicorn', 'adventure'],
            'realistic': ['work', 'school', 'daily life', 'routine', 'normal'],
        }
        suggested_tag_ids = set()

        all_tags = Tag.objects.all()
        tag_name_to_id_map = {tag.name.lower(): tag.id for tag in all_tags}

        description_lower = dream_description.lower()

        for tag_name, keywords in tag_keywords.items():
            if tag_name in tag_name_to_id_map:
                for keyword in keywords:
                    if keyword in description_lower:
                        suggested_tag_ids.add(tag_name_to_id_map[tag_name])
                        break

        results = {
            'interpretation': interpretation_text,
            'suggested_person_ids': list(set(person_ids_in_dream)),
            'suggested_new_person_names': list(new_person_names),
            'suggested_tag_ids': list(suggested_tag_ids)
        }

        return results
    
    def generate_dream_image(self, dream_description: str, interpretation: str = None) -> str | None:
        """
        Artemidorus Interpreter does not generate actual images.
        Returns a placeholder image URL from static files for development/display purposes.
        """
        placeholder_image_url = staticfiles_storage.url('images/dream_placeholder.png')
        return placeholder_image_url
        

# Instantiate the interpreter for use.
artemidorus_interpreter = ArtemidorusInterpreter()
