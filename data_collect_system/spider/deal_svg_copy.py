import bs4
import numpy
from svg.path import parse_path


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
    # print(numpy_element)
    # numpy_element = numpy_element.transpose()


    return numpy_element

def get_attr(element, attr, default_value = ""):
    if element.has_attr(attr):
        return element[attr]
    else:
        return default_value

def parse_fill(fill):
    if fill[0] != "#":
        print("I cannot handle this situation!!!")
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



def deal_rect(rect_group, svg_width, svg_height):
    elements = []
    for element in rect_group:
        # this_type = type.index("rect")
        type = [1.0, 0, 0]
        fill = get_attr(element, "fill", "#000")
        color = parse_fill(fill)
        width = float(get_attr(element, "width"))
        height = float(get_attr(element, "height"))
        x = float(get_attr(element, "x", 0))
        y = float(get_attr(element, "y", 0))
        x_left = x
        x_right = x + width
        y_up = y
        y_down = y + height
        position = cal_relative_position(width, height, x_left, x_right, y_up, y_down, svg_width, svg_height)
        # position = [width/svg_width, height/svg_height, x_left/svg_width, x_right/]
        opacity = float(get_attr(element, "opacity", 1))
        quantity0 = float(get_attr(element, "quantity0", 0))
        quantity1 = float(get_attr(element, "quantity1", 0))
        category0 = int(get_attr(element, "category0", 0))
        category1 = int(get_attr(element, "categoty1", 0))
        category0_array = [0,0,0,0,0, 0,0,0,0,0]
        category0_array[category0] = 1
        category1_array = [0,0,0,0,0, 0,0,0,0,0]
        category1_array[category1] = 1

        this_element = type + position + color + [opacity] + [quantity0, quantity1] + category0_array + category1_array

        # type 3 + position 6 + color 3 + opacity 1 + quantity0 1 + quantity1 1 + category0 10 + categoty1 10
        # 35

        elements.append(this_element)
    return elements

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

# print(parse_svg("../data_collect_system/spider/svg/0001.svg"))
