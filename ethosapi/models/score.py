from django.db import models
from .profile import Profile


class Score(models.Model):

  score = models.CharField(max_length=50)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)