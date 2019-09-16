import json
import bs4
# import os
import numpy
import re
from svgpathtools import parse_path, Line, disvg
import copy
# def get_attr_by_style(element):
    #
def is_number(s):
    try:
        float(s.replace(",", ""))
        return True
    except ValueError:
        pass
    return False

def try_convert_number(s):
    try:
        number = float(s.replace(",", ""))
        return number 
    except ValueError:
        pass
    return s

def parse_fill(fill):
    # print(fill)
    if type(fill)==list and len(fill)==3:
        return fill
    elif fill[0] != "#":
        print(f"I cannot handle this color {fill}")
        return [-100, -100, -100]
    elif len(fill) == 7:
        r = int(fill[1:3], 16)/255.0;
        g = int(fill[3:5], 16)/255.0;
        b = int(fill[5:7], 16)/255.0;
        # print(r, g, b)
        return [r, g, b]
    elif len(fill) == 4:
        r = int(fill[1:2], 16)/15.0;
        g = int(fill[2:3], 16)/15.0;
        b = int(fill[3:4], 16)/15.0;
        # print(r, g, b)
        return [r, g, b]
    return [0,0,0]

def get_attr(element, attr, default_value = ""):
    # 这是一个补丁
    if attr == "fill":
        if not element.has_attr(attr):
            for node in element.parents:
                if node.name == "g":
                    if node.has_attr(attr):
                        return node[attr]
        else:
            return parse_fill(element[attr])

    if attr == "text-anchor":
        if element.has_attr(attr):
            return element[attr]
            for node in element.parents:
                if node.name == "g":
                    if node.has_attr(attr):
                        return node[attr]
        return "start"


    elif element.has_attr(attr):
        if attr == "width" or attr == "height":
            if element[attr].endswith("%"):
                return default_value
        elif attr == "r":
            return re.sub("[a-z]", "", element[attr])
        elif attr == "font-size":
            font_size_value = element[attr]
            font_size_value = font_size_value.replace("px", '')
            if font_size_value.endswith("em"):
                relative_value = float(font_size_value.replace("em", "")) * 12
                return relative_value
            print(font_size_value)
            return font_size_value
        return element[attr]
    else:
        return default_value

def parse_transform(element):
    transform = get_attr(element, "transform", "translate(0,0)")
    x = transform.split("(")[1].split(",")[0]
    y = transform.split(",")[1].split(")")[0]
    x = float(x)
    y = float(y)

    return x, y

def get_font_size(element):
    if element.name == "text":
        font_size = float(get_attr(element, "font-size", 12))
    
        return font_size

def get_translate(element):
    if not element.has_attr("transform"):
        return 0,0
    transform = element['transform']
    if not transform.startswith("translate("):
        return 0,0
    xy = transform.replace("translate(", "").replace(")", "").split(",")

    x = float(xy[0])
    y = float(xy[1])
    print(f"deal with transform: {x} {y}")
    return x,y


def get_position(element, is_bbox = False):
    # print(element.name)
    if not is_bbox:
        if element.name == "rect":
            x = float(get_attr(element, "x", 0))
            y = float(get_attr(element, "y", 0))
            dx, dy = get_translate(element)
            x = x + dx
            y = y + dy
        elif element.name == "circle":
            x = float(get_attr(element, "cx", 0))
            y = float(get_attr(element, "cy", 0))
        elif element.name == "text":
            x = float(get_attr(element, "x", 0))
            y = float(get_attr(element, "y", 0))
    else:
        x = float(get_attr(element, "bbox_x", 0))
        y = float(get_attr(element, "bbox_y", 0))



    # print(f"Now, x: {x}, y: {y}")
    for parent in element.parents:
        if parent.name == "svg":
            break;
        if parent.name == "g":
            add_x, add_y = parse_transform(parent)
            x = x + add_x
            y = y + add_y

    # print(f"Now, x: {x}, y: {y}")
    return x, y


def get_rectangles(soup):
    rects = soup.select("rect")
    return rects

def judge_vertical(rects):
    width_array = {}
    height_array = {}
    for rect in rects:
        # print(f"width: {rect["width"]}, height {rect["height"]}")
        if rect["width"] in width_array.keys():
            width_array[rect["width"]] = width_array[rect["width"]] + 1
        else:
            width_array[rect["width"]] = 1

        if rect["height"] in height_array.keys():
            height_array[rect["height"]] = height_array[rect["height"]] + 1
        else:
            height_array[rect["height"]] = 1

    if len(width_array) > len(height_array):
        is_vertical =  False
    else:
        is_vertical = True
    return is_vertical, width_array, height_array

