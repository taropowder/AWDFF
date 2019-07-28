from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from team.models import Team


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Member(AbstractUser):
    username = models.CharField('用户名', max_length=64, unique=True)
    email = models.EmailField('邮箱', max_length=255, unique=True)
    organization = models.CharField('组织', max_length=30)
    team = models.ForeignKey(Team, verbose_name="队伍", on_delete=models.CASCADE, null=True, blank=True)
    # is_leader = models.BooleanField('是否为队长', default=False)
    objects = MyUserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username
