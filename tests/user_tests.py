from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ethosapi.models import User, Circle, CircleUser

class UserViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='Test User', uid='12345')
        self.circle = Circle.objects.create(name='Test Circle', creator=self.user)

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user.name)

    def test_retrieve_user_not_found(self):
        url = reverse('user-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'user not found')

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one user created in setUp

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'name': 'New User',
            'uid': '67890'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New User')
        self.assertEqual(User.objects.count(), 2)  # One from setUp, one from this test

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        data = {
            'name': 'Updated User'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated User')

    def test_destroy_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_add_circle_to_user(self):
        url = reverse('user-add-circle', args=[self.user.pk, self.circle.pk])
        response = self.client.patch(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(CircleUser.objects.filter(user=self.user, circle=self.circle).exists())

    def test_remove_circle_from_user(self):
        CircleUser.objects.create(user=self.user, circle=self.circle)
        url = reverse('user-remove-circle', args=[self.user.pk, self.circle.pk])
        response = self.client.patch(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CircleUser.objects.filter(user=self.user, circle=self.circle).exists())
