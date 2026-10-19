from rest_framework import serializers

from video_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for the video model."""

    class Meta:
        model = Video
        fields = ["id", "created_at", "title", "description", "thumbnail_url", "category"]