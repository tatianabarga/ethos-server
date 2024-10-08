from rest_framework.test import APITestCase
from rest_framework import status
from ethosapi.models import User, Circle, Profile, CircleProfile, Score

class ProfileTests(APITestCase):
    
    def setUp(self):
      self.user = User.objects.create(name="Test User", uid="12345")
      self.circle1 = Circle.objects.create(name="Circle 1", creator=self.user)
      self.circle2 = Circle.objects.create(name="Circle 2", creator=self.user)
      self.profile_data = {
          "creator": self.user.id,
          "bio": "Test Bio",
          "name": "Test Name",
          "circles": [self.circle1.id, self.circle2.id]
      }
      self.profile = Profile.objects.create(
          creator=self.user,
          bio="Test Bio",
          name="Test Name"
      )
      CircleProfile.objects.create(circle=self.circle1, profile=self.profile)
      CircleProfile.objects.create(circle=self.circle2, profile=self.profile)
      Score.objects.create(score="10", profile=self.profile)
        
    def test_create_profile(self):
      url = '/profiles'
      response = self.client.post(url, self.profile_data, format='json')
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(Profile.objects.count(), 2)
      self.assertEqual(Profile.objects.get(id=response.data['id']).bio, "Test Bio")
      self.assertEqual(CircleProfile.objects.filter(profile=response.data['id']).count(), 2)
      self.assertEqual(Score.objects.last().score, "10")
      
    def test_retrieve_profile(self):
      url = f'/profiles/{self.profile.id}'
      response = self.client.get(url)
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['name'], self.profile.name)
      self.assertEqual(len(response.data['circles']), 2)

    def test_update_profile(self):
        update_data = {
            "bio": "Updated Bio",
            "name": "Updated Name",
            "circles": [self.circle1.id]  # Remove one circle
        }
        url = f'/profiles/{self.profile.id}'
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.bio, "Updated Bio")
        self.assertEqual(updated_profile.name, "Updated Name")
        self.assertEqual(CircleProfile.objects.filter(profile=updated_profile).count(), 1)

    def test_delete_profile(self):
        url = f'/profiles/{self.profile.id}'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(CircleProfile.objects.filter(profile=self.profile.id).count(), 0)
        self.assertEqual(Score.objects.filter(profile=self.profile.id).count(), 0)
