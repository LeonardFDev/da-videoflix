"""Tests for the video list API."""
import time
import shutil
import uuid

from pathlib import Path
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files import File

from tests.helpers import status_code_with_message
from ..models import Video


class VideoListTests(APITestCase):
    def customized_setUp(self):
        self.user = User.objects.create_user(username="testuserTest", email="testuser@test.de", password="123456", is_active=True)
        
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)

    def create_test_file(self, is_ready = False):
        temp_dir_path = Path.cwd() / "video_app" / "tests"
        unique_number = uuid.uuid4().hex[:6]
        unique_temp_dir_path = Path (temp_dir_path) / f"temp_{unique_number}"

        with override_settings(MEDIA_ROOT=unique_temp_dir_path):
            video_url = Path(__file__).resolve().parent / "file_to_test" / "test_video.mp4"
            with open(video_url, "rb") as file:
                create_video = Video.objects.create(title=f"VideoTest_{unique_number}", video_file=File(file, name="test_video.mp4"), is_ready=is_ready)

        self.delete_after_enqueue_job(create_video, unique_temp_dir_path)

    def delete_after_enqueue_job(self, create_video, unique_temp_dir_path):
        while True:
            time.sleep(1)
            print(f"Data is processed (video id: {create_video.id} of 3)")
            path_of_thumbnail= Path(unique_temp_dir_path) / "video" /f"{create_video.id}" / "thumbnail.jpg"
            if path_of_thumbnail.exists():
                print(f"Data is ready (video id: {create_video.id} of 3)")
                shutil.rmtree(unique_temp_dir_path)
                break


    def test_video_list_post_405(self):
        self.customized_setUp()
        url = reverse("video-list")
        response = self.client.post(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_list_patch_405(self):
        self.customized_setUp()
        url = reverse("video-list")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_list_put_405(self):
        self.customized_setUp()
        url = reverse("video-list")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_video_list_delete_405(self):
        self.customized_setUp()
        url = reverse("video-list")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_list_get_401(self):
        url = reverse("video-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_list_get_200(self):
        self.customized_setUp()
        self.create_test_file()
        self.create_test_file(True)
        self.create_test_file(True)
        
        url = reverse("video-list")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)