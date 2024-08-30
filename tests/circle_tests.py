from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ethosapi.models import User, Circle, Profile, CircleProfile, CircleUser

class CircleViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio="Test Bio")
        self.circle = Circle.objects.create(name="Test Circle", creator=self.user)

    def test_retrieve_circle(self):
        url = reverse('circle-detail', args=[self.circle.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.circle.name)

    def test_retrieve_circle_not_found(self):
        url = reverse('circle-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'circle not found')

    def test_list_circles(self):
        url = reverse('circle-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one circle created in setUp

    def test_list_circles_with_profile_filter(self):
        CircleProfile.objects.create(profile=self.profile, circle=self.circle)
        url = f"{reverse('circle-list')}?profile={self.profile.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_circles_with_user_filter(self):
        CircleUser.objects.create(user=self.user, circle=self.circle)
        url = f"{reverse('circle-list')}?user={self.user.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_circle(self):
        url = reverse('circle-list')
        data = {
            'name': 'New Circle',
            'creator': self.user.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Circle')
        self.assertEqual(Circle.objects.count(), 2)  # One from setUp, one from this test

    def test_create_circle_invalid(self):
        url = reverse('circle-list')
        data = {
            'name': '',
            'creator': self.user.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_circle(self):
        url = reverse('circle-detail', args=[self.circle.pk])
        data = {
            'name': 'Updated Circle',
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.circle.refresh_from_db()
        self.assertEqual(self.circle.name, 'Updated Circle')

    def test_destroy_circle(self):
        CircleProfile.objects.create(profile=self.profile, circle=self.circle)
        CircleUser.objects.create(user=self.user, circle=self.circle)
        url = reverse('circle-detail', args=[self.circle.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Circle.objects.count(), 0)
        self.assertEqual(CircleProfile.objects.count(), 0)
        self.assertEqual(CircleUser.objects.count(), 0)
