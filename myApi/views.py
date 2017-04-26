# encoding=utf-8
import json
import os

from django.http import Http404
from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from myApi.single_use_rate import main_process
from django_api import settings


def home_page(request):
    return render(request, 'index.html')


@csrf_exempt
def single_use_rate(request):
    if request.method == 'POST':
        data = request.POST
        # 命名规则：x_y_width_height_border.png
        filename = '%s_%s_%s_%s_%s' %\
                   (data['shape_x'], data['shape_y'], data['width'], data['height'], data['border'])
        path = os.path.join(settings.BASE_DIR, 'static')
        path = os.path.join(path, filename)
        rate = main_process(data, path)
        content = {
            'rate': rate,
            'file_name': 'static/%s.png' % filename,
        }
        return HttpResponse(json.dumps(content), content_type="application/json")
    else:
        return render(request, 'use_rate.html')









