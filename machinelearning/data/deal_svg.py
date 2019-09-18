import bs4
import numpy
import json
import os
# from svg.path import parse_path
import sys

current_url = os.path.dirname(__file__)
extracter_url = os.path.abspath(os.path.join(current_url, '../../extracter/'))
sys.path.append(extracter_url)

from extract_svg import parse_unknown_svg

type = ["circle", "rect", "line", "path"]

def parse_svg_full(filename):
    file_handle = open(filename)
    soup = bs4.BeautifulSoup(file_handle.read(), "html5lib")
    svg = soup.select("svg")
    svg_height = float(svg[0]["height"])
    svg_width = float(svg[0]["width"])

    # print("width is:  ", svg[0]["height"])
    # print("Height is: ", svg[0]["width"])
    # rect_group = soup.select("rect")
    # deal_rect(rect_group, svg_width, )

    circle_group = soup.select("circle")
    if len(circle_group) > 0:
        elements = deal_circle(circle_group, svg_width, svg_height)

    rect_group = soup.select("rect")
    if len(rect_group) > 0:
        elements = deal_rect(rect_group, svg_width, svg_height)

    # deal_path(path_group, svg_width, svg_height)
    # length = len(a)
    # path = soup.select("path")
    # path_group = soup.select("path")
    length = len(elements)
    # for i in range(length, 7):
    #     elements.append([0,0,0,0, 0,0,0,0, 0,0,0,0])

    numpy_element = numpy.asarray(elements)
    print(numpy_element)
    numpy_element = numpy_element.transpose()


    return numpy_element
def parse_svg(filename):
    file_handle = open(filename)
    soup = bs4.BeautifulSoup(file_handle.read(), "html5lib")
    svg = soup.select("svg")
    svg_height = float(svg[0]["height"])
    svg_width = float(svg[0]["width"])

    # print("width is:  ", svg[0]["height"])
    # print("Height is: ", svg[0]["width"])
    # rect_group = soup.select("rect")
    # deal_rect(rect_group, svg_width, )

    circle_group = soup.select("circle")
    if len(circle_group) > 0:
        elements = deal_circle(circle_group, svg_width, svg_height)

    rect_group = soup.select("rect")
    if len(rect_group) > 0:
        elements, id_array = deal_rect(rect_group, svg_width, svg_height)

    # deal_path(path_group, svg_width, svg_height)
    # length = len(a)
    # path = soup.select("path")
    # path_group = soup.select("path")
    length = len(elements)
    for i in range(length, 7):
        elements.append([0,0,0,0, 0,0,0,0, 0,0,0,0])
    numpy_element = numpy.asarray(elements)
    # print(numpy_element)
    numpy_element = numpy_element.transpose()


    return numpy_element

def get_rect_attr(rect, attr, default_value):
    if attr in rect.keys():
        return rect[attr]
    else:
        return default_value

def get_list(rect):
    cate_choice_number = 15
    type = [1, 0, 0]
    position = [rect['width'], rect['height'], rect['left'], rect['right'], rect['up'], rect['down']]
    color = rect['fill']
    opacity = [rect['opacity']]
    quantity = [get_rect_attr(rect, 'q0', 0), get_rect_attr(rect, 'q1', 0)]
    cate0_array = [0 for i in range(cate_choice_number)]
    cate1_array = [0 for i in range(cate_choice_number)]
    ordi0_array = [0 for i in range(cate_choice_number)]
    ordi1_array = [0 for i in range(cate_choice_number)]
    cate0_choice = get_rect_attr(rect, 'c0', 0)
    cate1_choice = get_rect_attr(rect, 'c1', 0)
    ordi0_choice = get_rect_attr(rect, 'o0', 0)
    ordi1_choice = get_rect_attr(rect, 'o1', 0)
    cate0_array[cate0_choice] = 1
    cate1_array[cate1_choice] = 1
    ordi0_array[ordi0_choice] = 1
    # ordi1_array[ordi1_choice] = 1
    list = type + position + color + opacity + quantity + cate0_array + cate1_array + ordi0_array
    # print(f'The attribute of each rectangle is {len(list)}')
    return list

