from django.conf.urls import url
from django.urls import path, include

from .views import *

urlpatterns = [
    url('logout', user_logout, name='logout'),
    url('login', user_login, name='login'),
    url('register', user_register, name='register'),
    url('join_team', JoinTeamView.as_view(), name='join_team'),
]
