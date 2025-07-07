"""
Database models for the Somnologia application.

This file defines the structure of the data for Persons, Tags, and Dreams,
including their fields, relationships, and metadata for database representation.
"""

from django.db import models
# No direct use of 'date' from datetime here, but kept if other default logic relied on it.

class Person(models.Model):
    """
    Represents a person (real individual, fictional character, or archetype)
    associated with a dream.
    """
    name = models.CharField(max_length=255, help_text="The name of the person.")
    description = models.TextField(
        blank=True,
        null=True,
        help_text="A brief description or role of the person in dreams, or notes about them."
    )
    photo = models.ImageField(
        upload_to='person_photos/',
        blank=True,
        null=True,
        help_text="Optional photo of the person."
    )
    entry_created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this person entry was created."
    )

    class Meta:
        # Default ordering: keep persons sorted by name for consistent display
        ordering = ['name']
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    Represents a descriptive tag that can be associated with dreams.
    Examples: 'Lucid', 'Nightmare', 'Recurring', 'Symbolic'.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the tag (e.g., 'Lucid', 'Nightmare')."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="An optional longer description for the tag's meaning or common usage."
    )
    entry_created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this tag entry was created."
    )

    class Meta:
        # Default ordering: keep tags sorted by name for consistent display
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

class Dream(models.Model):
    """
    Represents a single dream entry.
    Stores dream details, AI interpretation, generated image URL,
    and relationships to associated persons and tags.
    """
    description = models.TextField(help_text="The detailed description of the dream.")
    dream_date = models.DateField(
        blank=True,
        null=True, # Crucial: Allows dream_date to be optional and nullable in the database
        help_text="The date on which the dream occurred (user input, can be approximate)."
    )
    entry_created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this dream entry was created in the system."
    )

    # AI-generated fields (will be populated by the AI model)
    ai_interpretation = models.TextField(
        blank=True,
        null=True,
        help_text="AI-generated interpretation of the dream."
    )
    generated_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to an AI-generated image representing the dream."
    )

    # Relationships
    persons = models.ManyToManyField(
        Person,
        related_name='dreams', # Allows querying person.dreams.all()
        blank=True,
        help_text="Persons involved in or related to the dream."
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='dreams', # Allows querying tag.dreams.all()
        blank=True,
        help_text="Descriptive tags associated with the dream."
    )

    class Meta:
        # Default ordering: most recent dreams first
        ordering = ['-dream_date', '-entry_created_at']
        verbose_name = "Dream"
        verbose_name_plural = "Dreams"

    def __str__(self):
        date_str = self.dream_date.strftime('%Y-%m-%d') if self.dream_date else 'No Date'
        desc_preview = (self.description[:50] + "...") if len(self.description) > 50 else self.description
        tag_names = ", ".join([tag.name for tag in self.tags.all()]) if self.tags.exists() else "No Tags"
        person_names = ", ".join([person.name for person in self.persons.all()]) if self.persons.exists() else "No Persons"

        return f"Dream on {date_str} - '{desc_preview}' (Persons: {person_names} | Tags: {tag_names})"
