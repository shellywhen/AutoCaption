import numpy
from basic_change import add_color, add_type, get_data_type, del_long_name, add_vis_type
import os
import sys
import json
import random

def get_OCQ_data(special = False):
    if special:
        data = get_from_special_file()
    else:
        data = get_data_from_file()

    data['major_name'] = 'o0'
    data['second_name'] = 'c0'
    return data

def add_small_value(data):
    max_value = max([datum['q0'] for datum in data['data_array']])
    for i in range(len(data['data_array'])):
        if data['data_array'][i]['q0'] <= 0:
            data['data_array'][i]['q0'] = max_value * 0.01 * numpy.random.randint(5,10)
    return data

def change_oq_order(data, order = True):
    data_array = data['data_array']
    data_array = sorted(data_array, key = lambda x:x['q0'])
    # print(data_array)
    for i, datum in enumerate(data_array):
        data_array[i]['id'] = i
        data_array[i]['o0'] = i

    data['data_array'] = data_array
    return data

def add_random_by_cat(data, sigma = 0.2, cat_name = 'c0', quantity_name = 'q0', absolute_rate_base = 0.3):
    type = get_data_type(data)
    if (type != 'ocq'):
        print("the type is not ocq, we can not handle this")
        return data
    cat_dim = data[cat_name]
    max_value = max([datum[quantity_name] for datum in data['data_array']])

    for cat in range(len(cat_dim)):
        random_rate = numpy.random.normal(1, sigma)
        absolute_random = max_value * abs(numpy.random.normal(absolute_rate_base, sigma))
        if (random_rate < 0):
            random_rate = - random_rate
        for i, datum in enumerate(data['data_array']):
            if datum[cat_name] == cat:
                data['data_array'][i][quantity_name] = data['data_array'][i][quantity_name] * random_rate + absolute_random

    min_value = min([datum[quantity_name] for datum in data['data_array']])
    cut_random_rate = numpy.random.normal(1, sigma)
    if cut_random_rate > 0.8:
        cut_random_rate = 0.8
    if cut_random_rate < 0:
        cut_random_rate = 0
    cut_random_value = cut_random_rate * min_value

    for i, datum in enumerate(data['data_array']):
        data['data_array'][i][quantity_name] = datum[quantity_name] - cut_random_value


    return data
    # for i in range(len(data['data_array'])):


def add_small_random(data, sigma = 0.03):
    for i in range(len(data['data_array'])):
        data['data_array'][i]['q0'] = data['data_array'][i]['q0'] * numpy.random.normal(1, sigma)
    return data

def get_json_file_path():
    current_url = os.path.dirname(__file__)
    json_file_path = os.path.abspath(os.path.join(current_url, "../../data_collect_system/json/Ielts_new_principle/ielts_data/"))
    return json_file_path

def change_cat_order(data, cat_name = 'c0'):
    cat_dimension = data[cat_name]
    cat_num = len(cat_dimension)
    cat_order = [i for i in range(cat_num)]
    random.shuffle(cat_order)
    data_array = data['data_array']
    data_array = sorted(data_array, key = lambda x:cat_order[x['c0']] * 100 + x['o0'])
    # print(cat_order)
    # print(data_array)
    for i in range(len(data_array)):
        data_array[i]['id'] = i
        data_array[i]['c0'] = cat_order[data_array[i]['c0']]
    # print(data_array)
    new_catname = [cat_dimension[cat_order[i]] for i in range(cat_num)]
    data['data_array'] = data_array
    data[cat_name] = new_catname
    return data
def cut_cat(data, cat_name = 'c0'):
    cat_dimension = data[cat_name]
    cat_num = len(cat_dimension)

def get_from_special_file(json_filename = '0070.json'):
    json_path = get_json_file_path()
    json_fileurl = os.path.join(json_path, json_filename)
    f = open(json_fileurl)
    data = json.load(f)
    data = add_random_by_cat(data)
    data = change_cat_order(data)
    data = add_small_random(data, 0)
    data = add_small_value(data)
    data = del_long_name(data)
    data = add_color(data)
    data = add_type(data)
    data = add_vis_type(data)

    return data


def get_data_from_file():
    json_path = get_json_file_path()
    json_choice = os.listdir(json_path)
    while True:
    # for i in range(10, 20):
        # json_filename = json_choice[i]
        json_filename = json_choice[numpy.random.randint(0, len(json_choice))]
        json_fileurl = os.path.join(json_path, json_filename)
        f = open(json_fileurl)
        data = json.load(f)
        type = get_data_type(data)
        if type == 'ocq':
            break
    # print(data)
    data = add_random_by_cat(data)
    data = change_cat_order(data)
    data = add_small_random(data, 0)
    data = add_small_value(data)
    data = del_long_name(data)
    data = add_color(data)
    data = add_type(data)
    data = add_vis_type(data)
    return data

if __name__ == '__main__':
    get_data_from_file()
