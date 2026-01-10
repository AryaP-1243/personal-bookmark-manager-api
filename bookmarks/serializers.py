from rest_framework import serializers
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark model.
    
    Handles serialization and validation of bookmark data.
    The user field is read-only and automatically set to the authenticated user.
    """
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Bookmark
        fields = ['id', 'url', 'title', 'description', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']
    
    def validate_url(self, value):
        """Validate that the URL is properly formatted."""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "URL must start with http:// or https://"
            )
        return value
    
    def validate_title(self, value):
        """Validate that title is not empty or just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty"
            )
        return value.strip()
