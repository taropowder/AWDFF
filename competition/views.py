from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView, FormView, ListView
from problem.models import *
from team.models import *
from .form import *
from django.http import JsonResponse, HttpResponseRedirect
from uuid import UUID

# Create your views here.


class solveProblemView(FormView):
    template_name = 'competition/submitFLAG.html'
    form_class = ProblemFrom

    def form_valid(self, form):
        result = {}
        try:
            problem = Problem.objects.get(flag=form.data['flag'])
        except Problem.DoesNotExist:
            problem = None
        if Problem:
            try:
                token_uuid = UUID(form.data['token'])
                team = Team.objects.get(token=token_uuid)
            except Team.DoesNotExist:
                team = None
            if team:
                if team != problem.team:
                    try:
                        attack = Attack.objects.get(problem=problem,attack_team=team)
                    except Attack.DoesNotExist:
                        attack = None
                    if attack:
                        result['message'] = "已经提交过了,不能再提交了"
                        result['status'] = False
                    else:
                        acctack = Attack.objects.create(problem=problem, attack_team=team)
                        problem.status = 'hacked'
                        problem.save()
                        result['message'] = "提交正确"
                        result['status'] = True
                else:
                    result['message'] = "你不能提交自己的FLAG"
                    result['status'] = False
            else:
                result['message'] = "TOKEN异常"
                result['status'] = False
        else:
            result['message'] = "FLAG错误"
            result['status'] = False
        return JsonResponse(result)


class TeamListView(ListView):
    template_name = 'competition/team_list.html'
    model = Team

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['team_list'] = sorted(context['team_list'], key=lambda t: t.score, reverse=True)
        return context