import time
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, CreateView, FormView, ListView
from problem.models import *
from team.models import *
from .form import *
from django.http import JsonResponse, HttpResponseRedirect
from uuid import UUID
from AWDFF.settings import END_TIME, START_TIME


# Create your views here.


class solveProblemView(View):

    def post(self, request):
        result = {}
        start_time = time.mktime(time.strptime(START_TIME, "%Y/%m/%d %H:%M:%S"))
        end_time = time.mktime(time.strptime(END_TIME, "%Y/%m/%d %H:%M:%S"))
        now = int(time.time())
        if start_time < now < end_time:
            try:
                problem = Problem.objects.get(flag=request.POST.get('flag'))
            except Problem.DoesNotExist:
                problem = None
            if problem:
                try:
                    token_uuid = UUID(request.POST.get('token').lower())
                    team = Team.objects.get(token=token_uuid)
                except Team.DoesNotExist:
                    team = None
                if team:
                    if team != problem.team:
                        try:
                            attack = Attack.objects.get(problem=problem, attack_team=team, rounds=problem.rounds)
                        except Attack.DoesNotExist:
                            attack = None
                        if attack:
                            result['result'] = -1
                            result['message'] = "已经提交过了,不能再提交了"
                            result['title'] = "提交失败"
                        else:
                            acctack = Attack.objects.create(problem=problem, attack_team=team, rounds=problem.rounds)
                            hacked = Hack.objects.filter(problem=problem, rounds=problem.rounds).first()
                            if not hacked:
                                hacked = Hack.objects.create(problem=problem, rounds=problem.rounds)
                            problem.status = 'hacked'
                            problem.save()
                            result['result'] = 1
                            result['message'] = "提交正确"
                            result['title'] = "提交成功"

                    else:
                        result['result'] = -1
                        result['message'] = "你不能提交自己的FLAG"
                        result['title'] = "提交失败"
                else:
                    result['result'] = -1
                    result['message'] = "TOKEN异常"
                    result['title'] = "提交失败"
            else:
                result['result'] = 0
                result['message'] = "FLAG错误"
                result['title'] = "提交失败"
        else:
            result['result'] = -1
            result['message'] = "比赛未开始或者已经结束"
            result['title'] = "提交失败"
        return JsonResponse(result, safe=False)
        # return render(request, 'alert.html', result)


class TeamListView(ListView):
    template_name = 'competition/team_list.html'
    model = Team

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['team_list'] = sorted(context['team_list'], key=lambda t: t.score, reverse=True)
        return context
