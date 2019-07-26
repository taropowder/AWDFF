from uuid import uuid1

from django.db import models
from problem.models import Attack, Problem


# Create your models here.
class Team(models.Model):
    name = models.CharField('队伍名称', max_length=50, unique=True)
    token = models.CharField('队伍ID', max_length=36, unique=True, default=uuid1())

    @property
    def score(self):
        solved_problems = Attack.objects.filter(attack_team=self)
        integral = 0
        for solved_problem in solved_problems:
            try:
                integral += solved_problem.problem.template.score
            except:
                pass
        hacked_problems = Problem.objects.filter(team=self, status='hacked')
        for hacked_problem in hacked_problems:
            try:
                integral -= hacked_problem.template.score
            except:
                pass
        return integral

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = verbose_name
        ordering = ['-id']
