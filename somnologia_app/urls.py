"""
API URL routing for the Somnologia application.

This file defines the URL patterns that map incoming HTTP requests to the
appropriate views within the somnologia_app. It utilizes Django REST Framework's
DefaultRouter for ViewSet-based APIs and standard `path` for function-based views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router instance for automatic URL generation for ViewSets.
router = DefaultRouter()

# Register our ViewSets with the router.
# This automatically generates a set of URLs for list, create, retrieve, update,
# and delete operations for the registered models.
# For example, PersonViewSet will generate:
# - /api/v1/persons/ (list and create)
# - /api/v1/persons/{id}/ (retrieve, update, and delete)
router.register(r'persons', views.PersonViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'dreams', views.DreamViewSet)

# Define the URL patterns for the Somnologia API.
urlpatterns = [
    # Include the router-generated URLs under the 'api/v1/' prefix for this app.
    # This consolidates all ViewSet-based API endpoints under a common base path.
    path('api/v1/', include(router.urls)),

    # Custom API endpoints (function-based views not automatically handled by ModelViewSet).
    # These paths are explicitly defined for specific functionalities.
    path('api/v1/dashboard/', views.dashboard_data_api, name='dashboard_api'),
    path('api/v1/interpret/', views.interpret_dream_api, name='interpret_dream_api'),
]