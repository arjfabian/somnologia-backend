# somnologia_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Import our API views from the current app

# Create a router instance
router = DefaultRouter()

# Register our ViewSets with the router
# This automatically generates URLs for list, create, retrieve, update, delete
# e.g., /api/persons/, /api/persons/{id}/
router.register(r'persons', views.PersonViewSet)
router.register(r'dreams', views.DreamViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Include the router-generated URLs under a 'api/' prefix for this app
    # This will result in paths like /api/v1/persons/, /api/v1/dreams/ etc.
    path('api/v1/', include(router.urls)), # Recommended to version your API like v1

    # Custom API endpoints (not handled by ModelViewSet)
    path('api/v1/dashboard/', views.dashboard_data_api, name='dashboard_api'),
    path('api/v1/interpret/', views.interpret_dream_api, name='interpret_dream_api'),

    # --- Optional: If you want to keep old HTML rendering views temporarily ---
    # If you still have views that render HTML (e.g., your old write, read, delete)
    # and want to keep them for testing or until the frontend is ready,
    # you would define them here without the 'api/' prefix.
    # For a pure API backend, these would typically be removed.
    # path('write/', views.write_html_view, name='write_html'),
    # path('read/', views.read_html_view, name='read_html'),
    # path('delete/', views.delete_html_view, name='delete_html'),
]