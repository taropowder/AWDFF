from uuid import uuid4

from django.db import models
from problem.models import Attack


# Create your models here.
class Team(models.Model):
    name = models.CharField('队伍名称', max_length=50, unique=True)
    token = models.CharField('队伍ID', max_length=8, unique=True, default=uuid4())

    @property
    def score(self):
        solved_problems = Attack.objects.filter(member=self)
        integral = 0
        for solved_problem in solved_problems:
            try:
                integral += solved_problem.integral
            except:
                pass
        return integral

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = verbose_name
        ordering = ['-id']