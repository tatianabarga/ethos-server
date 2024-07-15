from django.db import models


class Circle(models.Model):

  creator_id = models.CharField(max_length=50)