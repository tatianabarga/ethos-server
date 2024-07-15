from django.db import models
from .user import User
from .score import Score


class Profile(models.Model):

  creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
  bio = models.CharField(max_length=50)
  name = models.CharField(max_length=50)
  # score_id = models.ForeignKey(Score, on_delete=models.CASCADE)