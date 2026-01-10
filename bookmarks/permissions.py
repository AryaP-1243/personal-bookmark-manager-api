from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a bookmark to access it.
    
    This permission ensures that:
    - Users can only view their own bookmarks
    - Users can only edit/delete their own bookmarks
    - Other users cannot access bookmarks they don't own
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the bookmark.
        """
        return obj.user == request.user