def get_important_rects(rects, dim, array):
    important_rects = []
    other_rects = []
    sorted_array = sorted(array.items(), key = lambda item:item[1], reverse = True)
    common_value = sorted_array[0][0]
    if common_value == 0:
        common_value = sorted_array[1][0]
    for rect in rects:
        if rect[dim] == common_value:
            important_rects.append(rect)
        elif rect["width"] > 0 and rect["height"] > 0 and rect["opacity"] > 0:
            other_rects.append(rect)
    return important_rects, other_rects

def parse_a_path(path):
    pathObj = parse_path(path["d"])
    for parent in path.parents:
        if parent.name == "svg":
            break
        if parent.name == "g":
            add_x, add_y = parse_transform(parent)
    path_attr = {
        "origin": path,
        "pathObj": pathObj,
        "sx": pathObj[0].start.real,
        "sy": pathObj[0].start.imag,
        "ex": pathObj[-1].end.real,
        "ey": pathObj[-1].end.imag,
        "rx": add_x,
        "ry": add_y,
        "color": get_attr(path, "stroke", "#000"),
    }
    # print("DEBUG", path_attr)
    return path_attr

def parse_a_circle(circle):
    radius = float(get_attr(circle, "r", 0))
    opacity = float(get_attr(circle, "opacity", 1))
    color = get_attr(circle, "fill", "#000")
    x, y = get_position(circle)
    left = x - radius
    right = x + radius
    up = y - radius
    down = y + radius
    width = 2 * radius
    height = 2 * radius
    circle_attr = {
        "origin"    : circle,
        "width"     : width,
        "height"    : height,
        "left"      : left,
        "right"     : right,
        "fill"      : color,
        "opacity"   : opacity,
        "x"         : x,
        "y"         : y,
        "up"        : up,
        "down"      : down,
        "r"         : radius
    }
    return circle_attr



def parse_a_rect(rect):
    width = float(get_attr(rect, "width", 0))
    height = float(get_attr(rect, "height", 0))
    opacity = float(get_attr(rect, "opacity", 1))
    color  = parse_fill(get_attr(rect, "fill", "#000"))


    # print(get_attr(rect, "fill", "#000"))
    # for debug
    value = float(get_attr(rect, "q0", 0))
    x, y = get_position(rect)
    left = x
    right = x + width
    up = y
    down = y + height
    rect_attr = {
        "origin": rect,
        "width": width,
        "height": height,
        "left": left,
        "right": right,
        "value": value,
        "fill": color,
        "opacity": opacity,
        "x": x,
        "y": y,
        "up": up,
        "down": down}
    return rect_attr

def parse_a_text(text):
    x, y = get_position(text)
    bbox_x, bbox_y = get_position(text, is_bbox = True)
    font_size = get_font_size(text)
    content = text.string.replace("\n", "").replace(" ", "")
    text_anchor = get_attr(text, "text-anchor", "start")
    # bbox_x = float(get_attr(text, "box_x"))
    # bbox_y = float(get_attr(text, "box_y"))
    # print("debug", text)
    # print(get_attr(text, "bbox_w"))
    bbox_w = float(get_attr(text, "bbox_w"))
    bbox_h = float(get_attr(text, "bbox_h"))

    print("bbox content", bbox_x, bbox_y, bbox_w, bbox_h)
    
    # print(content)
    return_content = {"x": x, "y": y, "content": content, "orgin":text, "font_size": font_size, "text_anchor": text_anchor, "bbox_x": bbox_x, "bbox_y": bbox_y, "bbox_w": bbox_w, "bbox_h": bbox_h}
    print("text content", return_content)
    return return_content


def extract_group(x_array, y_array, texts):

    x_array = sorted(x_array.items(), key = lambda item:item[1], reverse = True)
    y_array = sorted(y_array.items(), key = lambda item:item[1], reverse = True)
    # only for those larger than 1.
    x_important_array = [x for x in x_array if x[1] > 1]
    y_important_array = [y for y in y_array if y[1] > 1]

    print('DEBUG', x_array, y_array);

    x_groups = [{"x": x_set[0], "y": [{"position": text["y"], "content": text["content"].replace("\n", "").replace(" ", ""), "text_id": text["text_id"]} for text in texts if text["x"] == x_set[0]]} for x_set in x_important_array]
    y_groups = [{"y": y_set[0], "x": [{"position": text["x"], "content": text["content"].replace("\n", "").replace(" ", ""), "text_id": text["text_id"]} for text in texts if text["y"] == y_set[0]]} for y_set in y_important_array]
    for x_group in x_groups:
        x_group["distance"] = max([item["position"] for item in x_group["y"]]) - min([item["position"] for item in x_group["y"]])
    for y_group in y_groups:
        y_group["distance"] = max([item["position"] for item in y_group["x"]]) - min([item["position"] for item in y_group["x"]])
    return x_groups, y_groups


