from django.conf.urls import url
from django.urls import path, include

from .views import *

urlpatterns = [
    url('instantiate_all_problem', InstantiateAllProblemView.as_view(), name='instantiate_all_problem'),
]