from django.db import models
from .user import User
from .profile import Profile
from .score import Score


class Log(models.Model):

  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  score_impact = models.CharField(max_length=50)
  title = models.CharField(max_length=50)
  description = models.CharField(max_length=50)
  event_date = models.DateField(auto_now=True)
  log_date = models.DateField(auto_now=True)