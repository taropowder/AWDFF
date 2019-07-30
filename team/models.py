import uuid
from django.db import models
from problem.models import Attack, Problem, Down, Hack, Restart


# Create your models here.
class Team(models.Model):
    name = models.CharField('队伍名称', max_length=50, unique=True)
    token = models.CharField('队伍UUID', max_length=50, unique=True, default=uuid.uuid4, help_text="可用于提交flag,加入队伍")

    # token = models.UUIDField(default=uuid.uuid4, null=False, blank=False, verbose_name=u'队伍TOKEN',
    #                          help_text="可用于提交flag,加入队伍")

    @property
    def ports(self):
        port_str = ""
        problems = Problem.objects.filter(team=self)
        for problem in problems:
            port_str += str(problem.web_external_port) + ","
        return port_str

    @property
    def score(self):
        solved_problems = Attack.objects.filter(attack_team=self)
        integral = 10000
        for solved_problem in solved_problems:
            try:
                integral += solved_problem.score
            except:
                pass
        hacked_problems = Hack.objects.filter(problem__team=self)
        for hacked_problem in hacked_problems:
            try:
                integral -= hacked_problem.problem.template.score
            except:
                pass
        down_problems = Down.objects.filter(team=self)
        for down_problem in down_problems:
            try:
                integral -= down_problem.problem.template.score * 1.5
            except:
                pass
        restart_problems = Restart.objects.filter(team=self)
        for restart_problem in restart_problems:
            try:
                integral -= restart_problem.problem.template.score * 2.0
            except:
                pass
        return integral

    @property
    def problems(self):
        problems = Problem.objects.filter(team=self)
        return problems

    @property
    def attacks(self):
        attack = Attack.objects.filter(attack_team=self)
        return attack

    @property
    def down(self):
        return Down.objects.filter(team=self)

    @property
    def restart(self):
        return Restart.objects.filter(team=self)

    @property
    def sheep(self):
        return Hack.objects.filter(problem__team=self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '队伍'
        verbose_name_plural = verbose_name
        ordering = ['-id']
