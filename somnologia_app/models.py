from django.db import models
from datetime import date

class Person(models.Model):

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='person_photos/',blank=True, null=True)

    def __str__(self):
        return self.name

class Dream(models.Model):

    # Possible types of dreams.
    TAG_CHOICES = (
        ('R', 'Realistic'),
        ('N', 'Nightmare'),
        ('L', 'Lucid'),
        ('F', 'Fantasy'),
    )

    tags = models.CharField(max_length=255, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    description = models.TextField()

    # Use DateField for date only.
    # The default value (e.g. "yesterday") will be set in the API view.
    dream_date = models.DateField()

    # An optional field to store the AI interpretation result.
    ai_interpretation = models.TextField(blank=True, null=True)

    # An optional field to store the URL of the generated image.
    generated_image_url = models.URLField(max_length=500, blank=True, null=True)

    # Automatically capture when the dream entry was *created* in the database
    entry_created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        # Optional: Order dreams by date by default, newest first
        ordering = ['-dream_date', '-entry_created_at'] 

    def __str__(self):
        # A more informative string representation
        return f"Dream on {self.dream_date} ({self.description[:50]}...)" if len(self.description) > 50 else f"Dream on {self.dream_date} ({self.description})"

    # Helper methods for tags (useful for internal logic or manual parsing)
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()] if self.tags else []

    def set_tags_list(self, list_of_tags):
        # Ensures there are no duplicate tags and handles empty lists gracefully
        cleaned_tags = set([str(tag).strip() for tag in list_of_tags if str(tag).strip()])
        cleaned_tags = sorted(list(cleaned_tags))
        self.tags = ','.join(cleaned_tags)

    # Override save method if you want to ensure tag list is always stored correctly
    def save(self, *args, **kwargs):
        # Ensure tags are stored as a comma-separated string from a list if it's passed as such
        if isinstance(self.tags, list):
            self.set_tags_list(self.tags)
        super().save(*args, **kwargs)
