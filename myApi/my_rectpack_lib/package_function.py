# encoding=utf8

from package_tools import use_rate, draw_one_pic, tidy_shape, is_valid_empty_section
from packer import newPacker
import guillotine as guillotine
import packer as packer

"""
给定数量的产品，求混排的最优结果
输出板材的数量和排版结果
"""


def find_model(shape_x, shape_y, place, border):
    """
    拆分矩形,找适合的矩形, place坐标表示空余空间:(0,0,30,40) = begin(0,0), end(30,40)
    判断怎么放，横竖组合，然后看剩余多少，找出剩余空间最少的方案
    :param shape_x: 矩形边长
    :param shape_y: 矩形边长
    :param place: 空余空间
    :param border: 图形间间隙
    :return:
    solution: 排列的方案
    {
    'x': 1    x 边长 排多少个
    'y': 3    y 边长 排多少个
    'empty': 根据这个方案，得到的剩余空间面积
    'model': 根据空间的长或者宽的边来排列 w：长边排列，h：宽边排列
    'length': 选取空间的边的长度
    'place': 空间的坐标
    }
    """
    # 初始化空白可填充部分
    width = place[2] - place[0]
    height = place[3] - place[1]
    # 先找出两种模式的最佳解
    solution_1 = cal_rate_num(shape_x, shape_y, width, height, border)
    solution_1['model'] = 'w'
    solution_1['place'] = place
    solution_2 = cal_rate_num(shape_x, shape_y, height, width, border)
    solution_2['model'] = 'h'
    solution_2['place'] = place
    # 比较两种模式，找出最优解
    if solution_1['empty'] > solution_2['empty']:
        if solution_2['model'] == 'w':
            solution_2['length'] = height
        else:
            solution_2['length'] = width
        return solution_2
    else:
        if solution_1['model'] == 'w':
            solution_1['length'] = height
        else:
            solution_1['length'] = width
        return solution_1


def get_shape_data(data, width, num_pic=1):
    """
    输入是一个字符串如：400 500 30;130 250 10;800 900 5;
    没有空格，然后通过处理，返回两个队列

    :param data:
    :return:
    shape_list: [(400,500), (130,250),(900,800)]  一个矩形的长宽
    shape_num: [30,10,5] 对应矩形的数量
    """
    shape_list = list()
    shape_num = list()
    shapes = data.split(';')
    for shape in shapes:
        try:
            x, y, num = shape.split(' ')
            x = int(x)
            y = int(y)
            num = int(num) * num_pic
            shape_list.append((x, y))
            shape_num.append(num)
        except:
            return {
                'error': True,
                'info': u'输入的格式不对, 一组数据之间用空格, 数据之间用分号<;>, 最后结尾不要放分号<;>, 而且要用英文标点'
            }
        if x > width or y > width:
            return {'error': True, 'info': u'输入尺寸数值错误，组件尺寸必须小于板材'}
        if x <= 0 or y <= 0:
            return {'error': True, 'info': u'输入尺寸数值错误，尺寸输入值必须大于零'}
        if num <= 0:
            return {'error': True, 'info': u'输入矩形数量错误，输入值必须大于零'}

    return {'shape_list': shape_list, 'shape_num': shape_num, 'error': False}


def output_res(all_rects, width, height):
    rects = list()
    all_positions = list()

    is_new_bin = 0
    for rect in all_rects:
        b, x, y, w, h, rid = rect
        if b == is_new_bin:
            rects.append((x, y, w, h))
        else:
            is_new_bin = b
            all_positions.append(rects)
            rects = list()
            rects.append((x, y, w, h))

    all_positions.append(rects)

    # 计算使用率
    rate_list = list()
    total_rate = 0
    for s in all_positions:
        r = use_rate(s, width, height)
        total_rate += r
        rate_list.append(r)
    avg_rate = int((total_rate / len(all_positions) * 100)) / 100.0
    return avg_rate, all_positions


