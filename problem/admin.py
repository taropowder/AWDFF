from django.contrib import admin
from django.http import HttpResponseRedirect
from utils.dockerController import DockerController
from .models import *
from .views import *

# Register your models here.


admin.site.register(ProblemTemplate)
admin.site.register(Hack)


@admin.register(Down)
class DownAdmin(admin.ModelAdmin):
    list_display = ('problem', 'time', 'team', 'rounds')
    list_display_links = ('problem',)


@admin.register(Restart)
class RestartAdmin(admin.ModelAdmin):
    list_display = ('problem', 'time', 'team', 'rounds')
    list_display_links = ('problem',)

# @admin.register(Problem)
# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ('container_id', 'time', 'template', 'web_external_port', 'ssh_external_port', 'status', 'team')
#     list_display_links = ('container_id',)

# def name(self, obj):
#     return str(obj.owner) + "：" + str(obj.owner.first_name)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    change_form_template = "manager/problem_list.html"
    list_display = ('container_id', 'time', 'template', 'web_external_port', 'ssh_external_port', 'status', 'team')
    list_display_links = ('container_id',)

    def response_change(self, request, obj):
        if "_restart" in request.POST:
            docker_controller = DockerController()
            docker_controller.rm_container(obj.container_id)
            template = obj.template
            docker_info = docker_controller.run_container(template.image_id, template.internal_port)
            obj.container_id = docker_info['id']
            obj.ssh_external_port = docker_info['ssh_port']
            obj.web_external_port = docker_info['web_port']
            obj.status = 'running'
            obj.flag, command = generate_flag_command(template.change_flag_command)
            docker_controller.exec_container(obj.container_id, command)
            obj.ssh_passwd, command = generate_ssh_paasword(template.change_passwd_command)
            docker_controller.exec_container(obj.container_id, command)
            obj.save()
            restart = Restart.objects.filter(team=obj.team,problem=obj,rounds=obj.rounds).first()
            if not restart:
                Restart.objects.create(team=obj.team,problem=obj,rounds=obj.rounds)
            self.message_user(request, f"{obj.container_id}重启成功")

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    list_display = ('detail', 'problem', 'time')
    list_display_links = ('detail',)

    def detail(self, obj):
        return str(obj)


_admin_site_get_urls = admin.site.get_urls


def get_urls():
    from django.conf.urls import url
    urls = _admin_site_get_urls()
    urls += [
        url(r'^instantiate_all_problem/$',
            admin.site.admin_view(InstantiateAllProblemView.as_view()), name='instantiate_all_problem'),
        url(r'^remove_all_problem/$',
            admin.site.admin_view(RemoveAllProblem.as_view()), name='remove_all_problem'),
    ]
    return urls


admin.site.get_urls = get_urls
