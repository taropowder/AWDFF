from django.db import models


# Create your models here.
class Announcement(models.Model):
    title = models.CharField('标题', max_length=50)
    content = models.TextField("内容")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "公告"
        ordering = ['-create_time']