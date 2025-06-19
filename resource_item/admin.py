from django.contrib import admin
from .models import ResourceItem

"""
Admin configuration for the ResourceItem model.

Displays key information about resources, including average rating and rating count.
Ensures administrators can easily search, filter, and review resource statistics
directly in the Django admin panel.
"""


@admin.register(ResourceItem)
class ResourceItemAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'user', 'average_rating', 'rating_count', 'created_at'
    )
    readonly_fields = ('average_rating', 'rating_count')
    search_fields = ('title', 'user__username')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
