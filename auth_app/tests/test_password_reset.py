"""Tests for the password reset API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tests.helpers import status_code_with_message


class PasswordResetTests(APITestCase):
    def test_password_reset_get_405(self):
        url = reverse("password_reset")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_reset_patch_405(self):
        url = reverse("password_reset")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_reset_put_405(self):
        url = reverse("password_reset")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_password_reset_delete_405(self):
        url = reverse("password_reset")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_reset_email_not_available_post_400(self):
        User.objects.create_user(email="testuser@test.de", password="123456", username="testuserTest")

        url = reverse("password_reset")
        data = {"email": "not_available@test.de"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_email_not_activated_post_400(self):
        User.objects.create_user(email="testuser@test.de", password="123456", username="testuserTest", is_active=False)

        url = reverse("password_reset")
        data = {"email": "not_available@test.de"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_post_200(self):
        User.objects.create_user(email="testuser@test.de", password="123456", username="testuserTest")

        url = reverse("password_reset")
        data = {"email": "testuser@test.de"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)