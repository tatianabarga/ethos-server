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
