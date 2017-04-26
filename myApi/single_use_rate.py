# encoding=utf8
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time

"""
计算一个矩形组件的使用率
输入组件尺寸和板材尺寸
返回使用率和排列方式
"""


def use_rate(use_place, width, height):
    total_use = 0
    for b_x, b_y, w, h in use_place:
        total_use += w * h
    print(total_use)
    return float(total_use)/width/height * 100


def draw_the_pic(position, border_position, width, height, border=0, filename=None):
    fig1 = Figure(figsize=(12, 6))
    FigureCanvas(fig1)
    ax1 = fig1.add_subplot(111)
    output_obj = list()
    # color_list = ['red', 'blue', 'yellow', 'black']
    index_v = 0
    for v in position:
        output_obj.append(patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='m', label='Label',
                                            facecolor='blue', lw=border))
        index_v += 1
    for v in border_position:
        output_obj.append(patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='m', label='Label',
                                            facecolor='red', lw=border))
        index_v += 1
    for p in output_obj:
        ax1.add_patch(p)
    ax1.set_xlim(0, width)
    ax1.set_ylim(0, height)
    fig1.savefig('%s.png' % filename, dpi=200)


def is_enough(shape, place):
    width = place[2] - place[0]
    height = place[3] - place[1]
    if shape[0] <= width and shape[1] <= height:
        return True, place
    else:
        for v_p in empty_place:
            if v_p != place:
                if v_p[0] == place[0] and v_p[2] == place[2] and (v_p[1] == place[3] or v_p[3] == place[1]):
                    if v_p[3] > place[3]:
                        new_place = (place[0], place[1], place[2], v_p[3])
                        i_v_p = empty_place.index(v_p)
                        i_p = empty_place.index(place)
                        empty_place.remove(v_p)
                        empty_place.remove(place)
                        empty_place.append(new_place)
                        res, r_place = is_enough(shape, new_place)
                        if not res:
                            empty_place.remove(new_place)
                            empty_place.insert(i_v_p, v_p)
                            empty_place.insert(i_p, place)
                        return res, r_place
                    else:
                        new_place = (place[0], place[3], place[2], v_p[1])
                        i_v_p = empty_place.index(v_p)
                        i_p = empty_place.index(place)
                        empty_place.remove(v_p)
                        empty_place.remove(place)
                        empty_place.append(new_place)
                        res, r_place = is_enough(shape, new_place)
                        if not res:
                            empty_place.remove(new_place)
                            empty_place.insert(i_v_p, v_p)
                            empty_place.insert(i_p, place)
                        return res, r_place
                if v_p[1] == place[1] and v_p[3] == place[3] and (v_p[0] == place[2] or v_p[2] == place[0]):
                    if v_p[2] > place[2]:
                        new_place = (place[0], place[1], v_p[2], place[3])
                        i_v_p = empty_place.index(v_p)
                        i_p = empty_place.index(place)
                        empty_place.remove(v_p)
                        empty_place.remove(place)
                        empty_place.append(new_place)
                        res, r_place = is_enough(shape, new_place)
                        if not res:
                            empty_place.remove(new_place)
                            empty_place.insert(i_v_p, v_p)
                            empty_place.insert(i_p, place)
                        return res, r_place
                    else:
                        new_place = (v_p[0], place[1], place[2], place[3])
                        i_v_p = empty_place.index(v_p)
                        i_p = empty_place.index(place)
                        empty_place.remove(v_p)
                        empty_place.remove(place)
                        empty_place.append(new_place)
                        res, r_place = is_enough(shape, new_place)
                        if not res:
                            empty_place.remove(new_place)
                            empty_place.insert(i_v_p, v_p)
                            empty_place.insert(i_p, place)
                        return res, r_place
        return False, None


def tidy_empty_place(em_place):
    for i in range(len(em_place)-1,0,-1):
        for j in range(0, i):
            # 比较Y的开始值
            if em_place[j][1] > em_place[j+1][1]:
                em_place[j], em_place[j+1] = em_place[j+1], em_place[j]

    return em_place


