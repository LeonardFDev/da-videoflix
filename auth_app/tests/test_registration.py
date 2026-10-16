"""Tests for the registration API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tests.helpers import status_code_with_message


class RegistrationTests(APITestCase):
    def test_registration_get_405(self):
        url = reverse("registration")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_patch_405(self):
        url = reverse("registration")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_put_405(self):
        url = reverse("registration")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_registration_delete_405(self):
        url = reverse("registration")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_passwords_not_match_post_400(self):
        url = reverse("registration")
        data = {"email": "testuser@test.de", "password": "123456", "confirmed_password": "testpassword"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_valid_email_post_400(self):
        url = reverse("registration")
        data = {"email": "testuser.test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_double_profile_post_400(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")

        url = reverse("registration")
        data = {"email": "testuser@test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_post_201(self):
        url = reverse("registration")
        data = {"email": "testuser@test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)