from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Admin configuration for Bookmark model."""
    list_display = ['title', 'url', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'url', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
