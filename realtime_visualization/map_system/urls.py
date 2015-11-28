__author__ = 'tmkasun'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'base', views.base_map, name='base'),
    # url(r'.*', views.base_map, name='default')
]
