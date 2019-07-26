from django.contrib import admin
from .models import *
from .views import InstantiateAllProblemView

# Register your models here.


admin.site.register(ProblemTemplate)
admin.site.register(Attack)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('container_id', 'time', 'template', 'web_external_port', 'ssh_external_port', 'status', 'team')
    list_display_links = ('container_id',)

    # def name(self, obj):
    #     return str(obj.owner) + "：" + str(obj.owner.first_name)
    #


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