def getCircleList(data):
    cate_choice_number = 15
    type = [0,0,0]
    position = [2*data['r'], 2*data['r'], data['q0'], data['q1'], data['q0'], data['q1']]
    color = [0,0,0,1]
    quantity = [data['q0'], data['q1']]
    co= [0 for i in range(4*cate_choice_number)]
    list = type + position + color + quantity + co
    return list

    # width/svg_width, height/svg_height, left/svg_width, right/svg_width, up/svg_height, down/svg_height]
def getDataPointList(data):
    cate_choice_number = 15
    eps = 1e-5
    type = [0, 0, 1]
    position = [eps, eps, data['point_x'], data['point_y'], data['point_x'], data['point_y']]
    color = data['color']
    opacity = [1] #!!!!!!!!!TODO
    quantity = [data['q0'], 0]
    cate0_array = [0 for i in range(cate_choice_number)]
    cate1_array = [0 for i in range(cate_choice_number)]
    ordi0_array = [0 for i in range(cate_choice_number)]
    ordi1_array = [0 for i in range(cate_choice_number)]
    cate0_choice = data['c0']
    ordi0_choice = data['o0']
    cate0_array[cate0_choice] = 1
    ordi0_array[ordi0_choice] = 1
    list = type + position + color + opacity + quantity + cate0_array + cate1_array + ordi0_array
    return list

def parse_svg_string(svg_string, min_element_num = 7):
    important_rects, data, soup = parse_unknown_svg(svg_string)
    if 'vis_type' in data and data['vis_type']=="load_scatter_line_plot":
        elements = [getDataPointList(dp) for dp in important_rects]
        id_array = [i for i in range(len(important_rects))]
    elif 'vis_type' in data and data['vis_type']=="load_scatter_plot":
        elements = [getCircleList(c) for c in important_rects]
        id_array = [i for i in range(len(important_rects))]
    else:
        elements = []
        for rect in important_rects:
            list = get_list(rect)
            elements.append(list)
        if len(important_rects) < min_element_num:
            for i in range(len(important_rects), min_element_num):
                elements.append([0 for i in range(len(elements[0]))])
        print("I want to see the important rects")
        print(important_rects)
        id_array = [rect['id'] for rect in important_rects]
        print(id_array)
        if sum(id_array) == - len(id_array):
            id_array = [i for i in range(len(id_array))]
        print(f"The id array is {id_array}")
    return numpy.asarray(elements), id_array


def parse_svg_string_new(str):
    soup = bs4.BeautifulSoup(str, "html5lib")
    svg = soup.select("svg")
    svg_height = float(svg[0]["height"])
    svg_width = float(svg[0]["width"])

    # print("width is:  ", svg[0]["height"])
    # print("Height is: ", svg[0]["width"])
    # rect_group = soup.select("rect")
    # deal_rect(rect_group, svg_width, )

    circle_group = soup.select("circle")
    if len(circle_group) > 0:
        elements = deal_circle(circle_group, svg_width, svg_height)

    id_array = []
    rect_group = soup.select(".elements")
    if len(rect_group) > 0:
        elements, id_array = deal_rect_real(rect_group, svg_width, svg_height)

    # deal_path(path_group, svg_width, svg_height)
    # length = len(a)
    # path = soup.select("path")
    # path_group = soup.select("path")
    length = len(elements)
    if length < 7:
        pad = [0 for i in range(len(elements[0]))]
        for i in range(length, 7):
            elements.append(pad)
    # for i in range(length, 7):
    #     elements.append([0,0,0,0, 0,0,0,0, 0,0,0,0])
    numpy_element = numpy.asarray(elements)
    # print(numpy_element)
    # numpy_element = numpy_element.transpose()


    return numpy_element, id_array


# simple edition for #xxxxxx
def get_attr(element, attr, default_value = ""):
    if element.has_attr(attr):
        return element[attr]
    else:
        return default_value

def parse_fill(fill):
    if fill[0] != "#":
        print("I cannot handle this color parse situation!!!")
        return
    if len(fill) == 7:
        r = int(fill[1:3], 16)/255.0;
        g = int(fill[3:5], 16)/255.0;
        b = int(fill[5:7], 16)/255.0;
        # print(r, g, b)
        return [r, g, b]
    elif len(fill) == 7:
        r = int(fill[1:2], 16)/15.0;
        g = int(fill[2:3], 16)/15.0;
        b = int(fill[3:4], 16)/15.0;
        # print(r, g, b)
        return [r, g, b]
    return [0,0,0]

