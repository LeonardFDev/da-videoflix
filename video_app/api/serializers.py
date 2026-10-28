from rest_framework import serializers
from rest_framework.exceptions import NotFound
from pathlib import Path

from video_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for the video model."""

    class Meta:
        model = Video
        fields = ["id", "created_at", "title", "description", "thumbnail_url", "category"]


class VideoDetailtSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    resolution = serializers.CharField()
    segment = serializers.CharField()

    def validate(self, attrs):
        movie_id = attrs["movie_id"]
        resolution = attrs["resolution"]
        segment = attrs["segment"]

        try:
            video = Video.objects.get(id=movie_id, is_ready=True)
        except Exception:
            raise NotFound()

        video_id_dir = Path(video.video_file.path).parent
        if not video_id_dir.is_dir():
            raise NotFound()

        video_resolution_dir = Path(video_id_dir) / resolution
        if not video_resolution_dir.is_dir():
            raise NotFound()

        video_segment = Path(video_resolution_dir) / segment
        if not video_segment.exists():
            raise NotFound()

        if not str(video_segment).endswith((".m3u8", ".ts")):
            raise serializers.ValidationError()
        
        return video_segment


class ThumbnailImageSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    thumbnail = serializers.CharField()

    def validate(self, attrs):
        movie_id = attrs["movie_id"]
        thumbnail = attrs["thumbnail"]

        try:
            video = Video.objects.get(id=movie_id, is_ready=True)
        except Exception:
            raise NotFound()

        video_id_dir = Path(video.video_file.path).parent
        if not video_id_dir.is_dir():
            raise NotFound()

        video_thumbnail = Path(video_id_dir) / thumbnail
        if not video_thumbnail.exists():
            raise NotFound()

        if not str(video_thumbnail).endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise serializers.ValidationError()
        
        return video_thumbnail