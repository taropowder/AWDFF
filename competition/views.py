from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, FormView, ListView
from problem.models import *
from team.models import *
from .form import *
from django.http import JsonResponse, HttpResponseRedirect
from uuid import UUID

# Create your views here.


class solveProblemView(FormView):

    def post(self, request):
        result = {}
        result['url'] = reverse_lazy('home') + '#submit'
        try:
            problem = Problem.objects.get(flag=request.POST.get('flag'))
        except Problem.DoesNotExist:
            problem = None
        if problem:
            try:
                token_uuid = UUID(request.POST.get('token'))
                team = Team.objects.get(token=token_uuid)
            except Team.DoesNotExist:
                team = None
            if team:
                if team != problem.team:
                    try:
                        attack = Attack.objects.get(problem=problem,attack_team=team,rounds=problem.rounds)
                    except Attack.DoesNotExist:
                        attack = None
                    if attack:
                        result['message'] = "已经提交过了,不能再提交了"
                        result['title'] = "提交失败"
                    else:
                        acctack = Attack.objects.create(problem=problem, attack_team=team,rounds=problem.rounds)
                        problem.status = 'hacked'
                        problem.save()
                        result['message'] = "提交正确"
                        result['title'] = "提交成功"
                        result['url'] = reverse_lazy('home') + '#info'

                else:
                    result['message'] = "你不能提交自己的FLAG"
                    result['title'] = "提交失败"
            else:
                result['message'] = "TOKEN异常"
                result['title'] = "提交失败"
        else:
            result['message'] = "FLAG错误"
            result['title'] = "提交失败"
        return render(request, 'alert.html', result)


class TeamListView(ListView):
    template_name = 'competition/team_list.html'
    model = Team

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['team_list'] = sorted(context['team_list'], key=lambda t: t.score, reverse=True)
        return context