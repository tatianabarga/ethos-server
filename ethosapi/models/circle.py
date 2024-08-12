from django.db import models
from .user import User


class Circle(models.Model):

  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)