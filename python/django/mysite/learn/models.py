from __future__ import unicode_literals

from django.db import models

class people(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
