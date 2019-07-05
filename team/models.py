from uuid import uuid4

from django.db import models


# Create your models here.
class Team(models.Model):
    name = models.CharField('队伍名称', max_length=50, unique=True)
    token = models.CharField('队伍ID', max_length=8, unique=True, default=uuid4())
