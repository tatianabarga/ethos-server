from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Circle, CircleProfile, Profile, CircleUser

class CircleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", uid="12345")
        self.circle = Circle.objects.create(creator=self.user, name="Test Circle")

    def test_create_circle(self):
        url = '/circles'
        data = {
            "creator": self.user.id,
            "name": "New Circle"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Circle.objects.count(), 2)
        self.assertEqual(Circle.objects.get(id=response.data['id']).name, "New Circle")

    def test_retrieve_circle(self):
        url = f'/circles/{self.circle.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.circle.name)

    def test_list_circles(self):
        url = '/circles'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_circle(self):
        url = f'/circles/{self.circle.id}'
        data = {
            "name": "Updated Circle"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_circle = Circle.objects.get(id=self.circle.id)
        self.assertEqual(updated_circle.name, "Updated Circle")

    def test_delete_circle(self):
        url = f'/circles/{self.circle.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Circle.objects.count(), 0)
