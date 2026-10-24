"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from video_app.api.views import ThumbnailImageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("auth_app.api.urls")),
    path('api/', include("video_app.api.urls")),
    
    path('media/video/<int:movie_id>/<str:thumbnail>/', ThumbnailImageView.as_view(), name='thumbnail_image')
]