# 计算各种text的位置，
def count_text(texts):
    x_array = {}
    y_array = {}
    # calculate the x and y count number.
    for text in texts:
        if text["x"] in x_array.keys():
            x_array[text["x"]] = x_array[text["x"]] + 1
        else:
            x_array[text["x"]] = 1
        if text["y"] in y_array.keys():
            y_array[text["y"]] = y_array[text["y"]] + 1
        else:
            y_array[text["y"]] = 1
    return x_array, y_array


def calculate_axis(texts, force=1):
    # print("text_original_information", texts)
    x_array, y_array = count_text(texts)
    x_groups, y_groups = extract_group(x_array, y_array, texts)
    print("y_groups\n", y_groups)
    max_distance = max([y_group["distance"] for y_group in y_groups])
    def get_distance(item):
        item["distance"]
    y_group_order = sorted(y_groups, key = get_distance, reverse = True)
    X_axis = {}
    Y_axis = {}
    legend = {"type": "none", "x": []}
    for y_group in y_groups:
        if y_group["distance"] > max_distance * 0.5:
            X_axis = y_group
            max_distance = y_group["distance"]
            break
    if len(y_groups) > 1:
        for y_group in y_groups:
            if y_group["distance"] != max_distance:
                legend = y_group
                legend["type"] = "horizontal"
                break

    max_distance = max([x_group["distance"] for x_group in x_groups])
    for x_group in x_groups:
        if x_group["distance"] > max_distance * 0.5:
            Y_axis = x_group
            max_distance = x_group["distance"]
            break

    if len(x_groups) > 1:
        for x_group in x_groups:
            if x_group["distance"] != max_distance and len(legend["x"]) < len(x_group["y"]):
                legend = x_group
                legend["type"] = "vertical"
                break
    # for tmp in x_groups:
    #     print(":-(", tmp, "\n")
    if force==0:
        legend = x_groups[-1]
        legend["type"] = "vertical"
        return X_axis, Y_axis, legend
    return X_axis, Y_axis, legend

def parse_quantity_array(axis, vertical):
    if vertical == "vertical":
        num_array = axis["y"]
    else:
        num_array = axis["x"]
    value = [float(num_array[0]["content"].replace(",", "")), float(num_array[-1]["content"].replace(",", ""))]
    position = [float(num_array[0]["position"]), float(num_array[-1]["position"])]
    print(vertical, "v-p", value, position)
    b = 1
    def calculate_value_by_position(p):
        return (p - position[0]) * (value[1] - value[0]) / (position[1] - position[0]) + value[0]

    # for item in num_array:
        # print(f"the value we calculate is {calculate_value_by_position(item["position"])} and the original value is {item["content"]}")
    return calculate_value_by_position

# def add_value_to_rect(calculate_value, rects):

# def get_rects_important(rects):

def cal_distance(item1, item2):
    return numpy.sqrt(numpy.square(item1["x"] - item2["x"]) + numpy.square(item1["y"] - item2["y"]))

def parse_legend(legend, other_rects):
    if legend["type"] == "none":
        return []
    other_rects = [{"x": rect["left"] + rect["width"]/2, "y": rect["up"] + rect["height"]/2, "fill": rect["fill"]} for rect in other_rects]
    # print(f"other_rects: {other_rects}")
    if legend["type"] == "vertical":
        legend = [{"x": legend["x"], "y": item["position"], "content": item["content"]} for item in legend["y"]]
    elif legend["type"] == "horizontal":
        legend = [{"x": item["position"], "y": legend["y"], "content": item["content"]} for item in legend["x"]]
    for i, item in enumerate(legend):
        distances = [cal_distance(item, rect) for rect in other_rects]
        # print(f"distances: {distances}")
        rect_index = distances.index(min(distances))
        # print(f"the smallest index is {rect_index}")
        legend[i]["fill"] = other_rects[rect_index]["fill"]
    return legend

## TODO:  when have the legend, what can we do.

def cal_color_distance(fill_0, fill_1):
    diff = sum([numpy.square(fill_0[i] - fill_1[i]) for i in range(3)])
    return diff


def parse_color_legend(important_rects, legend):
    if len(legend) == 0:
        return important_rects
    for i, rect in enumerate(important_rects):
        diff_array = [cal_color_distance(item["fill"], rect["fill"]) for item in legend]
        # print(rect["fill"])
        # print(diff_array)
        match_index = diff_array.index(min(diff_array))
        important_rects[i]["second"] = match_index
        important_rects[i]["legend_index"] = match_index
    return important_rects

