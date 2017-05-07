# encoding=utf8
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches


def use_rate(use_place, width, height):
    total_use = 0
    for b_x, b_y, w, h in use_place:
        total_use += w * h
    return int(float(total_use)/width/height * 100)/100.0


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
            return True, (place_v2[0], place_v1[1], place_v2[2], place_v2[3])
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
    for i in range(len(tmp_list), 1, -1):
        for j in range(0, i-1):
            # 长度大于宽带，比较方式就是看长的边长，若长相等，看宽
            if tmp_list[j][1] < tmp_list[j + 1][1] or (
                            tmp_list[j][1] == tmp_list[j + 1][1] and tmp_list[j][0] < tmp_list[j + 1][0]):
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


def draw_one_pic(positions, rates, title, width, height, path, border=0, shapes=None):
    # 多个图像需要处理

    if shapes is not None:
        # 写一个空白文档，说明情况
        with open('%s_desc.txt' % path, 'w') as f:
            f.write('# : %d x %d \n' % (width, height))
            for i_shape in range(0, len(shapes)):
                f.write('%d : %d x %d \n' % (i_shape, shapes[i_shape][0], shapes[i_shape][1]))

        # 返回唯一的排版列表，以及数量
        num_list = find_the_same_position(positions,shapes)
    else:
        # 单个图表
        num_list = [1]
    i_p = 0     # 记录板材索引
    i_pic = 1   # 记录图片的索引
    num = len(positions)
    fig_height = num * 4
    fig1 = Figure(figsize=(8, fig_height))
    fig1.suptitle(title, fontsize=12, fontweight='bold')
    fig1.subplots_adjust(bottom=0.1, top=0.95)
    FigureCanvas(fig1)

    for position in positions:
        if num_list[i_p] != 0:
            ax1 = fig1.add_subplot(num, 1, i_pic, aspect='equal')
            i_pic += 1
            ax1.set_title('the rate: %s, Qty: %d' % (str(rates[i_p]), num_list[i_p]))
            output_obj = list()
            for v in position:
                output_obj.append(patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='m', facecolor='blue', lw=border))

            for p in output_obj:
                ax1.add_patch(p)
                # 计算显示位置
                if shapes is not None:
                    rx, ry = p.get_xy()
                    cx = rx + p.get_width() / 2.0
                    cy = ry + p.get_height() / 2.0
                    # 找到对应的序号
                    p_id = -1
                    if (p.get_width(), p.get_height()) in shapes:
                        p_id = shapes.index((p.get_width(), p.get_height()))
                    if (p.get_height(), p.get_width()) in shapes:
                        p_id = shapes.index((p.get_height(), p.get_width()))

                    ax1.annotate(p_id, (cx, cy), color='w', weight='bold',
                                 fontsize=6, ha='center', va='center')

            ax1.set_xlim(0, width)
            ax1.set_ylim(0, height)
        i_p += 1

    fig1.savefig('%s.png' % path)


def find_the_same_position(positions, shapes):
    # 初始化，默认每个都不一样，数量都是1
    num_list = [1] * len(positions)
    for i in range(len(positions)-1, 0, -1):
        for j in range(0, i):
            if positions[i] == positions[j] and num_list[j] != 0:
                num_list[i] += 1
                num_list[j] = 0
    return num_list