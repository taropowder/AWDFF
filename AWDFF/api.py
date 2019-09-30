from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from .apiView import *
from competition.views import solveProblemView
from account.views import JoinTeamView,user_login,user_register

urlpatterns = [
    path('user/info/', userInfo),
    path('rank/', teamRank),
    path('gamebox/', problemInfo),
    path('games/', ProblemTemplateInfo),
    path('token/', getToken),
    path('submit/', csrf_exempt(solveProblemView.as_view())),
    path('time/', RaceTime),
    path('roundtime/', RoundTime),
    path('announcement/', getAnnouncement),
    path('team/info/', TeamInfo),
    path('team/join/', csrf_exempt(JoinTeamView.as_view())),
    path('account/login/', csrf_exempt(user_login)),
    path('account/register/', csrf_exempt(user_register)),
    re_path(r'game/(\d+)', allGame),
    re_path(r'game/attack/(\d+)', getAttackRecord),
    re_path(r'game/hack/(\d+)', getHackRecord),
    re_path(r'game/down/(\d+)', getDownRecord),
    re_path(r'game/restart/(\d+)', getDownRecord),

]
