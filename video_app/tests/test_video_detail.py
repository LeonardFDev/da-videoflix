"""Tests for the video detail API."""

import random
import shutil
import time
import uuid

from django.contrib.auth.models import User
from django.core.files import File
from django.test import override_settings
from django.urls import reverse
from pathlib import Path
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Video
from tests.helpers import status_code_with_message


class VideoDetailTests(APITestCase):
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
                created_video_object = Video.objects.create(title=f"VideoTest_{unique_number}", video_file=File(file, name="test_video.mp4"), is_ready=is_ready)

        return created_video_object, unique_temp_dir_path

    def delete_after_enqueue_job(self, created_video_object, unique_temp_dir_path):
        while True:
            time.sleep(1)
            print(f"Data is processed for deletion (video-object: {created_video_object.id})")
            path_of_thumbnail= Path(unique_temp_dir_path) / "video" /f"{created_video_object.id}" / "thumbnail.jpg"
            if path_of_thumbnail.exists():
                print(f"Data is deleted (video-object: {created_video_object.id})")
                shutil.rmtree(unique_temp_dir_path)
                break

    def test_video_detail_post_405(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.post(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_detail_patch_405(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_detail_put_405(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_video_detail_delete_405(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_video_detail_get_401(self):
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_detail_movie_id_get_404(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 999, "resolution": "720p", "segment": "segment_001.ts"})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_video_detail_resolution_get_404(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "999p", "segment": "segment_001.ts"})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_video_detail_segment_get_404(self):
        self.customized_setUp()
        url = reverse("video-detail", kwargs={"movie_id": 1, "resolution": "720p", "segment": "segment_9999.ts"})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_video_detail_get_200(self):
        self.customized_setUp()
        created_video_object, unique_temp_dir_path = self.create_test_file(True)

        video_id = created_video_object.id
        resolution_list = ["480p", "720p", "1080p"]
        resolution = random.choice(resolution_list)
        segment_list = ["segment_000.ts", "segment_001.ts", "index.m3u8"]
        segment = random.choice(segment_list)

        with override_settings(MEDIA_ROOT=unique_temp_dir_path):
            self.ensure_data_available(created_video_object, unique_temp_dir_path, video_id, resolution, segment)
            self.execute_test(created_video_object, unique_temp_dir_path, video_id, resolution, segment)

    def ensure_data_available(self, created_video_object, unique_temp_dir_path, video_id, resolution, segment):
        try:
            self.run_until_segment_file_exists(created_video_object, unique_temp_dir_path, video_id, resolution, segment)
        except KeyboardInterrupt:
            self.delete_after_enqueue_job(created_video_object, unique_temp_dir_path)

    def run_until_segment_file_exists(self, created_video_object, unique_temp_dir_path, video_id, resolution, segment):
        while True:
            time.sleep(1)
            segment_path = Path(unique_temp_dir_path) / "video" / str(video_id) / resolution / segment
            print(f"Data is processed for use (video-object: {created_video_object.id})")
        
            is_exists_segment_path = self.exists_segment_path(created_video_object, unique_temp_dir_path, video_id, segment_path)
        
            if is_exists_segment_path:
                break

    def exists_segment_path(self, created_video_object, unique_temp_dir_path, video_id, segment_path):
        if segment_path.exists():
            video_file = Path(created_video_object.video_file.path).name
            new_video_file = Path(unique_temp_dir_path) / "video" / str(video_id) / video_file
            Video.objects.filter(id=video_id).update(video_file=new_video_file)
            print(f"Data is ready (video-object: {created_video_object.id})")
            return True
        else:
            return False

    def execute_test(self, created_video_object, unique_temp_dir_path, video_id, resolution, segment):
        # with override_settings(MEDIA_ROOT=unique_temp_dir_path):
            url = reverse("video-detail", kwargs={"movie_id": str(video_id), "resolution": resolution, "segment": segment})
            response = self.client.get(url)
        
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
            self.delete_after_enqueue_job(created_video_object, unique_temp_dir_path)
        
            status_code_with_message(self, response)