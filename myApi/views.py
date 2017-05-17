# encoding=utf-8
import json
import os
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from myApi.my_rectpack_lib.single_use_rate import main_process, use_rate_data_is_valid
from myApi.my_rectpack_lib.package_function import main_process as production_rate
from myApi.my_rectpack_lib.package_tools import del_same_data
from django_api import settings
from myApi.models import Userate, ProductRateDetail, Project


def home_page(request):
    return render(request, 'index.html')


@csrf_exempt
def single_use_rate(request):
    if request.method == 'POST':
        data = request.POST
        res = use_rate_data_is_valid(data)
        if res['error']:
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            # 命名规则：x_y_width_height_border.png
            filename = '%s_%s_%s_%s_%s_%s_%s' %\
                       (data['shape_x'], data['shape_y'], data['width'], data['height'],
                        data['border'], data['is_texture'], data['is_vertical'])
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
                res = main_process(data, path)
                # 出错就返回错误
                if res['error']:
                    return HttpResponse(json.dumps(res), content_type="application/json")

                content = {
                    'rate': res['rate'],
                    'file_name': 'static/%s.png' % filename,
                }
                new_use_rate = Userate(name=filename, rate=res['rate'])
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
                res = main_process(data, path)
                # 出错就返回错误
                if res['error']:
                    return render(request, 'use_rate_demo.html', res)

                info = u'组件：%s x %s ，板材尺寸：%s x %s' % (
                    data['shape_x'], data['shape_y'], data['width'], data['height'])
                content = {
                    'rate': res['rate'],
                    'file_name': 'static/%s.png' % filename,
                    'info': info,
                }
                new_use_rate = Userate(name=filename, rate=res['rate'])
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
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            try:
                product = ProductRateDetail(
                    sheet_name=res['sheet'],
                    num_sheet=res['num_sheet'],
                    avg_rate=res['rate'],
                    rates=res['rates'],
                    detail=res['detail'],
                    num_shape=res['num_shape'],
                    sheet_num_shape=res['sheet_num_shape'],
                    pic_url='static/%s.png' % filename,
                    doc_url='static/%s_desc.txt' % filename,
                )
                product.save()
                product_id = product.id
            except:
                product_id = None
            content = {
                'rates': res['rate'],
                'picture': 'static/%s.png' % filename,
                'describe': 'static/%s_desc.txt' % filename,
                'desc_url': 'product/%d' % product_id if product_id is not None else '',
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
        results = production_rate(request.POST, pathname=path)
        if results['error']:
            return render(request, 'product_use_rate_demo.html', results)
        else:
            # try:
            # save project
            project = Project(comment=request.POST['project_comment'])
            project.save()
            # save product
            for res in results['statistics_data']:
                product = ProductRateDetail(
                    sheet_name=res['sheet'],
                    num_sheet=res['num_sheet'],
                    avg_rate=res['rate'],
                    rates=res['rates'],
                    detail=res['detail'],
                    num_shape=res['num_shape'],
                    sheet_num_shape=res['sheet_num_shape'],
                    pic_url='static/%s%s.png' % (filename, res['bin_type']),
                    same_bin_list=res['same_bin_list'],
                    empty_sections=res['empty_sections']
                )
                product.save()
                project.products.add(product)
            project.save()
            project_id = project.id
            # except:
            #     project_id = None
            content = {
                'shape_data': request.POST['shape_data'],
                'bin_data': request.POST['bin_data'],
                'project_id': project_id
            }
            return render(request, 'product_use_rate_demo.html', content)
    else:
        return render(request, 'product_use_rate_demo.html')


def cut_detail(request, p_id):
    product = ProductRateDetail.objects.get(pk=p_id)
    content = {
        'sheet_name': product.sheet_name,
        'num_sheet': product.num_sheet,
        'avg_rate': product.avg_rate,
        'pic_url': product.pic_url,
    }

    if product is not None:
        # 合并相同排版
        same_bin_list = product.same_bin_list.split(',')
        content['bin_num'] = del_same_data(same_bin_list, same_bin_list)
        # 图形的数量
        num_shape = product.num_shape.split(',')

        # 图形的每个板数量
        details = product.detail.split(';')
        detail_list = list()
        i_shape = 0
        total_shape = 0

        for detail in details:
            detail_dic = {}
            tmp_list = detail.split(',')
            detail_dic['width'] = tmp_list[0]
            detail_dic['height'] = tmp_list[1]
            detail_dic['num_list'] = tmp_list[2:]
            tmp_sum = 0
            for x in range(2, len(tmp_list)):
                tmp_sum += int(tmp_list[x]) * int(content['bin_num'][x-2])

            detail_dic['total'] = tmp_sum
            total_shape += int(num_shape[i_shape])
            i_shape += 1
            detail_list.append(detail_dic)

        content['details'] = detail_list
        content['col_num'] = len(detail_list[0]['num_list']) + 3

        # 每块板的总图形数目
        content['sheet_num_shape'] = del_same_data(same_bin_list, product.sheet_num_shape.split(','))
        content['sheet_num_shape'].append(total_shape)
        # 每块板的利用率
        content['rates'] = del_same_data(same_bin_list, product.rates.split(','))
        content['rates'].append(content['avg_rate'])

        # 余料信息
        empty_sections = product.empty_sections.split(';')
        content['empty_sections'] = []
        for e_section in empty_sections:
            name, num, ares = e_section.split(' ')
            content['empty_sections'].append({
                'name': name,
                'num': num,
                'ares': ares
            })

        return render(request, 'cut_detail_desc.html', content)
    else:
        return render(request, 'cut_detail_desc.html', {'error': u'没有找到，请检查ID'})


def project_detail(request, p_id):
    project = Project.objects.get(pk=p_id)
    if project is None:
        return render(request, 'cut_detail_desc.html', {'error': u'没有找到，请检查ID'})
    bin_list = project.products.all()
    content = {
        'created': project.created,
        'comment': project.comment,
        'bin_list': list()
    }
    for abin in bin_list:
        content['bin_list'].append({
            'bin_id': abin.id,
            'sheet_name': abin.sheet_name,
            'num_sheet': abin.num_sheet,
            'avg_rate': abin.avg_rate,
            'pic_url': abin.pic_url,
        })
    return render(request, 'project_detail.html', content)


class ProjectIndexView(generic.ListView):
    model = Project
    template_name = "project_index.html"
    context_object_name = "project_list"