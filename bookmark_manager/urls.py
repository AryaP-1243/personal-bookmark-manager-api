"""
URL configuration for bookmark_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint with available endpoints info."""
    return Response({
        'message': 'Welcome to the Bookmark Manager API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'google_login': '/api/auth/google/',
                'user': '/api/auth/user/',
                'logout': '/api/auth/logout/',
            },
            'bookmarks': {
                'list_create': '/api/bookmarks/',
                'detail': '/api/bookmarks/{id}/',
            },
        },
        'documentation': '/api/docs/',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API root
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-alt'),
    
    # Authentication endpoints
    path('api/auth/', include('accounts.urls')),
    
    # Bookmark endpoints
    path('api/bookmarks/', include('bookmarks.urls')),
    
    # Allauth URLs (for web-based OAuth flow)
    path('accounts/', include('allauth.urls')),
]
