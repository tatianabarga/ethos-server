from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ethosapi.models import User, Profile, Log
from datetime import date

class LogViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio="Test Bio")
        self.log = Log.objects.create(
            title="Test Log",
            description="Test Description",
            score_impact=10,
            event_date="2024-01-01",
            creator=self.user,
            profile=self.profile,
            log_date=date.today()
        )

    def test_retrieve_log(self):
        url = reverse('log-detail', args=[self.log.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.log.title)

    def test_retrieve_log_not_found(self):
        url = reverse('log-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'log not found')

    def test_list_logs(self):
        url = reverse('log-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one log created in setUp

    def test_list_logs_with_profile_filter(self):
        url = f"{reverse('log-list')}?profile={self.profile.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_log(self):
        url = reverse('log-list')
        data = {
            'title': 'New Log',
            'description': 'New Description',
            'score_impact': 15,
            'event_date': '2024-02-01',
            'creator': self.user.pk,
            'profile': self.profile.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Log')
        self.assertEqual(Log.objects.count(), 2)  # One from setUp, one from this test

    def test_create_log_invalid(self):
        url = reverse('log-list')
        data = {
            'title': '',
            'description': 'New Description',
            'score_impact': 15,
            'event_date': '2024-02-01',
            'creator': self.user.pk,
            'profile': self.profile.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_log(self):
        url = reverse('log-detail', args=[self.log.pk])
        data = {
            'title': 'Updated Log',
            'description': 'Updated Description',
            'score_impact': 20,
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.log.refresh_from_db()
        self.assertEqual(self.log.title, 'Updated Log')
        self.assertEqual(self.log.score_impact, 20)

    def test_update_log_not_found(self):
        url = reverse('log-detail', args=[999])
        data = {
            'title': 'Non-existent Log',
            'description': 'Does not exist',
            'score_impact': 0,
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

