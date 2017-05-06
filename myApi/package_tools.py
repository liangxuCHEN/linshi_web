# encoding=utf8
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches


def use_rate(use_place, width, height):
    total_use = 0
    for b_x, b_y, w, h in use_place:
        total_use += w * h
    return float(int(float(total_use)/width/height * 100))/100


def draw_many_pics(positions, width, height, path, border=0):
    i_p = 0
    for position in positions:
        fig1 = Figure(figsize=(12, 6))
        FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111)
        output_obj = list()
        for v in position:
            output_obj.append(patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='m', facecolor='blue', lw=border))

        for p in output_obj:
            ax1.add_patch(p)
        ax1.set_xlim(0, width)
        ax1.set_ylim(0, height)
        fig1.savefig('%s_pic%d.png' % (path, i_p), dpi=200)
        i_p += 1


def can_merge_place(place_v1, place_v2):
    """
    判断两个空间是否能合并
    :param place_v1:
    :param place_v2:
    :return:
    可以合并，返回True 和 合并的新空间
    不可以，返回False 和 None
    """
    if place_v1[0] == place_v2[0] and place_v1[2] == place_v2[2] and (
                    place_v1[1] == place_v2[3] or place_v1[3] == place_v2[1]):
        if place_v1[3] > place_v2[3]:
            return True, (place_v2[0], place_v2[1], place_v2[2], place_v1[3])
        else:
            return True, (place_v2[0], place_v2[3], place_v2[2], place_v1[1])
    if place_v1[1] == place_v2[1] and place_v1[3] == place_v2[3] and (
                    place_v1[0] == place_v2[2] or place_v1[2] == place_v2[0]):
        if place_v1[2] > place_v2[2]:
            return True, (place_v2[0], place_v2[1], place_v1[2], place_v2[3])
        else:
            return True, (place_v1[0], place_v2[1], place_v2[2], place_v2[3])
    return False, None


def tidy_shape(shapes, shapes_num, texture, vertical):
    """
    默认是竖直放置, shape_x 是 宽 ， shape_y 是 长, 由大到小排序
    当有纹理并且是竖直摆放的时候，要选择矩形
    :param shapes: 记录各矩形的长宽
    :param shapes_num:  记录矩形的数量
    :param texture:  是否有纹理，0：没有，1：有
    :param vertical: 摆放方式，当有纹理的时候有用，0:水平摆放，1:竖直摆放
    :return:
    """
    tmp_list = list()
    if texture == 1 and vertical == 0:
        # 这里是水平放置
        for shape in shapes:
            shape_x = shape[0]
            shape_y = shape[1]
            if shape_x < shape_y:
                shape_x, shape_y = shape_y, shape_x
            tmp_list.append((shape_x, shape_y))
    else:
        for shape in shapes:
            shape_x = shape[0]
            shape_y = shape[1]
            if shape_x > shape_y:
                shape_x, shape_y = shape_y, shape_x
            tmp_list.append((shape_x, shape_y))

    # 根据矩形的面积有大到小排列，
    for i in range(len(tmp_list) - 1, 0, -1):
        for j in range(0, i):
            if tmp_list[j][1] * tmp_list[j][0] < tmp_list[j + 1][1] * tmp_list[j + 1][0]:
                tmp_list[j], tmp_list[j + 1] = tmp_list[j + 1], tmp_list[j]
                shapes_num[j], shapes_num[j + 1] = shapes_num[j + 1], shapes_num[j]

    # 结合数量，合并成一个新的队列
    index_shape = 0
    new_list = list()
    for shape in tmp_list:
        for num in range(0, shapes_num[index_shape]):
            new_list.append(shape)
        index_shape += 1
    return new_list, tmp_list


def draw_one_pic(positions, rates, title, width, height, path, border=0):
    i_p = 0
    num = len(positions)
    fig_height = num * 4
    fig1 = Figure(figsize=(8, fig_height))
    fig1.suptitle(title, fontsize=12, fontweight='bold')
    FigureCanvas(fig1)
    code = 100 * num + 11
    for position in positions:
        ax1 = fig1.add_subplot(code + i_p, aspect='equal')
        ax1.set_title('the rate: %f' % rates[i_p])
        output_obj = list()
        # color_list = ['red', 'blue', 'yellow', 'black']
        for v in position:
            output_obj.append(patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='m', facecolor='blue', lw=border))

        for p in output_obj:
            ax1.add_patch(p)

        ax1.set_xlim(0, width)
        ax1.set_ylim(0, height)
        i_p += 1

    fig1.savefig('%s.png' % path, dpi=200)
