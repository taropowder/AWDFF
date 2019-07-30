"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'AWDFF.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'AWDFF.dashboard.CustomAppIndexDashboard'
"""
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from AWDFF import settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for AWDFF.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('返回站点'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(modules.LinkList(
            _('赛题管理'),
            children=[
                {
                    'title': '开启赛题',
                    'url': '/admin/instantiate_all_problem',
                    'external': False,
                },
                {
                    'title': '关闭赛题',
                    'url': '/admin/remove_all_problem',
                    'external': False,
                },
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('最近操作'), 5))

        # append a feed module
        # 太慢了..太慢了..太慢了....
        # self.children.append(modules.Feed(
        #     _('Latest Django News'),
        #     feed_url='http://www.djangoproject.com/rss/weblog/',
        #     limit=5
        # ))

        self.children.append(modules.LinkList(
            _('比赛信息'),
            children=[
                {
                    'title': f'开始时间  {settings.START_TIME}',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'结束时间  {settings.END_TIME}',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'check 频率 {settings.CHECK_TIME_INTERVAL}min 1次',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'每轮时间 {settings.ROUND_TIME_INTERVAL}min',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'check日志位置 {settings.CHECK_LOG}',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'刷新轮次日志位置 {settings.ROUND_LOG}',
                    'url': '#',
                    'external': False,
                },
                {
                    'title': f'PLAY NOW模式 {settings.PLAY_NOW}',
                    'url': '#',
                    'external': False,
                },
            ]
        ))
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for AWDFF.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """

        return super(CustomAppIndexDashboard, self).init_with_context(context)
