from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Profile, Score
from django.urls import reverse

class ScoreTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
        self.profile = Profile.objects.create(creator=self.user, bio="Test Bio", name="Test Name")
        self.score = Score.objects.create(score="100", profile=self.profile)

    def test_create_score(self):
        url = f'/scores'
        data = {
            "score": "200",
            "profile": self.profile.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Score.objects.count(), 2)
        self.assertEqual(Score.objects.get(id=response.data['id']).score, "200")
        
    def test_retrieve_score(self):
        url = f'/scores/{self.score.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], self.score.score)
        
    def test_list_scores(self):
        url = f'/scores'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_score(self):
        url = f'/scores/{self.score.id}'
        data = {
            "score": "300"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Score.objects.get(id=self.score.id).score, "300")
        
    def test_delete_score(self):
        url = f'/scores/{self.score.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Score.objects.count(), 0)