def deal_rect_real(rect_group, svg_width, svg_height):
    elements = []
    id_array = []
    max_q = 0
    for element in rect_group:
        # this_type = type.index("rect")
        type = [1.0, 0, 0]
        fill = get_attr(element, "fill", "#000")
        color = parse_fill(fill)
        width = float(get_attr(element, "width"))
        height = float(get_attr(element, "height"))
        x = float(get_attr(element, "x", 0))
        y = float(get_attr(element, "y", 0))
        id_array.append(int(get_attr(element, "id", -1)))
        x_left = x
        x_right = x + width
        y_up = y
        y_down = y + height
        position = cal_relative_position(width, height, x_left, x_right, y_up, y_down, svg_width, svg_height)
        # position = [width/svg_width, height/svg_height, x_left/svg_width, x_right/]
        opacity = float(get_attr(element, "opacity", 1))
        quantity0 = max(float(get_attr(element, "q_major", 0)), float(get_attr(element, "q0", 0)))
        if max_q < quantity0:
            max_q = quantity0
        quantity1 = float(get_attr(element, "q_second", 0))
        category0 = int(get_attr(element, "c0", 0))
        category1 = int(get_attr(element, "c1", 0))
        ordinal0 = int(get_attr(element, 'o0', 0))
        # print(category0)
        # print(category1)
        category0_array = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0 ]
        category0_array[category0] = 1
        category1_array = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0 ]
        category1_array[category1] = 1
        ordinal0_array = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0 ]
        ordinal0_array[ordinal0] = 1

        this_element = type + position + color + [opacity] + [quantity0, quantity1] + category0_array + category1_array + ordinal0_array

        # type 3 + position 6 + color 3 + opacity 1 + quantity0 1 + quantity1 1 + category0 10 + categoty1 10
        # 35

        elements.append(this_element)
    for element in elements:
        element[13] = element[13] / max_q
    return elements, id_array


def cal_relative_position(width, height, left, right, up, down, svg_width, svg_height):
    return [width/svg_width, height/svg_height, left/svg_width, right/svg_width, up/svg_height, down/svg_height]

def deal_circle(circle_group, svg_width, svg_height):
    elements = []
    for element in circle_group:
        type = [0,1.0,0]
        # this_type = type.index("circle")
        fill = element["fill"]
        color = parse_fill(fill)
        r = float(element["r"])
        cx = float(element["cx"])
        cy = float(element["cy"])
        x_left = cx - r;
        x_right = cx + r;
        y_up = cy - r;
        y_down = cy + r;
        width = 2 * r;
        height = 2 * r;
        position = [width/svg_width, height/svg_height, x_left/svg_width, x_right/svg_width, y_up/svg_height, y_down/svg_height]

        this_element = type + position + color
        elements.append(this_element)
        # print(r,cx,cy)
    return elements

def deal_path(path_group, svg_width, svg_height):
    for element in path_group:
        d = element["d"]
        path = parse_path(d)

        print(parse_path(d))
        print(path[0])

    #
    # def open_svg_etree(filename):
    #     xml = ET.parse(filename)
    #

def get_B_numpy(sentences, id_array):
    B_list = []
    for id in id_array:
        choice = []
        for sentence in sentences:
            selected = 0
            compare_id = sentence['compare_id']
            focus_id = sentence['focus_id']
            if id in focus_id:
                selected = 2
            elif id in compare_id:
                selected = 1
            this_choice = [0,0,0]
            this_choice[selected] = 1
            choice = choice + this_choice
        B_list.append(choice)
    length = len(B_list)
    if length < 7:
        pad = [0 for i in range(len(B_list[0]))]
        for i in range(length, 7):
            B_list.append(pad)
    B_numpy = numpy.asarray(B_list)
    return B_numpy
