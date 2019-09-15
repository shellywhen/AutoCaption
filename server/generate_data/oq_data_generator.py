import numpy
from basic_change import add_color, add_type, get_data_type
import os
import sys
import json
import random

def get_OQ_data():
    return get_data_from_file()

def add_small_value(data):
    max_value = max([datum['q0'] for datum in data['data_array']])
    for i in range(len(data['data_array'])):
        if data['data_array'][i]['q0'] <= 0:
            data['data_array'][i]['q0'] = max_value * 0.01
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

def add_small_random(data, sigma = 0.03):
    for i in range(len(data['data_array'])):
        data['data_array'][i]['q0'] = data['data_array'][i]['q0'] * numpy.random.normal(1, sigma)
    return data

def get_simple_OQ():
    data = {}
    data['title'] = 'Value'
    data_number = numpy.random.randint(3,11)
    data['o0'] = [2010 + i for i in range(data_number)]
    data['data_array'] = []
    for i in range(data_number):
        datum = {}
        datum['o0'] = i
        datum['q0'] = numpy.random.randint(20, 100)
        datum['id'] = i
        data['data_array'].append(datum)
    data['unit'] = ''
    add_color(data, single = True)

    data = change_oq_order(data)
    # data['']
    # print(data['data_array'])
    return data
def get_json_file_path():
    current_url = os.path.dirname(__file__)
    json_file_path = os.path.abspath(os.path.join(current_url, "../../data_collect_system/json/Ielts_new_principle/ielts_data/"))
    return json_file_path

def get_data_from_file():
    json_path = get_json_file_path()
    json_choice = os.listdir(json_path)
    while True:
        json_filename = json_choice[numpy.random.randint(0, len(json_choice))]
        json_fileurl = os.path.join(json_path, json_filename)
        f = open(json_fileurl)
        data = json.load(f)
        type = get_data_type(data)
        if type == 'ocq':
            if len(data['o0']) > 3:
                break
    print(data)
    cat_number = len(data['c0'])
    choose_cat = numpy.random.randint(cat_number)
    new_data_array = []
    for i, datum in enumerate(data['data_array']):
        if datum['c0'] == choose_cat:
            del datum['c0']
            datum['id'] = datum['o0']
            new_data_array.append(datum)
    data['title'] = f'Value of {data["c0"][choose_cat]}'
    del data['c0']
    data['data_array'] = new_data_array
    data['type'] = 'oq'
    data = add_color(data, single = True)
    data = add_small_value(data)
    data = add_small_random(data)
    return data
