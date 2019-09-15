# -*- coding: UTF8 -*-
import json
import numpy

from oq_generator import get_sentence_setting, cal_trend_from_quantity_array, get_ordinal_trend_component, get_aggre_name, fix_sentence_end
from ccq_generator import generate_ccq_sentence


def judge_compare_trend(data, focus_id, compare_id):
    return True

def judge_trend_absolute(data, focus_id, compare_id):
    return True

def judge_sum_trend(data, focus_id, compare_id):
    return True




# 统计一个数组里的频率
def get_count_by_cat_and_ord(data, id_array, category_name = 'c0', ordinal_name = 'o0'):
    category_num = len(data[category_name])
    ordinal_num = len(data[ordinal_name])
    category_count = [0 for i in range(category_num)]
    ordinal_count = [0 for i in range(ordinal_num)]
    for i in id_array:
        datum = data['data_array'][i]
        category_count[datum[category_name]] = category_count[datum[category_name]] + 1.0
        ordinal_count[datum[ordinal_name]] = ordinal_count[datum[ordinal_name]] + 1.0
    return numpy.array(category_count), numpy.array(ordinal_count)

# modify 函数，修改id让他们成为有效的 compare id 和 focus id
def modify_compare_trend(data, focus_id, compare_id, category_name = 'c0', ordinal_name = 'o0', barrier = 0.3):
    # calculate the dimension that focus will choose.
    focus_category_cnt, focus_ordinal_cnt = get_count_by_cat_and_ord(data, focus_id)
    compare_category_cnt, compare_ordinal_cnt = get_count_by_cat_and_ord(data, compare_id)

    focus_category_chosen = numpy.logical_and(focus_category_cnt > max(focus_category_cnt) * barrier, focus_category_cnt >= compare_category_cnt)
    focus_ordinal_chosen = focus_ordinal_cnt > max(focus_ordinal_cnt) * barrier

    # calculate the dimension that compare will choose.
    compare_category_chosen = numpy.logical_and(compare_category_cnt > max(compare_category_cnt) * barrier, compare_category_cnt > focus_category_cnt)
    compare_ordinal_chosen = compare_ordinal_cnt > max(compare_ordinal_cnt) * barrier

    # 同步： 拥有同样的起始点和终止点
    if len(focus_category_chosen) > 0 and len(compare_category_chosen) > 0 :
        for i in range(len(focus_ordinal_chosen)):
            if focus_ordinal_chosen[i] or compare_ordinal_chosen[i]:
                focus_ordinal_chosen[i] = True
                compare_ordinal_chosen[i] = True
                break
        for i in reversed(range(len(focus_ordinal_chosen))):
            if focus_ordinal_chosen[i] or compare_ordinal_chosen[i]:
                focus_ordinal_chosen[i] = True
                compare_ordinal_chosen[i] = True
                break

    new_focus_id = []
    new_compare_id = []
    for datum in data['data_array']:
        if focus_category_chosen[datum[category_name]] and focus_ordinal_chosen[datum[ordinal_name]]:
            new_focus_id.append(datum['id'])
        elif compare_category_chosen[datum[category_name]] and compare_ordinal_chosen[datum[ordinal_name]]:
            new_compare_id.append(datum['id'])


    focus_category_chosen = [i for i in range(len(focus_category_chosen)) if focus_category_chosen[i]]
    focus_ordinal_chosen = [i for i in range(len(focus_ordinal_chosen)) if focus_ordinal_chosen[i]]

    compare_category_chosen = [i for i in range(len(compare_category_chosen)) if compare_category_chosen[i]]
    compare_ordinal_chosen = [i for i in range(len(compare_ordinal_chosen)) if compare_ordinal_chosen[i]]

    return new_focus_id, new_compare_id, focus_category_chosen, focus_ordinal_chosen, compare_category_chosen, compare_ordinal_chosen


