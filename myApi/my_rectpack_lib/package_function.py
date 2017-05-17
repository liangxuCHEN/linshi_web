# encoding=utf8

from package_tools import use_rate, draw_one_pic, tidy_shape, is_valid_empty_section, find_the_same_position
from packer import newPacker
import guillotine as guillotine
import packer as packer

"""
给定数量的产品，求混排的最优结果
输出板材的数量和排版结果
"""


def get_shape_data(shape_data, bin_data, num_pic=1):
    """
    shape_data 输入是一个字符串如：板A 400 500 30;板A 130 250 10;板B 800 900 5;
    bin_data : A 三聚氰胺板-双面胡桃木哑光(J2496-4)25mm 2430 1210 1 0;B 三聚氰胺板-双面白布纹哑光（18mm） 2430 1210 0 0;
    没有空格，然后通过处理，返回一个字典

    :param data:
    :return:
    {'板A': {
            'shape_list': [(400,500), (130,250)]  一个矩形的长宽
            'shape_num':  [30,10] 对应矩形的数量
            'name': 三聚氰胺板-双面胡桃木哑光(J2496-4)25mm
            'width': 2430,
            'height': 1210,
            'is_texture': 0     是否有纹理，有纹理不能旋转 0：没有， 1：有
            'is_vertical': 0    当在有纹理情况下的摆放方向  0：水平摆放，1：竖直摆放
        },
    '板B': {
            'shape_list': [(800, 900)]  一个矩形的长宽
            'shape_num': [5] 对应矩形的数量
            'name': 三聚氰胺板-双面白布纹哑光（18mm）
            'width': 2430,
            'height': 1210,
            'is_texture': 1
            'is_vertical': 0
        }
    }


    """
    data_dict = {}
    bin_list = list()
    # 板材信息
    bins = bin_data.split(';')
    for abin in bins:
        try:
            res = abin.split(' ')
            if len(res) == 6:
                bin_type = res[0]
                name = res[1]
                b_w = res[2]
                b_h = res[3]
                is_t = res[4]
                is_v = res[5]
            elif len(res) == 5:
                bin_type = res[0]
                name = res[1]
                b_w = res[2]
                b_h = res[3]
                is_t = res[4]
                is_v = 0
            else:
                return {
                    'error': True,
                    'info': u'板木数据输入有误，缺少参数，至少5个'
                }

            b_w = int(b_w)
            b_h = int(b_h)
            is_t = int(is_t)
            is_v = int(is_v)
            if b_w < b_h:
                b_w, b_h = b_h, b_w

            if bin_type in bin_list:
                return {
                    'error': True,
                    'info': u'板木数据输入有误，有重复的版木数据'
                }

            data_dict[bin_type] = {
                'shape_list': list(),
                'shape_num': list()
            }
            data_dict[bin_type]['name'] = name
            data_dict[bin_type]['width'] = b_w
            data_dict[bin_type]['height'] = b_h
            data_dict[bin_type]['is_texture'] = is_t
            data_dict[bin_type]['is_vertical'] = is_v
            bin_list.append(bin_type)

        except:
            return {
                'error': True,
                'info': u'板木数据输入的格式不对, 一组数据之间用空格, 数据之间用分号<;>, 最后结尾不要放分号<;>, 而且要用英文标点'
            }

    # 组件尺寸信息
    shapes = shape_data.split(';')
    for shape in shapes:
        try:
            bin_type, x, y, num = shape.split(' ')
            x = int(x)
            y = int(y)
            num = int(num) * num_pic
            if bin_type in bin_list:
                data_dict[bin_type]['shape_list'].append((x, y))
                data_dict[bin_type]['shape_num'].append(num)
            else:
                return {
                    'error': True,
                    'info': u'矩形数据输入有误，没有对应的板木类别'
                }
        except:
            return {
                'error': True,
                'info': u'矩形数据输入的格式不对, 一组数据之间用空格, 数据之间用分号<;>, 最后结尾不要放分号<;>, 而且要用英文标点'
            }
        if x > data_dict[bin_type]['width'] or y > data_dict[bin_type]['width']:
            return {'error': True, 'info': u'输入尺寸数值错误，组件尺寸必须小于板材'}
        if x <= 0 or y <= 0:
            return {'error': True, 'info': u'输入尺寸数值错误，尺寸输入值必须大于零'}
        if num <= 0:
            return {'error': True, 'info': u'输入矩形数量错误，输入值必须大于零'}

    return {'data':data_dict, 'error': False}


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
    avg_rate = int((total_rate / len(all_positions) * 10000)) / 10000.0
    return avg_rate, all_positions


