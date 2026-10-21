from django.contrib import admin

from video_app.models import Video

@admin.register(Video)
class OfferAdmin(admin.ModelAdmin):
    """Admin configuration for the video model."""

    list_display = ("id", "title", "category")
    fields = ("title", "description", "category" "video_file")
    ordering = ["id"]
    search_fields = ("title", "description")
