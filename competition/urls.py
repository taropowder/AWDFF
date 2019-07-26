from django.conf.urls import url
from django.urls import path, include

from .views import *

urlpatterns = [
    url('submit_flag', solveProblemView.as_view(), name='submit_flag'),
    url('team_list', TeamListView.as_view(), name='team_list')
]
