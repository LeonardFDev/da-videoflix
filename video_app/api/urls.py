from django.urls import path

from .views import VideoListView, VideoDetailtView


urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>', VideoDetailtView.as_view(), name='video-detail'),
]