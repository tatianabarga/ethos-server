from django.db import models
from .circle import Circle
from .user import User


class CircleUser(models.Model):

  circle_id = models.ForeignKey(Circle, on_delete=models.CASCADE)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)