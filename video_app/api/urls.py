from django.urls import path

from .views import VideoListView, VideoDetailtView, VideoWithSegmentDetailtView


urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoDetailtView.as_view(), name='video-detail'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoWithSegmentDetailtView.as_view(), name='video-with-segment-detail'),
]