"""Tests for the logout API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from tests.helpers import status_code_with_message


class LogoutTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(email="testuser@test.de", password="123456", username="testuserTest")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)

    def test_logout_get_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_logout_patch_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_logout_put_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_logout_delete_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_logout_post_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("logout")
        response = self.client.post(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_logout_about_cookies_post_200(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.post(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)