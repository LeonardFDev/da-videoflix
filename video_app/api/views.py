from rest_framework.views import APIView
from rest_framework import generics
from django.http import FileResponse

from video_app.models import Video
from .serializers import VideoSerializer, VideoDetailtSerializer


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailtView(APIView):
    def get(self, request, movie_id, resolution, segment):
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