def main_process(data, pathname):
    """
    给出矩形的大小和数量，以及板材的尺寸，返回需要多少块板材，以及每一块板材的利用率
    :param data: 所有输入数据
    :param pathname: 输出排列的数据的文档路径
    :return:
    reslut: [0.9, 0.88,,0.78] 返回每块板的利用率
    """
    # 输入值合理性判断
    try:
        # 板材尺寸
        WIDTH = int(data['width'])
        HEIGHT = int(data['height'])
        BORDER = float(data['border'])    # 间隙
    except ValueError:
        return {'error': True, 'info': u'输入类型错误，输入值必须是数值类型'}

    if WIDTH <= 0 or HEIGHT <= 0:
        return {'error': True, 'info': u'输入尺寸数值错误，尺寸输入值必须大于零'}
    # 防止输入长宽位置错，自动调整
    if WIDTH < HEIGHT:
        WIDTH, HEIGHT = HEIGHT, WIDTH

    if BORDER < 0:
        return {'error': True, 'info': u'输入尺寸数值错误，组件间隙不能小于零'}

    # 矩形参数
    shape_result = get_shape_data(data['shape_data'], WIDTH)
    if shape_result['error']:
        return {'error': True, 'info': shape_result['info']}
    else:
        SHAPE = shape_result['shape_list']
        SHAPE_NUM = shape_result['shape_num']

    is_texture = int(data['is_texture'])    # 是否有纹理，有纹理不能旋转 0：没有， 1：有
    is_vertical = int(data['is_vertical'])  # 当在有纹理情况下的摆放方向  0：水平摆放，1：竖直摆放

    # 整理数据，矩形从大到小排列，结合数量，得到一个总的需要排列的矩形列表 all_shapes
    # 结合纹理和横竖排列，返回矩形列表 shape_list
    all_shapes, shape_list, shape_num = tidy_shape(SHAPE, SHAPE_NUM, is_texture, is_vertical)

    bin_alogs = [packer.PackingBin.BBF, packer.PackingBin.BFF]
    pack_alogs = [guillotine.GuillotineBafLas, guillotine.GuillotineBafMaxas,
                  guillotine.GuillotineBafMinas, guillotine.GuillotineBafSlas, guillotine.GuillotineBafLlas,
                  guillotine.GuillotineBlsfLas, guillotine.GuillotineBlsfMaxas,
                  guillotine.GuillotineBlsfMinas, guillotine.GuillotineBlsfSlas, guillotine.GuillotineBlsfLlas,
                  guillotine.GuillotineBssfLas, guillotine.GuillotineBssfMaxas,
                  guillotine.GuillotineBssfMinas, guillotine.GuillotineBssfSlas, guillotine.GuillotineBssfLlas]
    sort_algos = [packer.SORT_AREA, packer.SORT_LSIDE, packer.SORT_SSIDE, packer.SORT_PERI]

    list_packer = list()
    for bin_alog in bin_alogs:
        for pack_alog in pack_alogs:
            for sort_algo in sort_algos:
                list_packer.append(newPacker(bin_algo=bin_alog,
                                             pack_algo=pack_alog,
                                             sort_algo=sort_algo,
                                             rotation=not is_texture,
                                             border=BORDER))

    # Add the rectangles to packing queue
    for my_pack in list_packer:
        for r in all_shapes:
            my_pack.add_rect(*r)

    # Add the bins where the rectangles will be placed
    NUM = 99999
    for my_pack in list_packer:
        my_pack.add_bin(WIDTH, HEIGHT, NUM)

    # Start packing
    best_rate = 0
    min_bin_num = NUM
    best_solution = None
    best_packer = 0
    index_packer = 0
    for my_pack in list_packer:
        my_pack.pack()
        avg_rate, tmp_solution = output_res(my_pack.rect_list(), WIDTH, HEIGHT)
        bin_num = len(tmp_solution)
        if min_bin_num > bin_num or (avg_rate > best_rate and bin_num == min_bin_num):
            best_solution = tmp_solution
            min_bin_num = bin_num
            best_rate = avg_rate
            best_packer = index_packer
        index_packer += 1

    # 计算使用率
    rate_list = list()
    total_rate = 0
    for s in best_solution:
        r = use_rate(s, WIDTH, HEIGHT)
        total_rate += r
        rate_list.append(r)
    avg_rate = int((total_rate / min_bin_num * 100)) / 100.0
    title = 'Average rate : %s' % str(avg_rate)

    # 余料判断
    empty_positions = is_valid_empty_section(list_packer[best_packer].get_sections(), shape_list)

    # 把排版结果显示并且保存
    draw_one_pic(best_solution, rate_list, title, WIDTH, HEIGHT, path=pathname, border=1,
                 shapes=shape_list, shapes_num=shape_num, avg_rate=avg_rate, empty_positions=empty_positions)

    result = {
        'error': False,
        'rate': avg_rate,
        'num_sheet': len(best_solution),
        'detail': detail_text(shape_list, best_solution),
        'num_shape': str(shape_num)[1:-1],
        'sheet_num_shape': str([len(s) for s in best_solution])[1:-1],
        'rates': str(rate_list)[1:-1],
        'sheet': '%d x %d' % (WIDTH, HEIGHT),
    }
    return result


def get_empty_situation(empty_places, min_shape, border):
    """
    把空白的地方转换成画图的格式，如果空白地方最小图形都放不下，就不要了
    :param empty_places:
    :param min_shape:
    :return:
    """
    situation_list = list()
    for place in empty_places:
        solution = find_model(min_shape[0], min_shape[1], place, border)
        if solution['x'] != 0 or solution['y'] != 0:
            situation_list.append((
                place[0],
                place[1],
                place[2] - place[0],
                place[3] - place[1]
            ))
    return situation_list


def detail_text(shape_list, situation_list):
    output_text = ''
    for shape in shape_list:
        output_text += '%d,%d' % (shape[1], shape[0])

        for situation in situation_list:
            # 统计每块板有多少个图形
            count = 0
            for position in situation:
                if shape == (position[2], position[3]) or shape == (position[3], position[2]):
                    count += 1

            output_text += ',%d' % count
        # 拆分用‘;’
        output_text += ';'

    return output_text[:-1]
