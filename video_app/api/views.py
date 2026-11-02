"""video list, video detail and thumbnail image API views."""

from rest_framework.views import APIView
from rest_framework import generics
from django.http import FileResponse

from video_app.models import Video
from .serializers import VideoListSerializer, VideoDetailtSerializer, ThumbnailImageSerializer


class VideoListView(generics.ListAPIView):
    """Provides an API endpoint for video list."""

    queryset = Video.objects.filter(is_ready=True)
    serializer_class = VideoListSerializer


class VideoDetailtView(APIView):
    """Provides an API endpoint for video detail."""

    def get(self, request, movie_id, resolution, segment):
        """returns the video"""
        serializer = VideoDetailtSerializer(data={"movie_id": movie_id, "resolution": resolution, "segment": segment})
        serializer.is_valid(raise_exception=True)
        movie_url = str(serializer.validated_data)

        if movie_url.endswith(".m3u8"):
            content_type = "application/vnd.apple.mpegurl"
        else:
            content_type = "video/mp2t"

        response = FileResponse(
            open(movie_url, "rb"),
            content_type=content_type,
        )
        response["Cache-Control"] = "private, no-store"
        return response

class ThumbnailImageView(APIView):
    """Provides an API endpoint for thumbnail image."""

    def get(self, reguest, movie_id, thumbnail):
        """returns thumbnail image"""
        serializer = ThumbnailImageSerializer(data={"movie_id": movie_id, "thumbnail": thumbnail})
        serializer.is_valid(raise_exception=True)
        thumbnail_image_path = str(serializer.validated_data)

        return FileResponse(open(thumbnail_image_path, "rb"))