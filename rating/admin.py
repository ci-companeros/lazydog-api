from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource_item', 'score', 'created_at')
    search_fields = ('user__username', 'resource_item__title')
    list_filter = ('score', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
