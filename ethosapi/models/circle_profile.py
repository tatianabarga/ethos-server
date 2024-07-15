from django.db import models
from .circle import Circle
from .profile import Profile


class CircleProfile(models.Model):

  circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
  profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)