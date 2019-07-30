import json

from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.models import User
from AWDFF.settings import NUMBER_TEAM
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, DetailView, UpdateView, CreateView, FormView, ListView


# Create your views here.


def user_register(request):
    context = {}
    context['title'] = '注册失败'
    context['message'] = '未知异常'
    context['url'] = context['url'] = reverse_lazy('home') + '#register'

    if request.method == 'POST':
        name = request.POST.get('username')
        u = Member.objects.filter(username=name)
        if u:
            context['title'] = '注册失败'
            context['message'] = '该用户名已被使用'
            return render(request, 'alert.html', context)
        password = request.POST.get('password')
        email = request.POST.get('email')
        organization = request.POST.get('email')
        member = Member.objects.create_user(username=name, email=email, password=password, organization=organization)
        if member:
            context['title'] = '注册成功'
            context['message'] = '自动跳转至登录页面'
            context['url'] = reverse_lazy('home') + '#login'
        # user.save()
        # profile.grade = profile.student_id[0:2]
        # profile.save()
        # context['name'] = name
        # return render(request, 'login.html', context)
    return render(request, 'alert.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    context = {}
    # context['statu'] = '0'
    if request.method == 'POST':
        get_name = request.POST.get('username')
        get_password = request.POST.get('password')
        user = authenticate(username=get_name, password=get_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = request.GET.get('next', '/')
                return HttpResponseRedirect(url)
            else:
                context['title'] = '登录失败'
                context['message'] = "您的用户已经被限制,请联系工作人员"
        else:
            context['title'] = '登录失败'
            context['message'] = "用户名或者密码错误"
        context['url'] = reverse_lazy('home') + '#login'
        return render(request, 'alert.html', context)


class JoinTeamView(View):

    def post(self, request):
        context = {'title': '加入成功'}
        context['url'] = reverse_lazy('home') + '#info'
        token = request.POST.get('token').lower()
        team = Team.objects.filter(token=token).first()
        if team:
            if Member.objects.filter(team=team).count() < NUMBER_TEAM:
                context['message'] = f'成功加入{team.name}队'
                request.user.team = team
                request.user.save()
            else:
                context['title'] = '加入失败'
                context['message'] = '队伍人数已满'
        else:
            context['title'] = '加入失败'
            context['message'] = '该队伍不存在,请确认token'
        return render(request, 'alert.html', context)
