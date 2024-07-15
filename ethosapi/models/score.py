from django.db import models


class Score(models.Model):

  score = models.CharField(max_length=50)