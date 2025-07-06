from django.db import models
from datetime import date

class Person(models.Model):

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='person_photos/',blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name'] # Keep tags sorted by name

    def __str__(self):
        return self.name

class Dream(models.Model):
    # Removed TAG_CHOICES since tags will now come from the Tag model

    # Changed from CharField to ManyToManyField
    tags = models.ManyToManyField(Tag, blank=True)
    persons = models.ManyToManyField(Person, blank=True)
    description = models.TextField()

    dream_date = models.DateField()
    ai_interpretation = models.TextField(blank=True, null=True)
    generated_image_url = models.URLField(max_length=500, blank=True, null=True)
    entry_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dream_date', '-entry_created_at']

    def __str__(self):
        # A more informative string representation
        # Displaying tag names for the dream
        tag_names = ", ".join([tag.name for tag in self.tags.all()])
        desc_preview = self.description[:50] + "..." if len(self.description) > 50 else self.description
        return f"Dream on {self.dream_date} ({desc_preview}) Tags: [{tag_names}]"


    # The helper methods for tags (get_tags_list, set_tags_list) are no longer needed
    # as Django's ManyToManyField handles this automatically.
    # The override save method is also not needed for tags anymore.

    # If you still want to manage tags as a comma-separated string for internal logic,
    # you could add a property, but it's generally best to use the ManyToManyField directly.
    # Example (not replacing existing methods but showing how you'd get string):
    # @property
    # def tags_as_string(self):
    #    return ", ".join([tag.name for tag in self.tags.all()])


    # The save method override should be removed or adapted, as the tag string logic is gone.
    # If there's no other custom logic, you can remove the save method entirely.
    def save(self, *args, **kwargs):
        # We no longer need the tag string conversion logic here.
        super().save(*args, **kwargs)
