"""YanHai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from .settings import MEDIA_ROOT
import xadmin
from commoditys.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('commoditys/', include('commoditys.urls', namespace='commoditys')),
    path('booklist/',include('booklist.urls',namespace='booklist')),
    re_path('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})
]
