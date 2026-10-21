from rest_framework import serializers
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
            video = Video.objects.get(id=movie_id)
        except Exception:
            raise serializers.ValidationError()

        video_id_dir = Path(video.video_file.path).parent / str(video.id)
        if not video_id_dir.is_dir():
            raise serializers.ValidationError()

        video_resolution_dir = Path(video_id_dir) / resolution
        if not video_resolution_dir.is_dir():
            raise serializers.ValidationError()

        video_segment = Path(video_resolution_dir) / segment
        if not video_segment.exists():
            raise serializers.ValidationError()

        if not str(video_segment).endswith((".m3u8", ".ts")):
            raise serializers.ValidationError()
        
        return video_segment