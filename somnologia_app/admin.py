from django.contrib import admin
from .models import Person, Dream, Tag

admin.site.register(Person)
admin.site.register(Dream)
admin.site.register(Tag)