def get_scatter_B_order_numpy(sentences, id_array):
    type_order = ['cluster', 'outlier']
    B_list = [[] for i in range(len(id_array))]
    for type in type_order:
        this_sentence = {}
        for sentence in sentences:
            if sentence['type'] == type:
                this_sentence = sentence
        if len(this_sentence) == 0:
            for i in range(len(id_array)):
                B_list[i].extend([0, 0, 0])
        else:
            focus_id = this_sentence['focus_id']
            compare_id = this_sentence['compare_id']
            for i, id in enumerate(id_array):
                id_choice = [0, 0, 0]
                if id in focus_id:
                    id_choice[2] = id_choice[2] + 1
                elif id in compare_id:
                    id_choice[1] = id_choice[1] + 1
                else:
                    id_choice[0] = id_choice[0] + 1
                B_list[i].extend(id_choice)
    length = len(B_list)
    if length < 7:
        pad = [0 for i in range(len(B_list[0]))]
        for i in range(length, 7):
            B_list.append(pad)
    B_numpy = numpy.asarray(B_list)
    print(B_numpy.shape)
    return B_numpy

def get_B_order_numpy(sentences, id_array):
    type_order = ["compare_trend", "compare_ave", "sum_trend", 'all_trend', 'local_trend', 'local_sum_trend']
    B_list = [[] for i in range(len(id_array))]
    for type in type_order:
        this_sentence = {}
        for sentence in sentences:
            if sentence['type'] == type:
                this_sentence = sentence
        if len(this_sentence) == 0:
            for i in range(len(id_array)):
                B_list[i].extend([0, 0, 0])
        else:
            focus_id = this_sentence['focus_id']
            compare_id = this_sentence['compare_id']
            for i, id in enumerate(id_array):
                id_choice = [0, 0, 0]
                if id in focus_id:
                    id_choice[2] = id_choice[2] + 1
                elif id in compare_id:
                    id_choice[1] = id_choice[1] + 1
                else:
                    id_choice[0] = id_choice[0] + 1
                B_list[i].extend(id_choice)
    length = len(B_list)
    if length < 7:
        pad = [0 for i in range(len(B_list[0]))]
        for i in range(length, 7):
            B_list.append(pad)
    B_numpy = numpy.asarray(B_list)
    print(B_numpy.shape)
    return B_numpy




def deal_with_json(file_name):
    with open(file_name) as f:
        datum = json.load(f)
    svg_string = datum['svg_string']
    sentences = datum['sentences']
    A_numpy, id_array =  parse_svg_string(svg_string)
    B_numpy = get_B_order_numpy(sentences, id_array)
    return A_numpy, B_numpy

def generate_data(file_dir, out_dir, opt = 'train'):
    out_dir_A = os.path.join(out_dir, f'{opt}A')
    out_dir_B = os.path.join(out_dir, f'{opt}B')
    os.system(f'mkdir -p {out_dir_A}')
    os.system(f'mkdir -p {out_dir_B}')
    file_list = os.listdir(file_dir)
    for i, file_name in enumerate(file_list):
        print(file_name)
        file_json = os.path.join(file_dir, file_name)
        # print(file_name)
        A_numpy, B_numpy = deal_with_json(file_json)

        # print(A_numpy)
        # print(B_numpy)
        # # print(file_name)
        # print(A_numpy.shape)
        # print(B_numpy.shape)
        # assert(A_numpy.shape[1] == 45)
        out_trainA = os.path.join(out_dir_A, file_name[:-5] + '.npy')
        out_trainB = os.path.join(out_dir_B, file_name[:-5] + '.npy')
        # B_numpy = B_numpy[:,0: 3 * output_sentence_number]
        # if (B_numpy.shape[1] < 3 * output_sentence_number):
        #     B_numpy = numpy.pad(B_numpy,((0, 0),(0, 3 * output_sentence_number - B_numpy.shape[1])), "constant")
        numpy.save(out_trainA, A_numpy)
        numpy.save(out_trainB, B_numpy)
        # print(A_numpy.shape)
        # print(B_numpy.shape)
        #
        if i % 100 == 0:
            print(i)

if __name__ == '__main__':
    generate_data('../../user_data/20180918_full_ocq_rule/', '../datasets/20190918_full_ocq_rule/')
    # file_json = '../../server/user_collected_data/cq_try_2018_08_27_21_48_37_337642.json'
    # A_numpy, B_numpy = deal_with_json(file_json)
    # print(A_numpy)
    # print(A_numpy.shape)
    # print(B_numpy.shape)
    #
    # file_name = '../../server/user_collected_data/2018_08_20_14_38_19_6309872.json'
    # data, B_list = deal_with_json(file_name)
    # print(data)
    # print(B_list)
    # print(B_numpy.shape)
    # print(data.shape)



# print(parse_svg("../data_collect_system/spider/svg/0001.svg"))