def get_main_second(main_dimension_list, second_dimension_list):
    if is_number(main_dimension_list[0]):
        main_dim = "o0"
        second_dim = "c0"
        data_type = "ocq"
    elif is_number(second_dimension_list[0]):
        main_dim = "c0"
        second_dim = "o0"
        data_type = "ocq"
    else:
        main_dim = "c0"
        second_dim = "c1"
        data_type = "ccq"

    return main_dim, second_dim, data_type

def get_elements(important_rects):
    elements_list = []
    print("important_rects: ", important_rects)
    for rect in important_rects:
        element = {}
        element['type'] = "rect"
        element["x"] = rect["x"]
        element['y'] = rect['y']
        element['w'] = rect['width']
        element['h'] = rect['height']
        element['legend_id'] = rect['legend_index']
        elements_list.append(element)

    return elements_list


def pack_data(important_rects, main_dimension_list, second_dimension_list):

    # for rect in important_rects:
    #     print(f"major: {rect["major"]}, second: {rect["second"]}, value: {rect["value"]}")
    for i in range(len(important_rects)):
        important_rects[i]["id"] = i



    main_dim, second_dim, data_type = get_main_second(main_dimension_list, second_dimension_list)


    

    data = {}
    data["data_type"] = data_type
    data_array = [{"id": rect["id"], main_dim: rect["major"], second_dim: rect["second"], "q0": int(rect["value"] * 100)/100.0} for rect in important_rects]
    data["data_array"] = data_array
    data[main_dim] = main_dimension_list
    data[second_dim] = second_dimension_list
    data["major"] = main_dim
    data["second"] = second_dim
    data["major_name"] = main_dim
    data["second_name"] = second_dim
    data["type"] = data_type
    data["unit"] = ""
    data["title"] = ""

    elements_list = get_elements(important_rects)
    print("elements_list: ", elements_list)
    # 获取元素列表
    data['elements'] = elements_list
    return data

def uniform_important_circle(data):
    q0 = [x['q0'] for x in data['data_array']]
    q1 = [x['q1'] for x in data['data_array']]
    min0 = min(q0)
    min1 = min(q1)
    max0 = max(q0)
    max1 = max(q1)
    circles = copy.deepcopy(data["data_array"])
    for c in circles:
        c['q0'] = (c['q0']-min0)/(max0-min0)
        c['q1'] = (c['q1']-min1)/(max1-min1)
    return circles

def uniform_important_datapoint(data):
    o0 = data["o0"]
    dps = copy.deepcopy(data["data_array"])
    q0 = [dp["q0"] for dp in dps]
    max_value = max(q0)
    min_value = min(q0)
    max_o = max(o0)
    min_o = min(o0)
    for i in range(len(dps)):
        dps[i]["q0"] = (dps[i]["q0"]-min_value)/(max_value-min_value)
        dps[i]["point_x"] = (o0[dps[i]["o0"]] - min_o)/(max_o-min_o)
        dps[i]["point_y"] = dps[i]["q0"]
    return dps

def uniform_important_elements(important_rects):
    top_most = 99999
    bottom_most = 0
    left_most = 99999
    right_most = 0
    for rect in important_rects:
        if rect["left"] < left_most:
            left_most = rect["left"]
        if rect["right"] > right_most:
            right_most = rect["right"]
        if rect["up"] < top_most:
            top_most = rect["up"]
        if rect["down"] > bottom_most:
            bottom_most = rect["down"]
    # print(f"top: {top_most}, bottom: {bottom_most}, left: {left_most}, right: {right_most}")
    total_width = right_most - left_most
    total_height = bottom_most - top_most
    max_value = max([rect["value"] for rect in important_rects])
    uniform_elements = []
    for rect in important_rects:
        rect["left"] = (rect["left"] - left_most) / total_width
        rect["right"] = (rect["right"] - left_most) / total_width
        rect["up"] = (rect["up"] - top_most) / total_height
        rect["down"] = (rect["down"] - top_most) / total_height
        rect["width"] = rect["width"] / total_width
        rect["height"] = rect["height"] / total_height
        rect["value"] = rect["value"] / max_value
        uniform_elements.append(rect)
    return uniform_elements

def get_text_bbox(text_element):

    text_anchor = text_element["text_anchor"]
    content = text_element["content"]
    length = len(text_element["content"])
    font_size = text_element["font_size"]
    width = text_element["bbox_w"]
    height = text_element["bbox_h"]
    x = text_element['bbox_x']
    y = text_element['bbox_y']

    text_bbox = {}
    text_bbox["x"] = x 
    text_bbox["y"] = y 
    text_bbox["w"] = width 
    text_bbox["h"] = height 

    text_bbox["content"] = try_convert_number(content)

    return text_bbox

    # if text_anchor == "start":


