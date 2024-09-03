from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Circle, CircleProfile, Profile, CircleUser

class CircleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
        self.circle = Circle.objects.create(creator=self.user, name="Test Circle")
