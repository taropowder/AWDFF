"""AWDFF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from .view import home, page_not_found

urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^$', home, name='home'),
    path('admin/', admin.site.urls),
    path('problem/', include('problem.urls')),
    path('account/', include('account.urls')),
    path('competition/', include('competition.urls'))
]

handler404 = page_not_found