def modify_sum_trend(data, focus_id, compare_id, category_name = 'c0', ordinal_name = 'o0', barrier = 0.3):
    category_count, ordinal_count = get_count_by_cat_and_ord(data, set(focus_id)|set(compare_id))
    max_category_count = max(category_count)
    max_ordinal_count = max(ordinal_count)
    category_chosen = numpy.array(category_count) > max_category_count * barrier
    ordinal_chosen = numpy.array(ordinal_count) > max_ordinal_count * barrier
    new_focus_id = []
    for datum in data['data_array']:
        if category_chosen[datum[category_name]] and ordinal_chosen[datum[ordinal_name]]:
            new_focus_id.append(datum['id'])

    category_chosen = [i for i in range(len(category_chosen)) if category_chosen[i]]
    ordinal_chosen = [i for i in range(len(ordinal_chosen)) if ordinal_chosen[i]]

    return new_focus_id, [], category_chosen, ordinal_chosen

# 描述总值的变化
# 如：总值从2008 到 2018年的变化

def get_sum_quantity_array(data, category_chosen, ordinal_name = 'o0', category_name = 'c0', quantity_name = 'q0'):

    ordinal_sum_quantity = [0 for name in data[ordinal_name]]

    for datum in data['data_array']:
        if datum[category_name] in category_chosen:
            ordinal_sum_quantity[datum[ordinal_name]] = ordinal_sum_quantity[datum[ordinal_name]] + datum[quantity_name]

    return ordinal_sum_quantity
# def get_sum_sentence(data, category_chosen, ordinal_chosen):

# 分段，并且获取各段的参数
def get_segment_parameter(ordinal_chosen, quantity_array, max_value):
    segment_array = [[ordinal_chosen[i], ordinal_chosen[i + 1]] for i in range(len(ordinal_chosen) - 1)]
    segment_parameter_array = [cal_trend_from_quantity_array(quantity_array[segment[0]: segment[1] + 1], max_value) for segment in segment_array]
    return segment_array, segment_parameter_array

def get_cat_quantity_array(data, cat_index):
    return get_sum_quantity_array(data, [cat_index])

def get_sentence(data, segment_array, segment_parameter_array, quantity_array, ordinal_name = 'o0', object_name = '', allow_absolute_value = True):
    sentence = ''
    for i in range(len(segment_array)):
        segment = segment_array[i]
        std_mean = segment_parameter_array[i]
        begin_o_index = segment[0]
        end_o_index = segment[1]
        begin_name = data[ordinal_name][begin_o_index]
        end_name = data[ordinal_name][end_o_index]
        begin_value = quantity_array[begin_o_index]
        end_value = quantity_array[end_o_index]
        need_absolute_value = False
        if end_value == max(quantity_array) or end_value == min(quantity_array):
            need_absolute_value = True
        need_absolute_value = need_absolute_value and allow_absolute_value
        sentence = sentence + get_ordinal_trend_component(begin_name, begin_value, end_name, end_value, std_mean, end_o_index - begin_o_index, i == 0, object_name, need_absolute_value = need_absolute_value)
    return sentence

def modify_local_trend(data, focus_id, compare_id, category_name = 'c0', ordinal_name = 'o0', barrier = 0.3):
    category_count, ordinal_count = get_count_by_cat_and_ord(data, set(focus_id)|set(compare_id))
    max_category_count = max(category_count)
    max_ordinal_count = max(ordinal_count)

    category_chosen = numpy.array(category_count) > max_category_count * barrier
    ordinal_chosen = numpy.array(ordinal_count) > max_ordinal_count * barrier
    for i in range(len(ordinal_count) - 2):
        if ordinal_chosen[i] and ordinal_chosen[i + 1] and ordinal_chosen[i + 2]:
            for j in range(0, i):
                ordinal_chosen[j] = False
            if i + 2 < len(ordinal_count):
                for j in range(i + 3, len(ordinal_count)):
                    ordinal_chosen[j] = False
            break
    if sum(ordinal_chosen) < 3:
        for i in range(len(ordinal_count)):
            ordinal_chosen[i] = False
        for i in range(len(category_count)):
            category_chosen[i] = False

    new_focus_id = []
    for datum in data['data_array']:
        if category_chosen[datum[category_name]] and ordinal_chosen[datum[ordinal_name]]:
            new_focus_id.append(datum['id'])

    category_chosen = [i for i in range(len(category_chosen)) if category_chosen[i]]
    ordinal_chosen = [i for i in range(len(ordinal_chosen)) if ordinal_chosen[i]]

    compare_id = []

    return new_focus_id, compare_id, category_chosen, ordinal_chosen

