__author__ = 'tmkasun'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^speed_alert$', views.get_speed_alert, name='get_speed'),
    url(r'^set_speed_alert', views.set_speed_alert, name='set_speed'),

    url(r'^proximity_alert', views.proximity_alert, name='get_proximity'),
    url(r'^set_proximity_alert', views.set_proximity_alert, name='set_proximity'),

    url(r'geofencing', views.geofence_alert, name='get_geofence'),
    url(r'set_geofence', views.set_geofence_alert, name='set_geofence'),

    url(r'stationery_alert', views.get_stationery_alert, name='get_stationery'),
    url(r'.*',views.service_not_available, name='no_service')

]