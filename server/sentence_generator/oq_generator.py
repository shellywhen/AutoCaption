# -*- coding: UTF8 -*-
import json
import numpy

def get_aggre_name(choose_name, total_length, version = 'English'):
    if len(choose_name) == 0:
        return "Fatal: Not element found"
    elif len(choose_name) == 1:
        return choose_name[0]
    # elif len(choose_name) == total_length and total_length > 2:
    #     return "all"
    else:
        name = ""
        for i in range(len(choose_name) - 2):
            if version == 'English':
                name = name + " "+ choose_name[i] + ", "
            else:
                name = name + choose_name[i] + "、"
        if version == 'English':
            name = name + choose_name[-2] + " and " + choose_name[-1]
        else:
            name = name + choose_name[-2] + "与" + choose_name[-1]
        if name[0] == " ":
            name = name[1:]
        return name

def fix_sentence_end(sentence):
    sentence = ' '.join(sentence.split())
    punctuation = [',', '.', ';', ':']
    if sentence[-1] in punctuation:
        sentence = sentence[:-1]
    return sentence

def get_sentence_setting(type, sentence, focus_id = [], compare_id = [], sure = True):
    sentence = fix_sentence_end(sentence)
    sentence = sentence + '.'
    sentence = sentence[0].upper() + sentence[1:]
    sentence_full_setting = {}
    sentence_full_setting['type'] = type
    sentence_full_setting['sentence'] = sentence
    sentence_full_setting['compare_id'] = compare_id
    sentence_full_setting['focus_id'] = focus_id
    sentence_full_setting['sure'] = sure
    return sentence_full_setting

def get_ordinal_name(name_array):
    return f'from {name_array[0]} to {name_array[-1]}'



def cal_segment_trend(id_array, data, max_value, diff_std_limit = 0.1):
    if len(id_array) != 2:
        return "Not right"
    id_min = min(id_array)
    id_max = max(id_array)
    quantity_array = [datum['q0'] for datum in data['data_array'] if datum['id'] >= id_min and datum['id'] <= id_max]
    return cal_trend_from_quantity_array(quantity_array, max_value)

def cal_trend_from_quantity_array(quantity_array, max_value):
    if len(quantity_array) < 2:
        return 'Not enough'
    degree = ''
    trend = ''
    quantity_array = numpy.asarray(quantity_array)
    length = len(quantity_array)
    begin = quantity_array[0]
    end = quantity_array[1]
    diff = numpy.array([quantity_array[i + 1] - quantity_array[i] for i in range(len(quantity_array) - 1)])
    diff_std = numpy.std(diff)
    diff_mean = numpy.mean(diff)
    diff_std_ratio = diff_std / max_value
    diff_mean_ratio = diff_mean / max_value
    return [diff_std_ratio, diff_mean_ratio]

def get_sentence(segment, setting, data, is_first, object_name = 'the value'):
    begin_id = segment[0]
    end_id = segment[-1]
    begin_name = data['o0'][data['data_array'][begin_id]['o0']]
    end_name = data['o0'][data['data_array'][end_id]['o0']]
    begin_value = data['data_array'][begin_id]['q0']
    end_value = data['data_array'][end_id]['q0']
    diff_number = end_id - begin_id
    return get_ordinal_trend_component(begin_name, begin_value, end_name, end_value, setting, diff_number, is_first)

def get_ordinal_trend_component(begin_name, begin_value, end_name, end_value, std_mean, diff_number, is_first, object_name = 'the value', need_absolute_value = True, is_compare = False):
    diff_std = std_mean[0]
    diff_mean = std_mean[1]
    trend = ""
    degree = ""
    if abs(diff_mean) > 0.13:
        degree = 'greatly'
    elif abs(diff_mean) < 0.04:
        degree = 'slightly'
    if diff_std < 0.1 and diff_number > 2:
        degree = degree + ' with steady steps'
    if diff_mean > 0.03:
        trend = 'increase'
    elif diff_mean < -0.03:
        trend = 'decrease'
    else:
        degree = ''
        if diff_std < 0.1:
            trend = 'keeps stable'
        else:
            trend = 'fluctuates'

    end_value = int(end_value * 100)/100.0

    if is_first:
        if is_compare:
            sentence = f'{object_name} {trend} {degree} during the same period, '
        else:
            sentence = f'{object_name} {trend} {degree} from {begin_name} to {end_name}, '
        return sentence
    else:
        if need_absolute_value:
            return f' then it {trend} {degree} to {end_value} by {end_name}, '
        else:
            return f' then it {trend} {degree} by {end_name}, '

def generate_oq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English'):
    max_value = max([datum['q0'] for datum in data['data_array']])
    if len(focus_id) < 2:
        return []
    segment_array = [[focus_id[i], focus_id[i + 1]] for i in range(len(focus_id) - 1)]
    segment_parameter_array = [cal_segment_trend(segment, data, max_value) for segment in segment_array]
    sentences = []
    sentence = ''
    for i in range(len(segment_array)):
        sentence = sentence + get_sentence(segment_array[i], segment_parameter_array[i], data, i == 0)


    sentences.append(get_sentence_setting('hhh',sentence))
    for i in range(len(sentences)):
        sentences[i]['focus_id'] = focus_id
        sentences[i]['compare_id'] = []
    return sentences

if __name__ == '__main__':
    sentences = get_general_trend()
    for sentence in sentences:
        print(sentence)