def update_empty_place(shape, place, border):
    # 添加放置位置, 判断是否为边界,添加边框
    if place[0] != 0 and place[1] != 0:
        # 不在左边和底部, 两边加一个BORDER/2 的矩形
        border_list.append((place[0] - border, place[1], border, shape[1]))
        border_list.append((place[0] - border, place[1] - border, shape[0] + border, border))
    elif place[0] != 0:
        border_list.append((place[0] - border, place[1], border, shape[1]))
    elif place[1] != 0:
        border_list.append((place[0], place[1] - border, shape[0], border))

    situation.append((place[0], place[1], shape[0], shape[1]))
    # 新建临时list , 储存新的空白地方, 空白增加边框的面积
    tmp_empty_place = list()
    # begin:
    begin_x = place[0] + shape[0] + border
    begin_y = place[1] + shape[1] + border
    # 拆分空余的地方
    if begin_x < place[2]:
        tmp_empty_place.append((begin_x, place[1], place[2], shape[1]+place[1]+border))
    if begin_y < place[3]:
        tmp_empty_place.append((place[0], begin_y, shape[0]+place[0]+border, place[3]))
    if begin_x < place[2] and begin_y < place[3]:
        tmp_empty_place.append((begin_x, begin_y, place[2], place[3]))

    # 保持从左到右,从下到上,找符合的空间
    for tmp_place in tmp_empty_place[::-1]:
        empty_place.insert(0, tmp_place)


def only_one(shape_x, shape_y, width, height):
    # 拆分矩形,找适合的矩形, 坐标表示矩形:(0,0,30,40) = begin(0,0), end(30,40)
    # 初始化空白可填充部分
    # 如果长宽一样，就忽略，若不等，判断怎么放，先看能不能整好，然后看剩余多少
    # x 是短 ， y是长
    if shape_x > shape_y:
        shape_x, shape_y = shape_y, shape_x
    shape = (shape_x, shape_y)

    wx = width % shape_x
    wy = width % shape_y
    hx = height % shape_x
    hy = height % shape_y

    model = 'y2w'
    # 大优先
    if wy == 0:
        model = 'y2w'
    if wx == 0:
        model = 'x2w'
    if hy == 0:
        model = 'x2w'
    if hx == 0:
        model = 'y2w'

    if model == 'y2w':
        shape = (shape[1], shape[0])
    return shape


def main_process(data, filename):
    global empty_place, situation, border_list
    shape_x = int(data['shape_x'])
    shape_y = int(data['shape_y'])
    WIDTH = int(data['width'])
    HEIGHT = int(data['height'])
    BORDER = float(data['border'])
    empty_place = list()
    situation = list()
    border_list = list()
    print(empty_place)
    # 整理图形
    shape = only_one(shape_x, shape_y, WIDTH, HEIGHT)

    is_done = True
    can_change = True
    empty_place.append((0, 0, WIDTH, HEIGHT))
    # 需要放的个数
    total_num = 0
    print(empty_place)
    while is_done or can_change:
        # 从左到右,从下到上,找符合的空间
        # 整理有空的位置排序
        if not is_done and can_change:
            shape = (shape[1], shape[0])
            can_change = False
        is_done = False
        tmp_empty_place = tidy_empty_place(empty_place)
        for place in tmp_empty_place:
            res, tmp_p = is_enough(shape, place)
            if res:
                # 拆分空白地方
                empty_place.remove(tmp_p)
                # 更新空余地方
                update_empty_place(shape, tmp_p, BORDER)
                total_num += 1
                print(total_num)
                is_done = True
                can_change = True
                break
        print is_done, can_change

    draw_the_pic(situation, border_list, WIDTH, HEIGHT, filename=filename)

    return use_rate(situation, WIDTH, HEIGHT)
