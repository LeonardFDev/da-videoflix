"""Tests for the activate API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator 

from tests.helpers import status_code_with_message


class ActivateTests(APITestCase):
    def customized_setUp(self):
        self.user = User.objects.create_user(username="testuserTest", email="testuser@test.de", password="123456", is_active=False)
        
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(self.user)

    def test_activate_post_405(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.post(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_activate_patch_405(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_activate_put_405(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_activate_delete_405(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_activate_invalid_link_get_400(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": 999, "token": self.token})
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_invalid_or_expired_token_get_400(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": 123456})
        response = self.client.get(url)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_user_is_already_activated_get_400(self):
        self.customized_setUp()
        self.user.is_active = True
        self.user.save()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_get_200(self):
        self.customized_setUp()
        url = reverse("activate", kwargs={"uidb64": self.uidb64, "token": self.token})
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)