# -*- coding: UTF8 -*-
import json
import numpy
import os
import sys

current_url = os.path.dirname(__file__)
parent_url = os.path.abspath(os.path.join(current_url, os.pardir))
sys.path.append(current_url)

from oq_generator import generate_oq_sentence, get_sentence_setting
from cq_generator import generate_cq_sentence
from ocq_generator import generate_ocq_sentence
from ccq_generator import generate_ccq_sentence
from qq_generator import generate_toy_qq_sentence


def generate_sentence_by(data, focus_id, compare_id, major_name, second_name, version = 'English'):
    print(f'Now deal with data type {data["type"]}')
    if data['type'] == 'cq':
        return generate_cq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')
    elif data['type'] == 'oq':
        return generate_oq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')
    elif data['type'] == 'ccq':
        return generate_ccq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')
    elif data['type'] == 'ocq':
        return generate_ocq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')
    elif data['vis_type'] == 'load_scatter_plot':
        return generate_qq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')
    elif data['type'] == 'cqq':
        return generate_ocq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English')

def example_try():
    with open("json/example.json", 'r') as f:
        data = json.load(f)
    focus_id = []
    compare_id = []
    for item in data['data_array']:
        if item['c0'] >= 0 and item['c0'] < 4:
            if item['c1'] >=0 and item['c1'] < 1:
                focus_id.append(item['id'])
            # else:
            #     compare_id.append(item['id'])
    return generate_sentence_by(data, focus_id, compare_id, 'c0', 'c1')
# get_fake_data()



if __name__ == '__main__':
    print(oq_generator.get_ordinal_name(['s','e']))
    # sentences = example_try()
    # for sentence in sentences:
    #     print(sentence['sentence'])
