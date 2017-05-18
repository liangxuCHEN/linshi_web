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
    data_dict = {}     # 返回结果
    bin_list = list()  # 板木种类
    # 板材信息
    bins = bin_data.split(';')
    for abin in bins:
        try:
            # 输入参数有可能6个或5个
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

    return {'data': data_dict, 'error': False}


def output_res(all_rects, width, height):
    """
    整理算法返回的结果,是它适合画图排版，返回使用率，组件排列坐标
    :param all_rects: 算法返回的结果[(bin_id, x, y, w, h, rid)]
    :param width:  板材的尺寸
    :param height: 板材的尺寸
    :return:
    avg_rate:
    all_positions: [[(x,y,w,h), (x,y,w,h)],[(x,y,w,h)],[(x,y,w,h)]]
    """
    # TODO：如果板材尺寸不一样，这个方法不适应，需要修改
    rects = list()
    all_positions = list()

    # 整理结果,不同板的分开到不同的队列
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


def find_best_solution(all_shapes, border, bin_width, bin_height, is_texture, packer_id_list=None):
    """
    遍历各种算法找最佳的方案
    :param all_shapes: 矩形数据
    :param border: 缝隙
    :param bin_width: 板材长
    :param bin_height: 板材宽
    :param is_texture: 是否有纹理
    :param packer_id_list:[0,4,50] :只选用特定算法
    :return:
    best_solution: 组件的坐标
    best_empty_positions: 余料坐标
    best_rate: 方案的平均利用率
    best_packer: 方案（算法）的ID
    """
    # 所有算法组合
    # 当排版的组件非常多，需要提高反应速度可以选择BFF（首次适应）算法
    # bin_algos = [packer.PackingBin.BBF, packer.PackingBin.BFF]
    # 这里选择BBF（最佳适应）算法，可以较好保留大块空余地方。
    bin_algos = [packer.PackingBin.BBF]
    # 这里是选择板材切割算法guillotine,
    # 选择区域标准：BAF:找最佳面积适应, BLSF:最佳长边适应值, BSSF:最佳短边边适应值
    # 分割剩余区域标准：SLAS:剩余短轴分割,LAS:长轴分割,MAXAS:剩余大面积分割:,LLAS:剩余长轴分割,MINAS:剩余小面积分割,
    # TODO：如果是激光切割，可以使用maxrects算法
    pack_algos = [guillotine.GuillotineBafLas, guillotine.GuillotineBafMaxas,
                  guillotine.GuillotineBafMinas, guillotine.GuillotineBafSlas, guillotine.GuillotineBafLlas,
                  guillotine.GuillotineBlsfLas, guillotine.GuillotineBlsfMaxas,
                  guillotine.GuillotineBlsfMinas, guillotine.GuillotineBlsfSlas, guillotine.GuillotineBlsfLlas,
                  guillotine.GuillotineBssfLas, guillotine.GuillotineBssfMaxas,
                  guillotine.GuillotineBssfMinas, guillotine.GuillotineBssfSlas, guillotine.GuillotineBssfLlas]
    # 矩形排序规则,由大到小:
    # SORT_AREA:面积, SORT_LSIDE:长边, SORT_SSIDE:短边, SORT_PERI:周长
    sort_algos = [packer.SORT_AREA, packer.SORT_LSIDE, packer.SORT_SSIDE, packer.SORT_PERI]

    # 按照不同算法规则添加对象
    list_packer = list()
    for bin_alog in bin_algos:
        for pack_alog in pack_algos:
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
    # TODO: 添加出入参数，选择可以使用的板材尺寸和数量
    NUM = 5000
    for my_pack in list_packer:
        my_pack.add_bin(bin_width, bin_height, NUM)

    # Start packing
    # 初始化参数
    best_rate = 0.0
    min_bin_num = NUM
    best_solution = None
    best_packer = 0
    index_packer = 0
    best_empty_positions = None
    max_empty_ares = 0

    # 是否选定算法
    if packer_id_list is not None:
        new_packer_list = list()
        for i_packer in packer_id_list:
            new_packer_list.append(list_packer[i_packer])
        list_packer = new_packer_list

    for my_pack in list_packer:
        my_pack.pack()
        avg_rate, tmp_solution = output_res(my_pack.rect_list(), bin_width, bin_height)
        bin_num = len(tmp_solution)
        # 余料判断
        tmp_empty_position, empty_ares = is_valid_empty_section(my_pack.get_sections())
        # 找最优解
        if min_bin_num > bin_num or (avg_rate > best_rate and bin_num == min_bin_num) or (
                        bin_num == min_bin_num and avg_rate == best_rate and empty_ares > max_empty_ares):
            best_solution = tmp_solution
            min_bin_num = bin_num
            best_rate = avg_rate
            best_empty_positions = tmp_empty_position
            max_empty_ares = empty_ares
            best_packer = index_packer
        index_packer += 1

    # 找到真实的id
    if packer_id_list is not None:
        best_packer = packer_id_list[best_packer]

    return best_solution, best_empty_positions, best_rate, best_packer


def main_process(input_data, pathname):
    """
    给出矩形的大小和数量和板材编号
    板材的编号，尺寸，纹理信息
    返回按不同板材分类输出每一种板材需要多少块，以及每一块的利用率
    :param data: 所有输入数据
    :param pathname: 输出排列的数据的文档路径
    :return:
    reslut: 保存报告的ID
    """
    # 输入值合理性判断
    try:
        # 板材尺寸
        BORDER = float(input_data['border'])    # 间隙
    except ValueError:
        return {'error': True, 'info': u'输入类型错误，输入值必须是数值类型'}

    if BORDER < 0:
        return {'error': True, 'info': u'输入尺寸数值错误，组件间隙不能小于零'}

    # 算法参数
    algo_list = None
    if 'algo_list' in input_data.keys():
        try:
            if len(input_data['algo_list']) > 0:
                algo_list = [int(x) for x in input_data.getlist('algo_list')]
        except:
            return {'error': True, 'info': u'算法选择错误'}

    # 矩形参数
    data = get_shape_data(input_data['shape_data'], input_data['bin_data'])
    if data['error']:
        return {'error': True, 'info': data['info']}

    statistics_data = []  # 汇总报告
    # 每一种板木排版一次
    for bin_type, values in data['data'].items():
        all_shapes, shape_list, num_shapes = tidy_shape(
            values['shape_list'], values['shape_num'], values['is_texture'], values['is_vertical'])
        best_solution, empty_positions, best_rate, best_packer = find_best_solution(
            all_shapes, BORDER, values['width'], values['height'], values['is_texture'], packer_id_list=algo_list)

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
            'sheet': u'%s %d x %d 选用算法<%d>' % (values['name'], values['width'], values['height'], best_packer),
            'name': values['name'],
            'bin_type': bin_type,
            'pic_url': pathname + bin_type+'.png',
            'empty_sections': detail_empty_sections(empty_positions),
            'algo_id': best_packer,
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