def get_text_group(original_text_group, texts_attr, is_legend = False):
    array = []
    if isinstance(original_text_group["x"], list):
        array = original_text_group["x"]
    elif isinstance(original_text_group["y"], list):
        array = original_text_group["y"]



    text_array = [texts_attr[item["text_id"]] for item in array]
    text_bbox = [get_text_bbox(item) for item in text_array]
    if is_legend:
        for i, text in enumerate(text_bbox):
            text["legend_id"] = i
    return text_bbox

def get_text_information(X_axis, Y_axis, legend, texts_attr):
    xAxis_text = get_text_group(X_axis, texts_attr)
    yAxis_text = get_text_group(Y_axis, texts_attr)
    legend_text = get_text_group(legend, texts_attr, is_legend = True)

    print("formal_x_axis_array", xAxis_text)
    print("formal_y_axis_array", yAxis_text)
    print("formal_legend_axis_array", legend_text)
    text_collection = {}
    text_collection['xAxis'] = {}
    text_collection['xAxis']["text"] = xAxis_text
    text_collection['yAxis'] = {}
    text_collection['yAxis']['text'] = yAxis_text 
    text_collection['legend'] = {}
    text_collection['legend']['text'] = legend_text
    text_collection['element'] = []

    return text_collection

def parse_unknown_svg(svg_string, need_data_soup = False):
    soup = bs4.BeautifulSoup(svg_string, "html5lib")
    svg = soup.select("svg")
    for defs in soup.find_all("defs"):
        defs.decompose()
    rects = soup.select("rect")
    print('debug!!', svg_string, svg, rects)
    for i in range(len(rects)):
        rects[i]["my_class_liucan"] = str(i)

    print("rect", len(rects))
    rects_attr = [parse_a_rect(rect) for rect in rects]
    texts = soup.select("text")
    newtexts = []
    for text in texts:
        if text.has_attr("transform") and "-90" in text["transform"]:
            continue
        else:
            newtexts.append(text)
    texts = newtexts
    print(texts)
    texts_attr = [parse_a_text(text) for text in texts]
    # add id, we need id
    for i in range(len(texts_attr)):
        texts_attr[i]["text_id"] = i

    # print(f"the length of texts_attr is {len(texts_attr)}")
    # for i in rects_attr:
    #     print(f"width is {i["width"]}, and height is {i["height"]}")
    # for i in texts_attr:
    #     print(f"the x is {i["x"]}, and the y is {i["y"]}")
    circles = soup.select("circle")
    print("circle", len(circles))
    circles_attr = [parse_a_circle(circle) for circle in circles]
    num_rect = len(rects_attr)
    num_circle = len(circles_attr)
    paths = soup.select("path")[2:-1] # TODO  NAIVE!!!!!!!!!!!!!!!!!!!!!!!!!
    num_path = len(paths)
    print(num_path, "number of paths")
    paths_attr = [parse_a_path(path) for path in paths]
    if num_path > 0:
        # print("parse_pie_chart no reason")
        # return parse_pie_chart(soup, paths_attr, texts_attr, rects_attr, need_data_soup = need_data_soup)
        print("parse_line_chart")
        return parse_line_chart(soup, paths_attr, texts_attr, rects_attr, need_data_soup = need_data_soup)
    elif num_circle > num_rect:
        print("parse_scatter_plot")
        return parse_scatter_plot(soup, circles_attr, texts_attr, need_data_soup = need_data_soup)

    print("parse_barchart")
    X_axis, Y_axis, legend = calculate_axis(texts_attr)
    is_vertical, width_array, height_array = judge_vertical(rects_attr)
    # print(f"X-axis: {X_axis} and Y-axis: {Y_axis}")

    print("legend_what", legend)

    text_information = get_text_information(X_axis, Y_axis, legend, texts_attr)

    # print("formal_x_axis_array", get_text_group(X_axis, texts_attr))
    # print("formal_y_axis_array", get_text_group(Y_axis, texts_attr))
    # print("formal_legend_axis_array", get_text_group(legend, texts_attr))
    # todo get the axis

    print("text_information", text_information) 

    if is_vertical:
        calculate_value = parse_quantity_array(Y_axis, "vertical")
        important_rects, other_rects = get_important_rects(rects_attr, "width", width_array)
        for i, rect in enumerate(important_rects):
            cal_value = calculate_value(rect["up"]) - calculate_value(rect["down"])
            important_rects[i]["value"] = cal_value
            # print(f"There value is {rect["value"]} and calculated is {cal_value}")

        legend = parse_legend(legend, other_rects)
        x_pair = X_axis["x"]
        def get_position(item):
            return item["position"]
        x_pair = sorted(x_pair, key = get_position)
        # print(x_pair)
        main_dimension_list = [x["content"] for x in x_pair]


        for i, rect in enumerate(important_rects):
            center_x = rect["left"] + rect["width"]/2
            diff_array = [abs(x["position"] - center_x) for x in x_pair]
            main_index = diff_array.index(min(diff_array))
            important_rects[i]["major"] = main_index
        important_rects = parse_color_legend(important_rects, legend)
        second_dimension_list = [item["content"] for item in legend]
    else:
        calculate_value = parse_quantity_array(X_axis, "horizontal")
        important_rects, other_rects = get_important_rects(rects_attr, "height", height_array)
        for i, rect in enumerate(important_rects):
            # TODO: Here in fact we direct using the up - down, left - right it"s not right
            cal_value = calculate_value(rect["right"]) - calculate_value(rect["left"])
            important_rects[i]["value"] = cal_value
            # print(f"Ther value is {rect["value"]} and calculated is {cal_value}")

        legend = parse_legend(legend, other_rects)
        y_pair = Y_axis["y"]
        def get_position(item):
            return item["position"]
        y_pair = sorted(y_pair, key = get_position)
        # print(y_pair)
        main_dimension_list = [y["content"] for y in y_pair]
        # print(main_dimension_list)

        for i, rect in enumerate(important_rects):
            center_y = rect["up"] + rect["height"]/2
            diff_array = [abs(y["position"] - center_y) for y in y_pair]
            main_index = diff_array.index(min(diff_array))
            important_rects[i]["major"] = main_index
        important_rects = parse_color_legend(important_rects, legend)

        second_dimension_list = [item["content"] for item in legend]

    print("legend_parsed", legend)
    main_dim, second_dim, data_type = get_main_second(main_dimension_list, second_dimension_list)
    if data_type == "ocq":
        if main_dim == "o0" and float(main_dimension_list[0]) > float(main_dimension_list[-1]):
            main_dimension_list.reverse()
            for i in range(len(important_rects)):
                important_rects[i]["major"] = len(main_dimension_list) - 1 - important_rects[i]["major"]
        elif second_dim == "o0" and float(second_dimension_list[0]) > float(second_dimension_list[-1]):
            second_dimension_list.reverse()
            for i in range(len(important_rects)):
                important_rects[i]["second"] = len(second_dimension_list) - 1 - important_rects[i]["second"]


    def get_order_value(item):
        return item["major"] * 100 + item["second"]
    important_rects = sorted(important_rects, key = get_order_value)
    print("important_rects", important_rects)
    data = pack_data(important_rects, main_dimension_list, second_dimension_list)
    data_string = json.dumps(data, indent = 2)
    uniform_elements = uniform_important_elements(important_rects)
    main_dim, second_dim, data_type = get_main_second(main_dimension_list, second_dimension_list)

    for i, element in enumerate(uniform_elements):
        uniform_elements[i][main_dim] = uniform_elements[i]["major"]
        uniform_elements[i][second_dim] = uniform_elements[i]["second"]
        uniform_elements[i]["q0"] = uniform_elements[i]["value"]
        uniform_elements[i]["id"] = i

    data['text_collection'] = text_information

    print("uniform elements:", uniform_elements)

    if need_data_soup:
        return uniform_elements, data, soup
    return uniform_elements, data, soup