def sentence_local_trend(data, focus_id, compare_id, major_name = 'c0', second_name = 'o0', version = 'English', fuzzy = True, ordinal_name = 'o0', category_name = 'c0'):

    if len(data[second_name]) < 4:
        return []
    focus_id, compare_id, category_chosen, ordinal_chosen = modify_local_trend(data, focus_id, compare_id)
    sentences = []
    if len(ordinal_chosen) < 3:
        return []
    ordinal_sum_quantity = get_sum_quantity_array(data, category_chosen)
    max_value = max(ordinal_sum_quantity)

    category_num = len(data['c0'])

    sentence = ''
    if ordinal_sum_quantity[ordinal_chosen[1]] > ordinal_sum_quantity[ordinal_chosen[0]] and ordinal_sum_quantity[ordinal_chosen[1]] > ordinal_sum_quantity[ordinal_chosen[2]]:
        sentence = f' there is an unusual rise in {get_aggre_name([data[second_name][ordinal_chosen[1]]], 10)} of {get_aggre_name([data[major_name][i] for i in category_chosen], category_num)}'
        sentences.append(get_sentence_setting('local_trend', sentence, focus_id, compare_id))

        sentence = f' the sum value of {get_aggre_name([data[major_name][i] for i in category_chosen], category_num)} has an unusual rise in {get_aggre_name([data[second_name][ordinal_chosen[1]]], 10)} '
        sentences.append(get_sentence_setting('local_sum_trend', sentence, focus_id, compare_id))


    if ordinal_sum_quantity[ordinal_chosen[1]] < ordinal_sum_quantity[ordinal_chosen[0]] and ordinal_sum_quantity[ordinal_chosen[1]] < ordinal_sum_quantity[ordinal_chosen[2]]:
        sentence = f'There is an unusual drop in {get_aggre_name([data[second_name][ordinal_chosen[1]]], 10)} of {get_aggre_name([data[major_name][i] for i in category_chosen], category_num)}'
        sentences.append(get_sentence_setting('local_trend', sentence, focus_id, compare_id))

        sentence = f' the sum value of {get_aggre_name([data[major_name][i] for i in category_chosen], category_num)} has an unusual drop in {get_aggre_name([data[second_name][ordinal_chosen[1]]], 10)} '
        sentences.append(get_sentence_setting('local_sum_trend', sentence, focus_id, compare_id))

    return sentences

def sentence_sum_trend(data, focus_id, compare_id, major_name = 'c0', second_name = 'q0', version = 'English', fuzzy = True, ordinal_name = 'o0', category_name = 'c0'):
    focus_id, compare_id, category_chosen, ordinal_chosen = modify_sum_trend(data, focus_id, compare_id)
    if len(ordinal_chosen) < 2:
        return []
    ordinal_sum_quantity = get_sum_quantity_array(data, category_chosen)
    max_value = max(ordinal_sum_quantity)
    segment_array, segment_parameter_array = get_segment_parameter(ordinal_chosen, ordinal_sum_quantity, max_value)
    # 只有一个没办法称为sum
    if len(category_chosen) == 1:
        object_name = f'The value of {get_aggre_name([data[category_name][i] for i in category_chosen], len(data[category_name]))}'
    else:
        object_name = f'The sum value of {get_aggre_name([data[category_name][i] for i in category_chosen], len(data[category_name]))}'
    sentence = get_sentence(data, segment_array, segment_parameter_array, ordinal_sum_quantity, object_name = object_name)
    sentences = []
    # sentence = str(segment_parameter_array)
    sentences.append(get_sentence_setting('sum_trend', sentence, focus_id, compare_id))
    if len(category_chosen) > 1:
        object_name = f'The value of {get_aggre_name([data[category_name][i] for i in category_chosen], len(data[category_name]))}'
    sentence = get_sentence(data, segment_array, segment_parameter_array, ordinal_sum_quantity, object_name = object_name, allow_absolute_value = False)
    sentences.append(get_sentence_setting('all_trend', sentence, focus_id, compare_id, sure = False))
    return sentences

