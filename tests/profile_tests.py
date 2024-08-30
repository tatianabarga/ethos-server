from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ethosapi.models import User, Profile, Circle, CircleProfile, Score, Log

class ProfileViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.circle = Circle.objects.create(name="Test Circle", creator=self.user)
        self.profile = Profile.objects.create(user=self.user, bio="Test Bio", name="Test Name")
        self.circle_profile = CircleProfile.objects.create(circle=self.circle, profile=self.profile)
        self.score = Score.objects.create(profile=self.profile, score=100)
        self.log = Log.objects.create(
            title="Test Log",
            description="Test Description",
            score_impact=10,
            event_date="2024-01-01",
            creator=self.user,
            profile=self.profile,
            log_date=date.today()
        )

    def test_retrieve_profile(self):
        url = reverse('profile-detail', args=[self.profile.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.profile.name)

    def test_retrieve_profile_not_found(self):
        url = reverse('profile-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'profile not found')

    def test_list_profiles(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one profile created in setUp

    def test_list_profiles_with_creator_filter(self):
        url = f"{reverse('profile-list')}?creator={self.user.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_profiles_with_circle_filter(self):
        url = f"{reverse('profile-list')}?circle={self.circle.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_profile(self):
        url = reverse('profile-list')
        data = {
            'bio': 'New Bio',
            'name': 'New Name',
            'creator': self.user.pk,
            'circles': [self.circle.pk],
            'score': 50
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Name')
        self.assertEqual(Profile.objects.count(), 2)  # One from setUp, one from this test

    def test_create_profile_with_invalid_circle(self):
        url = reverse('profile-list')
        data = {
            'bio': 'New Bio',
            'name': 'New Name',
            'creator': self.user.pk,
            'circles': [999],  # Non-existent circle ID
            'score': 50
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_profile(self):
        url = reverse('profile-detail', args=[self.profile.pk])
        data = {
            'bio': 'Updated Bio',
            'name': 'Updated Name',
            'circles': [self.circle.pk]
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated Bio')
        self.assertEqual(self.profile.name, 'Updated Name')

    def test_destroy_profile(self):
        url = reverse('profile-detail', args=[self.profile.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(CircleProfile.objects.count(), 0)
        self.assertEqual(Score.objects.count(), 0)
        self.assertEqual(Log.objects.count(), 0)
