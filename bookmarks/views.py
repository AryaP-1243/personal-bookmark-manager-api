from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bookmark
from .serializers import BookmarkSerializer
from .permissions import IsOwner


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user bookmarks.
    
    Provides CRUD operations for bookmarks:
    
    - GET /api/bookmarks/ - List all bookmarks for the authenticated user
    - POST /api/bookmarks/ - Create a new bookmark
    - GET /api/bookmarks/{id}/ - Retrieve a specific bookmark
    - PUT /api/bookmarks/{id}/ - Update a bookmark (full update)
    - PATCH /api/bookmarks/{id}/ - Partial update a bookmark
    - DELETE /api/bookmarks/{id}/ - Delete a bookmark
    
    All endpoints require authentication.
    Users can only access their own bookmarks.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        """
        Return bookmarks for the authenticated user only.
        
        This ensures users can only see their own bookmarks,
        even when listing all bookmarks.
        """
        return Bookmark.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set the user field to the authenticated user when creating a bookmark.
        
        This ensures the bookmark is associated with the correct user
        without requiring the user to specify it in the request.
        """
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new bookmark.
        
        Request body:
        {
            "url": "https://example.com",
            "title": "Example Website",
            "description": "Optional description"  # optional
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a bookmark.
        
        Returns a success message on deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Bookmark deleted successfully'},
            status=status.HTTP_200_OK
        )
