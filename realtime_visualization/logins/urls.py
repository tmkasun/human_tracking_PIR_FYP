__author__ = 'tmkasun'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^login_submit', views.submit, name='submit')
]