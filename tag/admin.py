from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Custom admin panel setting for the Tag modell, allows for easy
    management of tags. Apart from the default settings, this class also
     - Allows filtering tags by creation/update date.
     - Enables a date-based filtering.
     - Ensures consistent ordering
     - Prevents accidental edits to timestamps.    
    """
    list_display = ('tag_id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
# Register your models here.
