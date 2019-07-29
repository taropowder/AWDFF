from django.shortcuts import render
import re
import time
import os
from .settings import END_TIME, START_TIME, ROUND_TIME_INTERVAL
from problem.models import Problem, ProblemTemplate
from team.models import Team

START_CHECK_TIME = None


def home(request):
    context = {'temples': {}}
    temples = ProblemTemplate.objects.all()
    for temple in temples:
        context['temples'][temple.name] = Problem.objects.filter(template=temple)
    teams = Team.objects.all()
    context['teams'] = sorted(teams, key=lambda t: t.score, reverse=True)
    host = request.META['HTTP_HOST']
    host_without_port = re.search(r'(.+):.+', host)
    if host_without_port:
        host_without_port = host_without_port.group(1)
    if host_without_port:
        host = host_without_port
    now = int(time.time())
    context['host'] = host
    context['time'] = {'name': None, 'start': True, 'last_time': None}
    if START_TIME and END_TIME:
        start_time = time.mktime(time.strptime(START_TIME, "%Y/%m/%d %H:%M:%S"))
        end_time = time.mktime(time.strptime(END_TIME, "%Y/%m/%d %H:%M:%S"))
        context['time']['last_time'] = (start_time - now) % (60 * ROUND_TIME_INTERVAL)
        if start_time - now > 0:
            context['time']['name'] = "开始时间"
            context['time']['time'] = START_TIME
            context['time']['start'] = False
        elif end_time - now > 0:
            context['time']['name'] = "结束时间"
            context['time']['time'] = END_TIME
    return render(request, 'start.html', context)
