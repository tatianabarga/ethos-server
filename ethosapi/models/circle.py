from django.db import models
from .user import User


class Circle(models.Model):

  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  # users = models.ManyToManyField(User, through='CircleUser', related_name='circle')