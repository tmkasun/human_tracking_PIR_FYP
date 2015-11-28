from django.http.response import HttpResponse
from django.shortcuts import render


def base_map(request):
    context = {
        'page_title': "Knnect Spatial Object Analysis and Prediction System"
    }
    return render(request, 'map_system/content/base_map.html', context=context)