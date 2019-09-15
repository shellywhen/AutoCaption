# -*- coding: utf-8 -*-
# from numpy import random
import random
import numpy
import json
import os
import sys

current_url = os.path.dirname(__file__)
parent_url = os.path.abspath(os.path.join(current_url, os.pardir))
sys.path.append(current_url)

# print(current_url)
from generate_rule_data import generate_rule_data
from oq_data_generator import get_OQ_data
from basic_change import add_color, add_type, get_data_type, del_long_name, add_vis_type
from ocq_data_generator import get_OCQ_data



def get_q_by_c(data, major, c0, second, c1):
    for item in data['data_array']:
        if item[major] == c0 and item[second] == c1:
            return item['q0']
    return -1




def get_read_CCQ(json_path = "../data_collect_system/json/Ielts_new_principle/ielts_data/"):

    json_choice = os.listdir(json_path)
    while True:
        json_filename = json_choice[numpy.random.randint(0, len(json_choice))]
        json_filename = os.path.join(json_path, json_filename)
        # json_filename = os.path.join(json_path, '0019.json')
        with open(json_filename) as f:
            data = json.load(f)
            data = add_color(data)
            data = convert_ocq_ccq(data)
            if len(data['c0']) == 1  or len(data['c1']) == 1:
                continue;
            else:
                judge = numpy.random.randint(0,10)
                if judge < 5:
                    data = change_ccq_cat_order(data)

                data = change_order_ccq(data)
                data = add_random_errors(data)
                data = del_long_name(data)
                # print(data)
                return data

def add_random_errors(data, mu = 1, sigma = 0.2):
    new_data_array = []
    for item in data['data_array']:
        while (True):
            scale_rate = numpy.random.normal(mu, sigma)
            if scale_rate > 0:
                break;
        item['q0'] = int(item['q0'] * scale_rate * 2) / 2.0
        new_data_array.append(item)
    data['data_array'] = new_data_array
    return data

def convert_ocq_ccq(data):
    data_type = get_data_type(data)
    if (data_type != 'ocq'):
        return data
    data['title'] = 'Value'
    data['c1'] = ['#' + str(i) for i in range(len(data['o0']))]
    del data['o0']
    for i in range(len(data['data_array'])):
        data['data_array'][i]['c1'] = data['data_array'][i]['o0']
        del data['data_array'][i]['o0']

    return data

def change_order_ccq(data):
    data_type = get_data_type(data)
    if (data_type != 'ccq'):
        return data
    order0 = [i for i in range(len(data['c0']))]
    order1 = [i for i in range(len(data['c1']))]
    if len(order0) < 5:
        random.shuffle(order0)
    if len(order1) < 5:
        random.shuffle(order1)
    id = 0
    for i in range(len(order0)):
        for j in range(len(order1)):
            item = {}
            item['c0'] = i
            item['c1'] = j
            item['id'] = id
            id = id + 1
            item['q0'] = get_q_by_c(data, 'c0', order0[i], 'c1', order1[j])

    major_dim = data['c0']
    second_dim = data['c1']
    new_major_dim = [major_dim[order0[i]] for i in range(len(order0))]
    new_second_dim = [second_dim[order1[i]] for i in range(len(order1))]
    data['c0'] = new_major_dim
    data['c1'] = new_second_dim
    return data

def change_ccq_cat_order(data):
    data_type = get_data_type(data)
    # print(data_type)
    if (data_type != 'ccq'):
        return data
    # print(data_type)
    major = 'c0'
    second = 'c1'
    major_dim = data[major]
    second_dim = data[second]
    major_dim_num = len(major_dim)
    second_dim_num = len(second_dim)
    new_major = 'c0'
    new_second = 'c1'

    new_data_array = []

    id = 0

    for i in range(second_dim_num):
        for j in range(major_dim_num):
            q = get_q_by_c(data, major, j, second, i)
            item = {}
            item[new_major] = i
            item[new_second] = j
            item['id'] = id
            id = id + 1
            item['q0'] = q
            if q != -1:
                new_data_array.append(item)

    data['data_array'] = new_data_array
    data[new_major] = second_dim
    # print(new_major)
    # print(second_dim)
    data[new_second] = major_dim
    # print(data)

    return data

def get_data_value(datum):
    return datum['q0']

def change_cq_order(data, order = True):
    print(data)
    data_array = data['data_array']
    c0_dimension = data['c0']
    new_dimension = [i for i in range(len(c0_dimension))]
    data_array = sorted(data_array, key = lambda x:x['q0'])
    # print(data_array)
    for i, datum in enumerate(data_array):
        old_dimension_order = data_array[i]['c0']
        data_array[i]['id'] = i
        data_array[i]['c0'] = i
        new_dimension[i] = c0_dimension[old_dimension_order]

    data['data_array'] = data_array
    data['c0'] = new_dimension
    print(data)

    return data


def get_data(data_type = 'ocq'):
    generator = data_type
    if generator == "ccq":
        data = get_read_CCQ()
    elif generator == 'cq':
        data = get_simple_CQ()
    elif generator == 'oq':
        data = get_OQ_data()
    elif generator == 'ocq':
        data = get_OCQ_data()
    elif generator == "get_chinese_random_data":
        data = get_chinese_random_data()
    elif generator == 'special':
        data = get_OCQ_data(True)
    elif generator == 'rule':
        random_decider = random.randint(0,10)
        if random_decider < 5:
            data = generate_rule_data('ocq', 'load_stack_bar_chart','ocq_common')
        else:
            data = generate_rule_data('ocq', 'load_group_bar_chart','ocq_common')
    else:
        data = get_chinese_random_data()
    data = add_type(data)
    data = add_vis_type(data)
    return data


# get_ccq_data()
