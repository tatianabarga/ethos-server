from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")

    def test_create_user(self):
        url = '/users'
        data = {
            "name": "New User",
            "uid": "67890"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=response.data['id']).name, "New User")
        
    def test_retrieve_user(self):
        url = f'/users/{self.user.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user.name)

    def test_list_users(self):
        url = '/users'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_update_user(self):
        url = f'/users/{self.user.id}'
        data = {
            "name": "Updated User"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.name, "Updated User")

