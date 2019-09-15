# -*- coding:utf-8 -*-
import numpy
import json
# from .spider.deal_svg_copy import parse_svg_full

# Get the data inside
def extract_data():
    data = []
    return data

# 获取某维度的名字
def get_type_name(data, dimension, index):
    name = ''
    return name

def get_all_name(cat_name, cat_choice):
    name_set = []
    for i, cat in enumerate(cat_choice):
        if cat:
            name_set.append(cat_name[i])
    name_set_number = len(name_set)
    if name_set_number == 0:
        return "Fatal: Not element found"
    elif name_set_number == 1:
        return name_set[0]
    else:
        name = ""
        for i in range(name_set_number - 2):
            name = name + " "+ name_set[i] + ", "
        name = name + name_set[-2] + " and " + name_set[-1]
        if name[0] == " ":
            name = name[1:]
        return name

# def cal_dimension_numbers(cat,element_full_information):


def get_data_from_json(json_name):
    data = {}
    return data

def get_data_from_svg(svg_name):
    data = {}
    return data

def get_fake_data():
    with open("../../datasets/ielts/data_new_id_20180204.json") as f:
        data = json.load(f)
    data = data[0]
    data['data'] = parse_data(data['data'], data['first_dimension'])
    print(data)
    return data
# Parse the data u read from json to a nornal form.
def parse_data(data_inside, first_dimension):
    data = []
    for cat1 in first_dimension:
        data.append(data_inside[cat1])
    return data

def cal_attribute(element_set):
    max_category_num = 10
    if len(element_set) == 0:
        return 

    quantity0 = []
    quantity1 = []
    category0_index = []
    category1_index = []
    category0 = numpy.zeros(max_category_num)
    category1 = numpy.zeros(max_category_num)

    for element in element_set:
        assert(len(element) == 35)
        # print(numpy.split(element, [3,9,12,13,14,15,25]))
        type, position, color, opacity, q0, q1, c0, c1 = numpy.split(element, [3,9,12,13,14,15,25])
        category0_index.append(numpy.where(c0 > 0)[0][0])
        category1_index.append(numpy.where(c1 > 0)[0][0])
        quantity0.append(q0[0])
        quantity1.append(q1[0])
        category0 = category0 + c0
        category1 = category1 + c1
    category0 = category0.astype("int64").tolist()
    category1 = category1.astype("int64").tolist()
    quantity0 = aggregate(quantity0, category0_index)
    quantity1 = aggregate(quantity1, category1_index)
    result = {}
    result["quantity0"] = quantity0
    result["quantity1"] = quantity1
    result["category0"] = category0
    result["category1"] = category1
    return result

def aggregate(quantity, category_index):
    result = {}
    result["raw"] = quantity
    result["max"] = (max(quantity), category_index[quantity.index(max(quantity))])
    result["min"] = (min(quantity), category_index[quantity.index(min(quantity))])
    result["ave"] = (sum(quantity)/len(quantity))
    result["sum"] = (sum(quantity))
    return result

# 根据关键区域和比较区域的分布，判断哪个维度是关键的维度，而哪些不是。
def judge_diff_cat(focal_statistic, compare_statistic):
    print(focal_statistic)
    focal_cat0 = numpy.asarray(focal_statistic["category0"]) > 0
    focal_cat1 = numpy.asarray(focal_statistic["category1"]) > 0
    compare_cat0 = numpy.asarray(compare_statistic["category0"]) > 0
    compare_cat1 = numpy.asarray(compare_statistic["category1"]) > 0

    # print(focal_cat0 ^ compare_cat0)
    # print(focal_cat1 ^ compare_cat1)
    cat0_diff = sum(focal_cat0 ^ compare_cat0)
    cat1_diff = sum(focal_cat1 ^ compare_cat1)

    return cat0_diff, cat1_diff


# 根据两个numpy，获取关键区域和比较区域的正确的值
def get_focal_compare_from_numpy(element_set, element_full_information):
    focal_element = []
    compare_element = []
    important_element = []
    total_element_number = len(element_full_information)
    assert(total_element_number == len(element_set))
    for i in range(total_element_number):
        element_type = get_element_type(element_set[i])
        element = element_full_information[i]
        if (element_type > 0 ):
            important_element.append(element)
        # 重要的元素是主要元素和对比元素都在其中的。
        if (element_type == 2):
            focal_element.append(element)
        elif (element_type == 1):
            compare_element.append(element)
    return focal_element, compare_element, important_element

    # element_information =
# 根据某个elementset， 判断其是哪个选择。

def get_element_type(element):
    return numpy.where(element == element.max())[0][0]


    # indices = numpy.where(element_set == element_set.max())
    # print(indices)
