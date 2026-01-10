from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bookmark(models.Model):
    """
    Bookmark model for storing user's saved URLs.
    
    Fields:
        - user: Foreign key to the User model (owner of the bookmark)
        - url: The bookmarked URL (required)
        - title: Title/name for the bookmark (required)
        - description: Optional description of the bookmark
        - created_at: Timestamp when the bookmark was created
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        help_text='Owner of this bookmark'
    )
    url = models.URLField(
        max_length=2048,
        help_text='The URL to bookmark'
    )
    title = models.CharField(
        max_length=255,
        help_text='Title for the bookmark'
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Optional description of the bookmark'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the bookmark was created'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
