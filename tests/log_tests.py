from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Profile, Log
from django.urls import reverse
from datetime import date

class LogTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
        self.profile = Profile.objects.create(creator=self.user, bio="Test Bio", name="Test Name")
        self.log = Log.objects.create(
            creator=self.user,
            profile=self.profile,
            title="Test Title",
            description="Test Description",
            event_date=date.today()
        )