def find_best_solution(all_shapes, border, bin_width, bin_height, is_texture):
    # 所有算法组合
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
                                             border=border))

    # Add the rectangles to packing queue
    for my_pack in list_packer:
        for r in all_shapes:
            my_pack.add_rect(*r)

    # Add the bins where the rectangles will be placed
    NUM = 500
    for my_pack in list_packer:
        my_pack.add_bin(bin_width, bin_height, NUM)

    # Start packing
    best_rate = 0.0
    min_bin_num = NUM
    best_solution = None
    best_packer = 0
    index_packer = 0
    best_empty_positions = None
    max_empty_ares = 0
    for my_pack in list_packer:
        my_pack.pack()
        avg_rate, tmp_solution = output_res(my_pack.rect_list(), bin_width, bin_height)
        bin_num = len(tmp_solution)
        # 余料判断
        tmp_empty_position, empty_ares = is_valid_empty_section(my_pack.get_sections())
        if min_bin_num > bin_num or (avg_rate > best_rate and bin_num == min_bin_num) or (
                        bin_num == min_bin_num and avg_rate == best_rate and empty_ares > max_empty_ares):
            best_solution = tmp_solution
            min_bin_num = bin_num
            best_rate = avg_rate
            best_empty_positions = tmp_empty_position
            max_empty_ares = empty_ares
            best_packer = index_packer
        index_packer += 1

    return best_solution, best_empty_positions, best_rate, best_packer


def main_process(input_data, pathname):
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
        BORDER = float(input_data['border'])    # 间隙
    except ValueError:
        return {'error': True, 'info': u'输入类型错误，输入值必须是数值类型'}

    if BORDER < 0:
        return {'error': True, 'info': u'输入尺寸数值错误，组件间隙不能小于零'}

    # 矩形参数
    data = get_shape_data(input_data['shape_data'], input_data['bin_data'])
    if data['error']:
        return {'error': True, 'info': data['info']}

    statistics_data = []  # 汇总数据
    # 每一种板木排版一次
    for bin_type, values in data['data'].items():
        all_shapes, shape_list, num_shapes = tidy_shape(
            values['shape_list'], values['shape_num'], values['is_texture'], values['is_vertical'])
        best_solution, empty_positions, best_rate, best_packer = find_best_solution(
            all_shapes, BORDER, values['width'], values['height'], values['is_texture'])

        # 计算使用率
        rate_list = list()
        for s in best_solution:
            r = use_rate(s, values['width'], values['height'])
            rate_list.append(r)
        title = u'平均利用率: %s' % str(best_rate)
        # 把排版结果显示并且保存
        # 返回唯一的排版列表，以及数量
        same_bin_list = find_the_same_position(best_solution)

        draw_one_pic(best_solution, rate_list, values['width'], values['height'],
                     path=pathname+bin_type, border=1, num_list=same_bin_list, title=title,
                     shapes=shape_list, empty_positions=empty_positions)

        # 保存统计信息
        statistics_data.append({
            'error': False,
            'rate': best_rate,
            'num_sheet': len(best_solution),
            'detail': detail_text(shape_list, best_solution, same_bin_list),
            'num_shape': str(num_shapes)[1:-1],
            'same_bin_list': str(same_bin_list)[1:-1],
            'sheet_num_shape': str([len(s) for s in best_solution])[1:-1],
            'rates': str(rate_list)[1:-1],
            'sheet': u'%s %d x %d' % (values['name'], values['width'], values['height']),
            'name': values['name'],
            'bin_type': bin_type,
            'pic_url': pathname+bin_type+'.png',
            'empty_sections': detail_empty_sections(empty_positions)
        })

    return {'statistics_data': statistics_data, 'error': False}


def detail_text(shape_list, situation_list, num_list):
    output_text = ''

    for shape in shape_list:
        output_text += '%d,%d' % (shape[1], shape[0])
        id_situation = 0
        for situation in situation_list:
            if num_list[id_situation] != 0:
                # 统计每块板有多少个shape一样的图形
                count = 0
                for position in situation:
                        if shape == (position[2], position[3]) or shape == (position[3], position[2]):
                            count += 1

                output_text += ',%d' % count
            id_situation += 1
        # 拆分用‘;’
        output_text += ';'

    return output_text[:-1]


def detail_empty_sections(empty_sections):
    counts = {}

    for e_places in empty_sections:
        for e_p in e_places:
            c_id = "%dx%d" % (max(e_p[2], e_p[3]), min(e_p[2], e_p[3]))
            if c_id in counts.keys():
                counts[c_id]['num'] += 1
            else:
                counts[c_id] = {
                    'num': 1,
                    'ares': e_p[2] * e_p[3]
                }
    text = ""
    for key, value in counts.items():
        text += "%s %d %d;" % (key, value['num'], value['ares'])
    return text[:-1]

