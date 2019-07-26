import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, UpdateView, CreateView, FormView, ListView

from problem.models import Problem, ProblemTemplate
from team.models import Team
from utils.dockerController import DockerController
from utils.flag import generate_flag_command,generate_ssh_paasword
from django.http import HttpResponse

# Create your views here.

# TODO build赛题 (先采用制定镜像ID的方式)

# TODO 实例化赛题并将容器ID、web端口、ssh端口存入数据库
# TODO flag按轮刷新，执行

docker_controller = DockerController()


class InstantiateAllProblemView(View):
    # template_name = 'admin/instantiate_problem.html'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     user = self.request.user
    #     user.team = self.object
    #     user.is_leader = True
    #     user.save()
    #     # return HttpResponseRedirect(reverse_lazy('team_detail', kwargs={'pk': self.object.id}))
    def post(self, request):
        teams = Team.objects.all()
        resp = {'status':'ok'}
        template = get_object_or_404(ProblemTemplate,pk=request.POST.get('template_id', None))
        for team in teams:
            docker_info = docker_controller.run_container(template.image_id,template.internal_port)
            problem = Problem()
            problem.container_id = docker_info['id']
            problem.ssh_external_port = docker_info['ssh_port']
            problem.web_external_port = docker_info['web_port']
            problem.status = 'running'
            problem.template = template
            problem.team = team
            problem.flag, command = generate_flag_command(template.change_flag_command)
            docker_controller.exec_container(problem.container_id, command)
            problem.ssh_passwd, command = generate_ssh_paasword(template.change_passwd_command)
            docker_controller.exec_container(problem.container_id, command)
            problem.save()

        return HttpResponse(json.dumps(resp), content_type="application/json")

    def get(self,request):
        result = {}
        templates = ProblemTemplate.objects.all()
        result['templates'] = templates
        return render(request,'manager/instantiate_all_problem.html',result)