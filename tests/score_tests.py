from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ethosapi.models import Score, Profile, User

class ScoreViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(creator=self.user, bio="Test Bio", name="Test Name")
        self.score = Score.objects.create(profile=self.profile, score=100)

    def test_retrieve_score(self):
        url = reverse('score-detail', args=[self.score.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], self.score.score)

    def test_retrieve_score_not_found(self):
        url = reverse('score-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'score not found')

    def test_list_scores(self):
        url = reverse('score-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one score created in setUp

    def test_list_scores_with_profile_filter(self):
        url = f"{reverse('score-list')}?profile={self.profile.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_score(self):
        url = reverse('score-list')
        data = {
            'score': 50,
            'profile': self.profile.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 50)
        self.assertEqual(Score.objects.count(), 2)  # One from setUp, one from this test

    def test_update_score(self):
        url = reverse('score-detail', args=[self.score.pk])
        data = {
            'score': 200
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.score.refresh_from_db()
        self.assertEqual(self.score.score, 200)

    def test_destroy_score(self):
        url = reverse('score-detail', args=[self.score.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Score.objects.count(), 0)
