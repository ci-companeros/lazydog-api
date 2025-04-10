from django.contrib import admin
from .models import ResourceItem


@admin.register(ResourceItem)
class ResourceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created_at')
    search_fields = ('title', 'description', 'url')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('category',)
