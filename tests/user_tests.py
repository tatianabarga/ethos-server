from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User
from django.urls import reverse

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
