# encoding=utf-8
import json
import os
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myApi.single_use_rate import main_process, use_rate_data_is_valid
from myApi.package_function import main_process as production_rate
from django_api import settings
from myApi.models import Userate


def home_page(request):
    return render(request, 'index.html')


@csrf_exempt
def single_use_rate(request):
    if request.method == 'POST':
        data = request.POST
        res = use_rate_data_is_valid(data)
        if res['error']:
            return render(request, 'use_rate.html', res)
        else:
            # 命名规则：x_y_width_height_border.png
            filename = '%s_%s_%s_%s_%s_%s' %\
                       (data['shape_x'], data['shape_y'], data['width'], data['height'], data['border'], data['is_texture'])
            use_rate = Userate.objects.filter(name=filename)
            if use_rate:
                content = {
                    'rate': use_rate[0].rate,
                    'file_name': 'static/%s.png' % filename,
                }
                return HttpResponse(json.dumps(content), content_type="application/json")
            else:
                path = os.path.join(settings.BASE_DIR, 'static')
                path = os.path.join(path, filename)
                rate = main_process(data, path)
                content = {
                    'rate': rate,
                    'file_name': 'static/%s.png' % filename,
                }
                new_use_rate = Userate(name=filename, rate=rate)
                new_use_rate.save()
                return HttpResponse(json.dumps(content), content_type="application/json")
    else:
        return render(request, 'use_rate.html')


def single_use_rate_demo(request):
    if request.method == 'POST':
        data = request.POST
        # 判断数据是否合适
        res = use_rate_data_is_valid(data)
        if res['error']:
            return render(request, 'use_rate_demo.html', res)
        else:
            # 命名规则：x_y_width_height_border.png
            filename = '%s_%s_%s_%s_%s_%s_%s' %\
                       (data['shape_x'], data['shape_y'], data['width'], data['height'],
                        data['border'], data['is_texture'], data['is_vertical'])
            use_rate = Userate.objects.filter(name=filename)

            if use_rate:
                info = u'组件：%s x %s ，板材尺寸：%s x %s' % (
                    data['shape_x'], data['shape_y'], data['width'], data['height'])
                content = {
                    'rate': use_rate[0].rate,
                    'file_name': 'static/%s.png' % filename,
                    'info': info,
                }
                return render(request, 'use_rate_demo.html', content)
            else:
                path = os.path.join(settings.BASE_DIR, 'static')
                path = os.path.join(path, filename)
                rate = main_process(data, path)
                info = u'组件：%s x %s ，板材尺寸：%s x %s' % (
                    data['shape_x'], data['shape_y'], data['width'], data['height'])
                content = {
                    'rate': rate,
                    'file_name': 'static/%s.png' % filename,
                    'info': info,
                }
                new_use_rate = Userate(name=filename, rate=rate)
                new_use_rate.save()
                return render(request, 'use_rate_demo.html', content)
    else:
        return render(request, 'use_rate_demo.html')


@csrf_exempt
def product_use_rate(request):
    if request.method == 'POST':
        filename = str(time.time()).split('.')[0]
        path = os.path.join(settings.BASE_DIR, 'static')
        path = os.path.join(path, filename)
        res = production_rate(request.POST, pathname=path)
        if res['error']:
            return render(request, 'product_use_rate.html', res)
        else:
            content = {
                'rate': res['rate_list'],
                'prefix_name': 'static/%s.png' % filename,
            }
            return HttpResponse(json.dumps(content), content_type="application/json")
    else:
        return render(request, 'product_use_rate.html')


@csrf_exempt
def product_use_rate_demo(request):
    if request.method == 'POST':
        filename = str(time.time()).split('.')[0]
        path = os.path.join(settings.BASE_DIR, 'static')
        path = os.path.join(path, filename)
        res = production_rate(request.POST, pathname=path)
        if res['error']:
            return render(request, 'product_use_rate_demo.html', res)
        else:
            content = {
                'rates': res['rate_list'],
                'prefix_name': 'static/%s.png' % filename,
            }
            return render(request, 'product_use_rate_demo.html', content)
    else:
        return render(request, 'product_use_rate_demo.html')

