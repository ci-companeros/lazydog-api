from django.contrib import admin
from .models import Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """
    Admin interface customization for the Bookmark model.

    This class defines the display and interaction options for bookmarks
    in the Django admin interface, including list display fields, filters,
    search capabilities, date hierarchy, and default ordering.
    """
    list_display = ('user', 'resource', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'resource__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)