from django.http.response import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

from lib.wso2.services.eventProcessorAdminService import EventProcessor
from lib.trend_prediction import Prediction
import os
import re

from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

predictions = Prediction()
predictions.create_linear_model()


def estimate_trend(request):
    context = {
        'scatter_diagram': "images/figs/" + predictions.generate_scatter(),
        'regression_line': "images/figs/" + predictions.estimate_trend_line(),
    }
    return render(request, 'map_service/alerts/estimate_trend.html', context=context)


def set_proximity_alert(request):
    selected_date = request.POST['selected_date']
    date_format = "%m/%d/%Y"
    selected_date = datetime.strptime(selected_date, date_format)
    predicted_density = predictions.sckit_lm_predict(selected_date)
    return JsonResponse({'predicted_density': predicted_density[0][0]})


def get_speed_alert(request):
    speed_value = -1  # TODO: This value should fetch from organization.globals.speed_limit {MongoDB}
    context = {
        'speed_value': speed_value
    }
    return render(request, 'map_service/alerts/speed.html', context=context)


def set_speed_alert(request):
    speed_limit = request.POST['speedAlertValue']
    alert_template = open(os.path.join(BASE_DIR, 'map_service/templates/map_service/xml/geo_speed_alert.xml'))
    placeholder_pattern = re.compile(r'\$speedAlertValue')
    alert_query = placeholder_pattern.sub(speed_limit, alert_template.read())

    evnt_proc = EventProcessor()
    exe_plan_name = 'geo_speed_alert'
    exe_plan = evnt_proc.getActiveExecutionPlanConfiguration(exe_plan_name)
    if exe_plan:
        response = evnt_proc.editActiveExecutionPlanConfiguration(alert_query, exe_plan_name)
    else:
        response = evnt_proc.deployExecutionPlanConfigurationFromConfigXml(alert_query)

    return JsonResponse({'status': True})


def geofence_alert(request):
    """
    A geofence is a virtual barrier. Programs that incorporate geo-fencing allow an administrator to set up triggers
    so when a device enters (or exits) the boundaries defined by the administrator, a popup message or email alert is sent.
    :param request:
    :return:
    """
    geofences = [
        {
            'areaName': 'Test_name_1',
            'queryName': 'Testing_query_name_1',
            'createdTime': datetime.now(),
            'geoJson': {
                'geoJsonStructure': True
            }
        }, {
            'areaName': 'Test_name_2',
            'queryName': 'Testing_query_name_2',
            'createdTime': datetime.now(),
            'geoJson': {
                'geoJsonStructure': True
            }
        }, {
            'areaName': 'Test_name_3',
            'queryName': 'Testing_query_name_3',
            'createdTime': datetime.now(),
            'geoJson': {
                'geoJsonStructure': True
            }
        },
    ]
    context = {
        'geofences': geofences
    }
    return render(request, 'map_service/alerts/within.html', context=context)


def set_geofence_alert(request):
    queryName = 'geo_within_' + request.POST[
        'queryName'] + '_alert'  # TODO: Use this name to store the query in Database or remove this completly and use the area name only
    areaName = request.POST['areaName']
    geoFenceGeoJSON = request.POST['geoFenceGeoJSON']

    alert_template = open(os.path.join(BASE_DIR, 'map_service/templates/map_service/xml/geo_within_alert.xml'))
    placeholder_pattern = re.compile(r'\$areaName')
    alert_query = placeholder_pattern.sub(areaName, alert_template.read())

    placeholder_pattern = re.compile(r'\$geoFenceGeoJSON')
    alert_query = placeholder_pattern.sub(geoFenceGeoJSON, alert_query)

    placeholder_pattern = re.compile(r'\$executionPlanName')
    alert_query = placeholder_pattern.sub(queryName, alert_query)

    evnt_proc = EventProcessor()
    evnt_proc.deployExecutionPlanConfigurationFromConfigXml(alert_query)

    return JsonResponse({'status': True})


def get_stationery_alert(request):
    raise Http404("Not implemented yet")


def service_not_available(request):
    raise Http404("Not implemented yet")