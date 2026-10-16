"""Tests for the authentication (login) API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tests.helpers import status_code_with_message


class LoginTests(APITestCase):
    def test_login_get_405(self):
        url = reverse("login")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_patch_405(self):
        url = reverse("login")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_put_405(self):
        url = reverse("login")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_login_delete_405(self):
        url = reverse("login")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_invalid_email_post_400(self):
        User.objects.create_user(email="testuser@test.de", username="testuserTest", password="123456")
        
        url = reverse("login")
        data = {"email": "unknownUsername", "password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_email_post_400(self):
        User.objects.create_user(email="testuser@test.de", username="testuserTest", password="123456")
        
        url = reverse("login")
        data = {"email": "wrong_email@test.de", "password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password_post_400(self):
        User.objects.create_user(email="testuser@test.de", username="testuserTest", password="123456")
        
        url = reverse("login")
        data = {"email": "testuser@test.de", "password": "654321"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_post_200(self):
        User.objects.create_user(email="testuser@test.de", username="testuserTest", password="123456")
    
        url = reverse("login")
        data = {"email": "testuser@test.de", "password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)