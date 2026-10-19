from rest_framework.views import APIView
from rest_framework import generics

from video_app.models import Video
from .serializers import VideoSerializer


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailtView(APIView):
    pass


class VideoWithSegmentDetailtView(APIView):
    pass

