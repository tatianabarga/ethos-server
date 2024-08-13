from django.db import models
from .user import User
from .circle import Circle


class Profile(models.Model):

  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  bio = models.CharField(max_length=50)
  name = models.CharField(max_length=50)
  circles = models.ManyToManyField(Circle, through='CircleProfile', related_name='profile')