import json
import numpy
import os
import sys
from oq_generator import get_sentence_setting

def get_value_array(data, id_array):
    value_array = []
    for id in id_array:
        value_array.append(data['data_array'][id]['q0'])
    return value_array

def get_name_array(data, id_array):
    name_array = []
    for id in id_array:
        name_array.append(data['c0'][data['data_array'][id]['c0']])
    return name_array

def get_aggre_name(name_array, version = 'English'):
    if len(name_array) == 0:
        return "Fatal: Not element found"
    elif len(name_array) == 1:
        return name_array[0]
    # elif len(choose_name) == total_length and total_length > 2:
    #     return "all"
    else:
        name = ""
        for i in range(len(name_array) - 2):
            if version == 'English':
                name = name + " "+ name_array[i] + ", "
            else:
                name = name + name_array[i] + "、"
        if version == 'English':
            name = name + name_array[-2] + " and " + name_array[-1]
        else:
            name = name + name_array[-2] + "与" + name_array[-1]
        if name[0] == " ":
            name = name[1:]
        return name


def get_compare_relation(focus_value, compare_value, data):
    V_total_max = max([ datum['q0'] for datum in data['data_array']])
    focus_mean = numpy.mean(focus_value)
    compare_mean = numpy.mean(compare_value)
    diff = abs((focus_mean - compare_mean) / V_total_max)
    ratio = focus_mean / compare_mean
    degree = ''
    if ratio > 1.05:
        relation = 'higher than'
        if ratio < 1.1:
            degree = 'slight'
        elif ratio > 1.5 and diff > 0.05:
            degree = 'greatly'
    elif ratio < 0.95:
        relation = 'lower than'
        if ratio > 0.9:
            degree = 'slight'
        elif ratio < 0.7 and diff > 0.05:
            degree = 'greatly'
    else:
        relation = 'same as'
        degree = 'almost'

    return relation, degree, ratio


# 判断是否满足对比的条件
def judge_compare_value(focus_value, compare_value, data):
    if len(focus_value) == 0 or len(compare_value) == 0:
        return False
    if min(focus_value) > max(compare_value) or max(focus_value) < min(compare_value):
        return True

    return False
# 判断是否满足计数的条件：
def judge_count(focus_value, compare_value, data):
    if len(compare_value) != 0 or len(focus_value) == 0:
        return False
    V_min = min(focus_value)
    V_max = max(focus_value)

    if len([datum for datum in data['data_array'] if datum['q0'] >= V_min and datum['q0'] <= V_max]) == len(focus_value):
        return True
    return False

def judge_same(focus_value, compare_value, data, total_limit = 0.1, local_limit = 0.2):
    if len(compare_value) != 0 or len(focus_value) < 2:
        return False
    V_total_max = max([datum['q0'] for datum in data['data_array']])
    V_min = min(focus_value)
    V_max = max(focus_value)
    if (V_max - V_min) / V_total_max < total_limit and (V_max - V_min) / V_max < local_limit:
        return True
    return False

def judge_range(focus_value, compare_value, data):
    if len(compare_value) != 0 or len(focus_value) == 0:
        return False
    return True

# generate rules.

def get_compare_value(data, focus_value, compare_value, focus_aggre_name, compare_aggre_name):
    sentences = []
    relation, degree, ratio = get_compare_relation(focus_value, compare_value, data)
    sentence = f'The value in {focus_aggre_name} is {degree} {relation} {compare_aggre_name}'
    sentences.append(get_sentence_setting('compare', sentence))
    if len(focus_value) + len(compare_value) == len(data['data_array']) and len(compare_value) > 2:
        sentence = f'The value in {focus_aggre_name} is {degree} {relation} others'
        sentences.append(get_sentence_setting('compare', sentence))

        if relation != 'same as':
            if relation == 'higher than':
                extreme = 'highest'
            elif relation == 'lower than':
                extreme = 'lowest'
            if (len(focus_value) == 1):
                sentence = f'{focus_aggre_name} have the {extreme} {len(focus_value)} value'
                sentences.append(get_sentence_setting('compare', sentence))
            else:
                sentence = f'{focus_aggre_name} have the {extreme} {len(focus_value)} value'
                sentences.append(get_sentence_setting('compare', sentence))

    return sentences

def get_count(data, focus_value, compare_value, focus_aggre_name, compare_aggre_name):
    # print('into count')
    sentences = []
    V_all = [datum['q0'] for datum in data['data_array']]
    V_total_max = max(V_all)
    V_total_min = min(V_all)

    V_min = min(focus_value)
    V_max = max(focus_value)
    count = len(focus_value)
    if V_max == V_total_max:
        sentence = f'There are {count} categeries that higher than {V_min}'
        sentences.append(get_sentence_setting('count', sentence))
    if V_min == V_total_min:
        sentence = f'There are {count} categeries that lower than {V_max}'
        sentences.append(get_sentence_setting('count', sentence))
    return sentences

def get_range(data, focus_value, compare_value, focus_aggre_name, compare_aggre_name):
    # type = absolute_range/ absolute_higher/
    sentences = []
    V_all = [datum['q0'] for datum in data['data_array']]
    V_total_max = max(V_all)
    V_total_min = min(V_all)
    V_min = min(focus_value)
    V_max = max(focus_value)
    count = len(focus_value)
    if len(focus_value) == 1:
        sentence = f'The value of {focus_aggre_name} is {focus_value[0]}'
        sentences.append(get_sentence_setting('absolute_single', sentence))
        return sentences
    if len(focus_value) == len(data['data_array']):
        focus_aggre_name = 'all categories'
    sentence = f'The value of {focus_aggre_name} are higher than {V_min}'
    sentences.append(get_sentence_setting('absolute_higher', sentence))
    sentence = f'The value of {focus_aggre_name} are lower than {V_max}'
    sentences.append(get_sentence_setting('absolute_lower', sentence))
    sentence = f'The value of {focus_aggre_name} ranges from {V_min} to {V_max}'
    sentences.append(get_sentence_setting('absolute_range', sentence))

    return sentences

def get_same(data, focus_value, compare_value, focus_aggre_name, compare_aggre_name):
    sentences = []
    sentence = f'The value of {focus_aggre_name} is almost the same, around {int(numpy.mean(focus_value))} {data["unit"]}'
    sentences.append(get_sentence_setting('same', sentence))
    return sentences

def generate_cq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English'):
    focus_value_array = get_value_array(data, focus_id)
    compare_value_array = get_value_array(data, compare_id)
    focus_name_array = get_name_array(data, focus_id)
    compare_name_array = get_name_array(data, compare_id)
    focus_aggre_name = get_aggre_name(focus_name_array)
    compare_aggre_name = get_aggre_name(compare_name_array)
    sentences = []
    if (judge_compare_value(focus_value_array, compare_value_array, data)):
        sentences = sentences + get_compare_value(data, focus_value_array, compare_value_array, focus_aggre_name, compare_aggre_name)
    if (judge_range(focus_value_array, compare_value_array, data)):
        sentences = sentences + get_range(data, focus_value_array, compare_value_array, focus_aggre_name, compare_aggre_name)
    if (judge_same(focus_value_array, compare_value_array, data)):
        sentences = sentences + get_same(data, focus_value_array, compare_value_array, focus_aggre_name, compare_aggre_name)
    if (judge_count(focus_value_array, compare_value_array, data)):
        sentences = sentences + get_count(data, focus_value_array, compare_value_array, focus_aggre_name, compare_aggre_name)
    for sentence in sentences:
        sentence['compare_id'] = compare_id
        sentence['focus_id'] = focus_id

    return sentences
