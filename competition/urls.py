from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


from .views import *

urlpatterns = [
    url('submit_flag', csrf_exempt(solveProblemView.as_view()), name='submit_flag'),
    url('team_list', TeamListView.as_view(), name='team_list')
]
