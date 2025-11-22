# In destinations/admin.py
from django.contrib import admin
from .models import Destination, DestinationImage
from django.utils.html import format_html

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 5 
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'caption']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    inlines = [DestinationImageInline]
    list_display = ['place_name', 'state', 'district', 'weather', 'created_at']
    list_filter = ['state', 'weather', 'created_at']
    search_fields = ['place_name', 'state', 'district', 'description']
    prepopulated_fields = {'slug': ('place_name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['place_name', 'slug', 'description']
        }),
        ('Location', {
            'fields': ['state', 'district']
        }),
        ('Details', {
            'fields': ['weather', 'google_map_link']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'destination', 'created_at']
    list_filter = ['created_at']
    search_fields = ['destination__place_name', 'caption']
    readonly_fields = ['created_at', 'image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'