"""Tests for the confirm Password API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator 

from tests.helpers import status_code_with_message


class PasswordConfirmTests(APITestCase):
    def customized_setUp(self):
        self.user = User.objects.create_user(username="testuserTest", email="testuser@test.de", password="123456")
        
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(self.user)

    def test_password_confirm_get_405(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_confirm_patch_405(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_confirm_put_405(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_password_confirm_delete_405(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_password_confirm_invalid_link_post_400(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": 999, "token": self.token})
        data = {"new_password": "123456", "confirm_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_confirm_invalid_or_expired_token_post_400(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": 123456})
        data = {"new_password": "123456", "confirm_password": "123456"}
        response = self.client.post(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_confirm_passwords_not_match_post_400(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        data = {"new_password": "123456", "confirm_password": "654321"}
        response = self.client.post(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_confirm_fields_are_required_post_400(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        data = {}
        response = self.client.post(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_confirm_post_200(self):
        self.customized_setUp()
        url = reverse("password_confirm", kwargs={"uidb64": self.uidb64, "token": self.token})
        data = {"new_password": "123456", "confirm_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
