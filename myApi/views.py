# encoding=utf-8
import json
import os

from django.http import Http404
from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
# from myApi.single_use_rate import main_process
from django_api import settings
from myApi.models import Userate


def home_page(request):
    return render(request, 'index.html')


@csrf_exempt
def single_use_rate(request):
    if request.method == 'POST':
        data = request.POST
        # 命名规则：x_y_width_height_border.png
        filename = '%s_%s_%s_%s_%s' %\
                   (data['shape_x'], data['shape_y'], data['width'], data['height'], data['border'])
        use_rate = Userate.objects.get(name=filename)
        if use_rate:
            content = {
                'rate': use_rate.rate,
                'file_name': 'static/%s.png' % filename,
            }
            return HttpResponse(json.dumps(content), content_type="application/json")

        path = os.path.join(settings.BASE_DIR, 'static')
        path = os.path.join(path, filename)
        # rate = main_process(data, path)
        rate = 91.87
        content = {
            'rate': rate,
            'file_name': 'static/%s.png' % filename,
        }
        new_use_rate = Userate(name=filename, rate=rate)
        new_use_rate.save()
        return HttpResponse(json.dumps(content), content_type="application/json")
    else:
        return render(request, 'use_rate.html')