def parse_scatter_plot(soup, circles_attr, texts_attr, need_data_soup = False):
    X_axis, Y_axis, legend = calculate_axis(texts_attr)
    Y_value_function = parse_quantity_array(Y_axis, "vertical")
    X_value_function = parse_quantity_array(X_axis, "horizontal")
    dataList = []
    data = {}
    for i, circle in enumerate(circles_attr):
        x_value = X_value_function(circle["x"])
        y_value = Y_value_function(circle["y"])
        circles_attr[i]["x_value"] = x_value
        circles_attr[i]["y_value"] = y_value
        dataList.append({"id": i, "q0": x_value, "q1": y_value, 'c0': 0, 'r': circle['r'], 'left':circle['left'], 'up': circle['up']})
    data["major_name"] = "q0"
    data["second_name"] = "q1"
    data["type"] = "cqq"
    data["vis_type"] = "load_scatter_plot"
    data['data_array'] = dataList
    return uniform_important_circle(data), data, soup

def parse_pie_chart(soup, paths_attr, texts_attr, rects_attr, need_data_soup=False):
    for path in paths_attr:
        print(path["pathObj"])
    areas = [path["pathObj"].area() for path in paths_attr]
    print(areas)
    return uniform_important_datapoint(data), data, soup

def parse_line_chart(soup, paths_attr, texts_attr, rects_attr, need_data_soup=False):
    eps = 1e-7
    data = {}
    height = float(soup.select("svg")[0]["height"])
    X_axis, Y_axis, legend= calculate_axis(texts_attr, 0)
    # x_array, y_array = count_text(texts_attr)
    # legend, tmp = extract_group(x_array, y_array, texts_attr)
    is_vertical, width_array, height_array = judge_vertical(rects_attr)
    legend = parse_legend(legend, rects_attr)
    print("x_axis", X_axis)
    Y_value_function = parse_quantity_array(Y_axis, "vertical")
    X_value_function = parse_quantity_array(X_axis, "horizontal")
    points = [item["position"] for item in X_axis["x"]]
    dataList = []
    o0 = [0 for i in points]
    data["color"] = [line["origin"]["stroke"] for line in paths_attr]
    c0 = [0 for i in paths_attr]
    for lid, line in enumerate(paths_attr):
        # print("\nLINE", lid, parse_fill(line["origin"]["stroke"]), ":")
        line_color = parse_fill(line["origin"]["stroke"])
        dis = [numpy.linalg.norm(numpy.array(line_color) - numpy.array(l["fill"])) for l in legend]
        category = numpy.argmin(dis)
        c0[lid] = legend[category]["content"]
        for idx, x in enumerate(points):
            o0[idx] = X_value_function(x);
        for idx, x in enumerate(points):
            print(x, end=": ")
            xtick = min(x-line["rx"], line["ex"]-eps)
            tmpLine = Line(xtick, complex(xtick, height))
            ratio = line["pathObj"].intersect(tmpLine)[0][0][0]
            coor = line["pathObj"].point(ratio)
            # o0[idx] = int(X_value_function(x) + float(X_axis["x"][0]["content"]))
            o0[idx] = int(X_value_function(x))
            y_value = Y_value_function(coor.imag+line["ry"])
            # + float(Y_axis["y"][0]["content"])
            # print(f"({coor.real+line["rx"]}, {coor.imag+line["ry"]}), ({o0[idx]}, {y_value})")
            dataList.append({"id": lid*len(points)+idx, "o0": idx, "q0": y_value, "c0": lid, "color": line_color})
    data["o0"] = o0
    data["c0"] = c0
    data["major_name"] = "o0"
    data["second_name"] = "c0"
    data["quantity"] = "q0"
    data["data_array"] = dataList
    data["type"] = "cqq"
    data["vis_type"] = "load_scatter_line_plot"
    data["unit"] = ""
    data["unit1"] = ""
    data["unit2"] = ""
    data_string = json.dumps(data, indent = 2)
    return uniform_important_datapoint(data), data, soup

