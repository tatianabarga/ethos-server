from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Profile, Log
from datetime import date

class LogTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
        self.profile = Profile.objects.create(creator=self.user, bio="Test Bio", name="Test Name")
        self.log = Log.objects.create(
            creator=self.user,
            profile=self.profile,
            score_impact="Positive",
            title="Test Title",
            description="Test Description",
            event_date=date.today()
        )
        
    def test_create_log(self):
        url = f'/logs'
        data = {
            "creator": self.user.id,
            "profile": self.profile.id,
            "score_impact": "Negative",
            "title": "New Log",
            "description": "New Description",
            "event_date": "2024-09-01"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Log.objects.count(), 2)
        self.assertEqual(Log.objects.get(id=response.data['id']).title, "New Log")
        
    def test_retrieve_log(self):
        url = f'/logs/{self.log.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.log.title)
        
    def test_list_logs(self):
        url = '/logs'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_log(self):
        url = f'/logs/{self.log.id}'
        data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "score_impact": "Neutral"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_log = Log.objects.get(id=self.log.id)
        self.assertEqual(updated_log.title, "Updated Title")
        self.assertEqual(updated_log.description, "Updated Description")
        self.assertEqual(updated_log.score_impact, "Neutral")

