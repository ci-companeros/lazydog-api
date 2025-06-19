from django.contrib import admin
from .models import ResourceItem

"""
Admin configuration for the Rating model.

Enables searching, filtering, and display of ratings in the Django admin panel.
Automatically keeps resource average ratings and rating counts in sync via signals,
so administrators always see up-to-date rating statistics.
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
