from django.contrib import admin
from .models import *
from .views import InstantiateAllProblemView

# Register your models here.


admin.site.register(ProblemTemplate)


@admin.register(Down)
class DownAdmin(admin.ModelAdmin):
    list_display = ('problem', 'time', 'team', 'rounds')
    list_display_links = ('problem',)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('container_id', 'time', 'template', 'web_external_port', 'ssh_external_port', 'status', 'team')
    list_display_links = ('container_id',)

    # def name(self, obj):
    #     return str(obj.owner) + "：" + str(obj.owner.first_name)


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
            admin.site.admin_view(InstantiateAllProblemView.as_view()), name='instantiate_all_problem')
    ]
    return urls


admin.site.get_urls = get_urls