def get_modified_svg_data(svg_string):
    print('extract_svg.py 660', svg_string)
    uniform_elements, data, soup = parse_unknown_svg(svg_string, need_data_soup = True)
    if data["type"]== "cqq":
        data["major"] = "c0"
        data["second"] = "c0"
        return soup.prettify(), data

    for i, rect in enumerate(uniform_elements):
        this_class = get_attr(rect["origin"], "class", default_value = [])
        for class_name in this_class:
            if class_name.startswith("element_"):
                this_class.remove(class_name)
        this_class.append("element_" + str(i))
        rect["origin"]["class"] = this_class
        rect["origin"]["id"] = str(i)
        #rect.pop('origin', None)
    # print('prettify', soup.prettify())
    # print(uniform_important_elements)
    return soup.prettify(), data

if __name__ == "__main__":
    # with open("../user_data/cq_liucan_20180827/cq_liucan_2018_08_27_22_26_43_53308.json") as f:
    #     svg_string = json.load(f)["svg_string"]
    # print(svg_string)


    svg_string = "<svg id='mySvg' viewBox='0 0 800 660' preserveAspectRatio='xMidYMid meet' height='736.8000000000001' width='681.15'><g transform='translate(80,66)'><g class='brush'></g><g class='axis axis--x' transform='translate(0,528)' fill='none' font-size='10' font-family='sans-serif' text-anchor='middle'><path class='domain' stroke='#000' d='M0.5,6V0.5H640.5V6'></path><g class='tick' opacity='1' transform='translate(23.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>2.5</text></g><g class='tick' opacity='1' transform='translate(74.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>3.0</text></g><g class='tick' opacity='1' transform='translate(126.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>3.5</text></g><g class='tick' opacity='1' transform='translate(178.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>4.0</text></g><g class='tick' opacity='1' transform='translate(229.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>4.5</text></g><g class='tick' opacity='1' transform='translate(281.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>5.0</text></g><g class='tick' opacity='1' transform='translate(332.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>5.5</text></g><g class='tick' opacity='1' transform='translate(384.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>6.0</text></g><g class='tick' opacity='1' transform='translate(435.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>6.5</text></g><g class='tick' opacity='1' transform='translate(487.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>7.0</text></g><g class='tick' opacity='1' transform='translate(539.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>7.5</text></g><g class='tick' opacity='1' transform='translate(590.5,0)'><line stroke='#000' y2='6'></line><text fill='#000' y='9' dy='0.71em'>8.0</text></g><text transform='translate(640,0)' dy='-0.2rem' text-anchor='end' class='text-truncate' font-size='12px' style='stroke: black;'></text></g><g class='axis axis--y' fill='none' font-size='10' font-family='sans-serif' text-anchor='end'><path class='domain' stroke='#000' d='M-6,528.5H0.5V0.5H-6'></path><g class='tick' opacity='1' transform='translate(0,491.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>4.5</text></g><g class='tick' opacity='1' transform='translate(0,444.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>5.0</text></g><g class='tick' opacity='1' transform='translate(0,398.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>5.5</text></g><g class='tick' opacity='1' transform='translate(0,351.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>6.0</text></g><g class='tick' opacity='1' transform='translate(0,304.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>6.5</text></g><g class='tick' opacity='1' transform='translate(0,257.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>7.0</text></g><g class='tick' opacity='1' transform='translate(0,211.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>7.5</text></g><g class='tick' opacity='1' transform='translate(0,164.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>8.0</text></g><g class='tick' opacity='1' transform='translate(0,117.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>8.5</text></g><g class='tick' opacity='1' transform='translate(0,70.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>9.0</text></g><g class='tick' opacity='1' transform='translate(0,24.5)'><line stroke='#000' x2='-6'></line><text fill='#000' x='-9' dy='0.32em'>9.5</text></g><text transform='rotate(-90)' y='6' dy='0.71em' text-anchor='end' font-size='12px' style='stroke: black;'></text></g><circle class='circle elements ordinary' id='0' q1='4.195158413649341' q0='7.198710763509903' cx='507' cy='520' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='1' q1='4.105998722491816' q0='4.927043197160465' cx='273' cy='528' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='2' q1='4.364412084049337' q0='7.37830627544404' cx='526' cy='504' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='3' q1='5.210340307895841' q0='8.483762324294965' cx='640' cy='425' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='4' q1='4.350192140293566' q0='6.55810174847378' cx='441' cy='505' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='5' q1='4.529851070919655' q0='6.326317742274604' cx='418' cy='488' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='6' q1='5.547626206456212' q0='5.7025203437971745' cx='353' cy='393' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='7' q1='5.156149386166263' q0='4.414933104625661' cx='220' cy='430' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='8' q1='4.768113385029239' q0='5.3893556309564215' cx='321' cy='466' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='9' q1='4.724600003289483' q0='7.255713472489231' cx='513' cy='470' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='10' q1='4.968379531106541' q0='7.802011701039131' cx='570' cy='447' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='11' q1='4.256542358750759' q0='6.224460335912584' cx='407' cy='514' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='12' q1='4.806544417768363' q0='5.77998785562214' cx='361' cy='462' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='13' q1='5.5624667740274605' q0='5.8255861573535075' cx='366' cy='392' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='14' q1='4.686869117921095' q0='6.6090828876121375' cx='447' cy='474' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='15' q1='5.079626059985793' q0='5.44627499741418' cx='327' cy='437' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='16' q1='4.918978967800686' q0='5.964580608845678' cx='380' cy='452' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='17' q1='4.158619991271559' q0='5.9854679120721075' cx='382' cy='523' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='18' q1='5.680169621906575' q0='5.705231706531228' cx='353' cy='381' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='19' q1='4.67873700685887' q0='5.7703495357084496' cx='360' cy='474' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='20' q1='4.224984856160664' q0='5.34239627869707' cx='316' cy='517' r='0.5vh' alpha='0.5'></circle><circle class='circle elements ordinary' id='21' q1='9.751683896073704' q0='2.2777864725083186' cx='0' cy='0' r='0.5vh' alpha='0.5'></circle><text class='title' text-anchor='middle' font-size='23.759999999999998' x='320' y='-31.68'>The Relation of Oil Asumption and GDP</text></g></svg>"
    # print(svg_string)

    parse_unknown_svg(svg_string)
