from django.shortcuts import render
import re

from problem.models import Problem, ProblemTemplate
from team.models import Team


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
        host_without_port=host_without_port.group(1)
    if host_without_port:
        host = host_without_port
    context['host'] = host
    return render(request, 'start.html', context)
