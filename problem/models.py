from django.db import models


# Create your models here.

class ProblemTemplate(models.Model):
    image_id = models.CharField('镜像id', max_length=50, unique=True)
    score = models.IntegerField('题目分数')
    internal_port = models.IntegerField('内部端口')
    docker_command = models.CharField('docker 启动命令', max_length=100)
    change_flag_command = models.TextField('修改flag的命令', help_text='请用{flag}替换flag的位置')

    class Meta:
        verbose_name = '题目模板（docker镜像）'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Problem(models.Model):
    web_external_port = models.IntegerField('web 题目外部端口')
    ssh_external_port = models.IntegerField('ssh 外部端口')
    template = models.ForeignKey(ProblemTemplate, on_delete=models.CASCADE)
    flag = models.CharField('题目FLAG', max_length=50, unique=True)
    container_id = models.CharField('容器id', max_length=50, unique=True)
    # 容器状态分为 正常运行、宕机、被攻陷 三种状态
    STATUS_CHOICES = (
        ('running', '正常运行'),
        ('down', '宕机'),
        ('hacked', '被攻陷'),
    )
    status = models.CharField('容器状态', choices=STATUS_CHOICES, max_length=10)

    class Meta:
        verbose_name = '题目实例 (docker 容器)'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Attack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '攻击记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']
