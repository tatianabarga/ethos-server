from django.db import models
from .circle import Circle
from .profile import Profile


class CircleProfile(models.Model):

  circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)