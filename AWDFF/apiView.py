import os
import re

from django.http import JsonResponse
import time

from AWDFF.settings import START_TIME, END_TIME, PLAY_NOW, ROUND_TIME_INTERVAL
from account.models import Member
from announcement.models import Announcement
from problem.models import ProblemTemplate, Problem, Attack, Down, Hack, Restart
from team.models import Team


def userInfo(request):
    if request.user.team:
        teamid = request.user.team.id
    else:
        teamid = None
    data = {
        "username": request.user.username,
        "teamId": teamid,
    }

    return JsonResponse(data, safe=False)


def teamRank(request):
    teams = Team.objects.all()
    teams = sorted(teams, key=lambda t: t.score, reverse=True)
    data = []
    for team in teams:
        data.append({
            "team": team.name,
            "integral": team.score,
        })
    return JsonResponse(data, safe=False)


def problemInfo(request):
    problems = request.user.team.problems
    data = []
    for problem in problems:
        data.append({

            "title": problem.template.name,
            "id": problem.id,
            "info": {
                "轮次": problem.rounds,
                "分值": problem.score,
                "web端口": problem.web_external_port,
                "ssh端口": problem.ssh_external_port,
                "ssh用户": "user",
                "ssh密码": problem.ssh_passwd,
            }

        })
    return JsonResponse(data, safe=False)


def ProblemTemplateInfo(request):
    problems = request.user.team.problems
    data = []
    for problem in problems:
        data.append({
            "id": problem.template.id,
            "name": problem.template.name,
        }, )
    return JsonResponse(data, safe=False)


def getToken(request):
    data = {
        "token": request.user.team.token
    }
    return JsonResponse(data, safe=False)


def RaceTime(request):
    now = int(time.time())
    data = {}
    if START_TIME and END_TIME:
        start_time = time.mktime(time.strptime(START_TIME, "%Y/%m/%d %H:%M:%S"))
        end_time = time.mktime(time.strptime(END_TIME, "%Y/%m/%d %H:%M:%S"))
        if start_time - now > 0:
            data['status'] = "开始"
            data['serverTime'] = START_TIME
        elif end_time - now > 0:
            data['status'] = "结束"
            data['serverTime'] = END_TIME
    return JsonResponse(data, safe=False)


def RoundTime(request):
    with open("/tmp/round.time") as f:
        lastRoundTime = f.readline()
    if lastRoundTime:
        timeArray = time.localtime(int(lastRoundTime))
        lastRoundTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    data = {
        "lastRoundTime": lastRoundTime,
    }
    return JsonResponse(data, safe=False)


def getAttackRecord(request, id):
    # print(request.user.team)
    print(request.user)
    # id = int(id)
    attacks = Attack.objects.filter(problem__template_id=id).filter(attack_team=request.user.team)
    data = {
        id: {
            "info": []
        }
    }

    for attack in attacks:
        data[id]['info'].append({
            "time": attack.time.strftime("%Y-%m-%d %H:%M:%S"),
            "round": attack.rounds,
            "team": attack.problem.team.name
        })

    return JsonResponse(data, safe=False)


def getHackRecord(request, id):
    # print(request.user.team)
    hacks = Hack.objects.filter(problem__template_id=id).filter(problem__team=request.user.team)
    data = {
        id: {
            "info": []
        }
    }
    for hack in hacks:
        data[id]['info'].append({
            "time": hack.time.strftime("%Y-%m-%d %H:%M:%S"),
            "round": hack.rounds,
            "team": hack.problem.team.name
        })

    return JsonResponse(data, safe=False)


def getDownRecord(request, id):
    attacks = Down.objects.filter(problem__template_id=id).filter(team=request.user.team)
    data = {
        id: {
            "info": []
        }
    }
    for attack in attacks:
        data[id]['info'].append({
            "time": attack.time.strftime("%Y-%m-%d %H:%M:%S"),
            "round": attack.rounds,
            "team": attack.problem.team.name
        })

    return JsonResponse(data, safe=False)


def getRestartRecord(request, id):
    attacks = Restart.objects.filter(problem__template_id=id).filter(team=request.user.team)
    data = {
        id: {
            "info": []
        }
    }
    for attack in attacks:
        data[id]['info'].append({
            "time": attack.time.strftime("%Y-%m-%d %H:%M:%S"),
            "round": attack.rounds,
            "team": attack.problem.team.name
        })

    return JsonResponse(data, safe=False)


def TeamInfo(request):
    team = request.user.team
    data = {
        "name": team.name,
        "teamId": team.id,
        "rank": 1,
        "score": team.score,
        "uuid": team.token,
        "members": [

        ]
    }
    members = Member.objects.filter(team=team)
    for member in members:
        data['members'].append({
            "id": member.id,
            "name": member.username,
        })
    return JsonResponse(data, safe=False)

def allGame(request, id):
    problems = Problem.objects.filter(template_id=id)
    data ={id:{"info":[]}}
    host = request.META['HTTP_HOST']
    host_without_port = re.search(r'(.+):.+', host)
    if host_without_port:
        host_without_port = host_without_port.group(1)
    if host_without_port:
        host = host_without_port
    for problem in problems:
        data[id]["info"].append({
            "round":problem.rounds,
            "url": f"http://{host}:{problem.web_external_port}"
        })
    return JsonResponse(data, safe=False)


def getAnnouncement(request):
    data = []
    announcemnets = Announcement.objects.all().order_by('create_time')
    for announcemnet in announcemnets:
        data.append({
            "title": announcemnet.title,
            "time": announcemnet.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": announcemnet.content
        })

    return JsonResponse(data, safe=False)