# 比较趋势：
# 某某项从2008 到 2018年 上升， 而某某项
# 某某项比其他项上升得飞快，而

def get_ave_parameter(data, focus_category_chosen, focus_ordinal_chosen, max_value):
    focus_parameter_array_sum = [[0,0] for i in range(len(focus_ordinal_chosen) - 1)]
    for focus_cat in focus_category_chosen:
        focus_quantity = get_cat_quantity_array(data, focus_cat)
        focus_segment_array, segment_parameter_array = get_segment_parameter(focus_ordinal_chosen, focus_quantity, max_value)

        for i in range(len(segment_parameter_array)):
            focus_parameter_array_sum[i][0] = focus_parameter_array_sum[i][0] + segment_parameter_array[i][0]
            focus_parameter_array_sum[i][1] = focus_parameter_array_sum[i][1] + segment_parameter_array[i][1]

    for i,segment in enumerate(focus_parameter_array_sum):
        focus_parameter_array_sum[i][0] = segment[0] / len(focus_category_chosen)
        focus_parameter_array_sum[i][1] = segment[1] / len(focus_category_chosen)


    return focus_segment_array, focus_parameter_array_sum, focus_quantity

def sentence_compare_trend(data, focus_id, compare_id, major_name = 'c0', second_name = 'o0', version = 'English', fuzzy = True, quantity_name = 'q0', category_name = 'c0'):
    focus_id, compare_id, focus_category_chosen, focus_ordinal_chosen, compare_category_chosen, compare_ordinal_chosen = modify_compare_trend(data, focus_id, compare_id)
    if len(focus_category_chosen) == 0 or len(compare_category_chosen) == 0 or len(focus_ordinal_chosen) <2 or len(compare_ordinal_chosen) < 2:
        return []
    max_value = max([datum[quantity_name] for datum in data['data_array']])
    focus_name = get_aggre_name([data[category_name][i] for i in focus_category_chosen], len(data[category_name]))
    compare_name = get_aggre_name([data[category_name][i] for i in compare_category_chosen], len(data[category_name]))

    focus_segment_array, focus_parameter_array_ave, focus_quantity = get_ave_parameter(data, focus_category_chosen, focus_ordinal_chosen, max_value)
    compare_segment_array, compare_parameter_array_ave, compare_quantity = get_ave_parameter(data, compare_category_chosen, compare_ordinal_chosen, max_value)
    if len(focus_category_chosen) > 1:
        allow_absolute_value = False
    else:
        allow_absolute_value = True
    focus_sentence = get_sentence(data, focus_segment_array, focus_parameter_array_ave, focus_quantity, object_name = '', allow_absolute_value = allow_absolute_value)
    focus_sentence = fix_sentence_end(focus_sentence)

    if len(compare_category_chosen) > 1:
        allow_absolute_value = False
    else:
        allow_absolute_value = True
    compare_sentence = get_sentence(data, compare_segment_array, compare_parameter_array_ave, compare_quantity, object_name = '', allow_absolute_value = allow_absolute_value)
    sentence = f'The value of {focus_name} {focus_sentence}; while {compare_name} {compare_sentence}'

    sentences = []
    sentences.append(get_sentence_setting('compare_trend', sentence, focus_id, compare_id))

    return sentences

# 形容趋势：
# 形容某某项的趋势有所上升


def clean_input_id(data, focus_id, compare_id):
    return focus_id, compare_id

def generate_ocq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English', fuzzy = True):
    focus_id, compare_id = clean_input_id(data, focus_id, compare_id)
    sentences = []

    #
    if judge_compare_trend(data, focus_id, compare_id):
        sentences = sentences + sentence_sum_trend(data, focus_id, compare_id, fuzzy = fuzzy)
    if judge_sum_trend(data, focus_id, compare_id):
        sentences = sentences + sentence_compare_trend(data, focus_id, compare_id, fuzzy = fuzzy)
    sentences = sentences + sentence_local_trend(data, focus_id, compare_id, fuzzy = fuzzy)
    sentences = sentences + generate_ccq_sentence(data, focus_id, compare_id, major_name, second_name, version = version)

    return sentences






if __name__ == '__main__':
    sentences = get_general_trend()
    for sentence in sentences:
        print(sentence)
