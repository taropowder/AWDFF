from django.db import models


# Create your models here.

class ProblemTemplate(models.Model):
    ADD_USER_COMMAND = """bash -c "useradd -p `openssl passwd -1 -salt 'taro' {password}` user" """
    name = models.CharField('题目名称', max_length=50, unique=True)
    image_id = models.CharField('镜像id', max_length=50, unique=True)
    score = models.IntegerField('题目分数')
    internal_port = models.IntegerField('内部端口')
    docker_command = models.CharField('docker 启动命令', max_length=100, null=True, blank=True)
    change_passwd_command = models.TextField('修改用户密码的命令',
                                             default=ADD_USER_COMMAND,
                                             help_text="请用{passwd} 替换密码的位置,"
                                                       "如环境内存在openssl并且不存在user用户则不需要修改此命令")
    change_flag_command = models.TextField('修改flag的命令', default='bash -c \"echo \'{flag}\' > /flag\"',
                                           help_text='请用{flag}替换flag的位置,注意：如果需要重定向写入flag'
                                                     '需要显式调用可执行文件,例如： '
                                                     'bash -c \"echo \'{flag}\' > /flag\"')

    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '题目模板（docker镜像）'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Problem(models.Model):
    web_external_port = models.IntegerField('web 题目外部端口')
    ssh_external_port = models.IntegerField('ssh 外部端口')
    ssh_passwd = models.CharField('ssh密码', max_length=12)
    template = models.ForeignKey(ProblemTemplate, on_delete=models.CASCADE)
    flag = models.CharField('题目FLAG', max_length=50, unique=True)
    container_id = models.CharField('容器id', max_length=50, unique=True)
    # 容器状态分为 正常运行、宕机、被攻陷 三种状态
    STATUS_CHOICES = (
        ('running', '正常运行'),
        ('down', '宕机'),
        ('hacked', '被攻陷'),
    )
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    status = models.CharField('容器状态', choices=STATUS_CHOICES, max_length=10)
    time = models.DateTimeField(auto_now=True)
    rounds = models.IntegerField('比赛轮次', default=0)

    @property
    def score(self):
        attack = Attack.objects.filter(problem=self)
        if attack.first():
            return self.template.score / len(attack)
        else:
            return self.template.score

    def __str__(self):
        return self.container_id + ">>>>>>>" + self.team.name

    class Meta:
        verbose_name = '题目实例 (docker 容器)'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Attack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    attack_team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    rounds = models.IntegerField('比赛轮次', help_text="相同轮次内只可以攻击一次")

    @property
    def score(self):
        init_scorce = self.problem.template.score
        attack_team_count = Attack.objects.filter(rounds=self.rounds, problem=self.problem).count()
        return init_scorce / attack_team_count

    def __str__(self):
        return self.attack_team.name + ">>>>HACK>>>>" + self.problem.team.name

    class Meta:
        verbose_name = '攻击记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Hack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    rounds = models.IntegerField('比赛轮次', help_text="相同轮次内只可以攻击一次")

    def __str__(self):
        return self.problem.team.name + f"ROUND {self.rounds}  be hacked"

    class Meta:
        verbose_name = '被攻击记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Down(models.Model):
    time = models.DateTimeField('宕机时间', auto_now_add=True)
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    rounds = models.IntegerField('比赛轮次', help_text="相同轮次内只会被判定宕机一次")
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '宕机记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']
