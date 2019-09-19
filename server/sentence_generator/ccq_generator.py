# -*- coding: UTF8 -*-
import json
import numpy
import os
import sys

from oq_generator import get_sentence_setting

chinese_number = ['零','一','二','三','四','五','六','七','八','九','十']
relation_chinese = {'higher': '大', 'lower':'小'}
degree_chinese = {'greatly': '很多', 'slightly':'一点'}




# main_attr: 重要的、有区分度的维度。
# other_attr: 不重要的维度，所有都是一样的维度。
# value_name: 变量的名字：如GDP的值。
def extract_first_second(data, id_array, major_name, second_name):
    num_major = len(data[major_name])
    num_second = len(data[second_name])
    major = [False for i in range(num_major)]
    second = [False for i in range(num_second)]

    for i in id_array:
        # print(i)
        # print("len" + str(len(data['data_array'])))
        assert(i < len(data['data_array']))
        major[data['data_array'][i][major_name]] = True
        second[data['data_array'][i][second_name]] = True

    return major, second

def cal_diff(focus_array, compare_array):
    diff = sum(numpy.array(focus_array) ^ numpy.array(compare_array))
    return diff

def get_id_attribute(data, attr1_name, attr1, attr2_name, attr2):
    for item in data['data_array']:
        if item[attr1_name] == attr1 and item[attr2_name] == attr2:
            return item['id']
    return -1



def compare(focus_array, compare_array): # 这是两个一维数组
    # focus_array = numpy.asarray(focus_array)
    # compare_array = numpy.asarray(compare_array)
    assert(len(compare_array) > 0)
    focus_ave = sum(focus_array) / len(focus_array)
    focus_max = max(focus_array)
    focus_min = min(focus_array)
    compare_ave = sum(compare_array) / len(compare_array)
    compare_max = max(compare_array)
    compare_min = min(compare_array)

    relation = ''
    degree = ''
    range = ''

    ratio = focus_ave * 1.0 / (compare_ave + 0.00001)

    if focus_min > compare_max:
        range = "all"
    elif focus_max < compare_min:
        range = "all"

    if ratio > 1.05:
        relation = "higher"
    elif ratio < 0.95:
        relation = "lower"
    else:
        relation = "same"

    if ratio > 0.9 and ratio < 1.1:
        degree = 'slight'

    if ratio < 0.7 or ratio > 1.5:
        degree = 'greatly'

    return relation, degree, range, ratio

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
                name = str(name) + str(" ")+ str(choose_name[i]) + ", "
            else:
                name = name + choose_name[i] + "、"
        if version == 'English':
            name = str(name) + str(choose_name[-2]) + str(" and ") + str(choose_name[-1])
        else:
            name = name + choose_name[-2] + "与" + choose_name[-1]
        if name[0] == " ":
            name = name[1:]
        return name


def get_name(data, focus_data, compare_data, dimension_length_main, dimension_length_share, version = 'English'):
    focus = []
    compare = []
    share = []

    for i in focus_data:
        focus.append(i[0]['main'])

    for i in focus_data[0]:
        share.append(i['share'])

    for i in compare_data:
        compare.append(i[0]['main'])
    # # print(focus)
    focus_name = get_aggre_name(focus, dimension_length_main, version)
    # # print(focus_name)

    # # print(compare)
    if len(focus) + len(compare) == dimension_length_main and len(compare) > 2:
        compare_name = "others"
        if version == 'Chinese':
            compare_name = "其他的"
    else:
        compare_name = get_aggre_name(compare, dimension_length_main, version)
    # # print(compare_name)

    # # print(share)
    share_name = get_aggre_name(share, dimension_length_share, version)
    # # print(share_name)

    return focus_name, compare_name, share_name

def cal_compare_diff(part_data):
    focus_array = []
    for line in part_data:
        value = []
        for item in line:
            value.append(item['value'])
        value_numpy = numpy.asarray(value)
        variance = numpy.var(value_numpy)
        focus_array.append(variance)
    return focus_array

def compare_diff(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version = 'English'):
    focus_array = cal_compare_diff(focus_data)
    compare_array = cal_compare_diff(compare_data)

    # # print(focus_array, compare_array)
    sentences = []

    relation, degree, range, ratio = compare(focus_array, compare_array)
    if range == "all" and len(focus_array) + len(compare_array) > 2 and len(data[main_dimension]) == len(focus_array) + len(compare_array):
        extreme = "maximum"
        if ratio < 1:
            extreme = "minimum"

        sentence = f"The difference among {share_name} reached its {extreme} in the category of {focus_name}"
        # # print(' '.join(sentence.split()))
        sentences.append(get_sentence_setting('compare_diff', sentence))

    if relation == 'higher' or relation == 'lower':
        relation = relation + " than"
    else:
        degree = "almost"
        relation = "the same as"

    sentence = f"The difference among {share_name} in {focus_name} is {degree} {relation} than {compare_name}"

    sentences.append(get_sentence_setting('compare_diff', sentence))
    return sentences

def cal_compare_1d(part_data):
    focus_array = []
    for line in part_data:
        sum_value = 0
        for item in line:
            sum_value = sum_value + item['value']
        focus_array.append(sum_value)
    return focus_array

def compare_1d(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version = 'English'):
    sentences = []
    focus_array = cal_compare_1d(focus_data)
    compare_array = cal_compare_1d(compare_data)
    relation, degree, range, ratio = compare(focus_array, compare_array)
    unit = data['unit']


    if relation == 'higher' or relation == 'lower':
        relation = relation + " than"
    else:
        degree = "almost"
        relation = "the same as"

    if len(focus_array) == 1:
        sentence = f'In the category of {share_name}, {data["title"]} of {focus_name} is {focus_array[0]} {unit}, which is {degree} {relation} {compare_name}'
        sentences.append(get_sentence_setting('compare', sentence))
        sentences.append(get_sentence_setting('compare_ave', sentence))
        



    # # print(focus_array, compare_array)

    if range == "all" and len(focus_array) + len(compare_array) > 2 and len(data[main_dimension]) == len(focus_array) + len(compare_array):
        extreme = "highest"
        if ratio < 1:
            extreme = "lowest"
        if len(focus_array) > 1:
            sentence = f"{focus_name} has the {extreme} {len(focus_array)} value in {share_name}"
        else:
            sentence = f"{focus_name} is the {extreme} value in the categery of {share_name}"
        # sentence = "the value in {} is the {} {} value in the category of {}".format(focus_name, extreme, len(focus_array), share_name)
        # # print(' '.join(sentence.split()))
        sentences.append(get_sentence_setting('compare', sentence))



    sentence = "the value in {} is {} {} {} in the category of {}".format(focus_name, degree, relation, compare_name, share_name)
    # print(sentence)


    sentences.append(get_sentence_setting('compare', sentence))
    return sentences

def cal_compare_sum(part_data):
    part_array = []
    for line in part_data:
        sum_value = 0
        for item in line:
            sum_value = sum_value + item['value']
        part_array.append(sum_value)
    return part_array



def compare_sum(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version = 'English'):
    focus_array = cal_compare_sum(focus_data)
    compare_array = cal_compare_sum(compare_data)
    # print(focus_data.shape)


    # # print(focus_array, compare_array)
    sentences = []

    relation, degree, range, ratio = compare(focus_array, compare_array)

    if range == "all" and len(focus_array) == 1 and len(data[main_dimension]) == len(focus_array) + len(compare_array):
        extreme = "highest"
        if ratio < 1:
            extreme = "lowest"

        if len(focus_array) > 1:
            if len(compare_array) + len(focus_array) > 2:
                sentence = f"{focus_name} has the {extreme} {len(focus_array)} sum value of {share_name}"
                sentences.append(get_sentence_setting('compare_sum', sentence))
                sentence = f"{focus_name} has the {extreme} {len(focus_array)} average value of {share_name}"
                sentences.append(get_sentence_setting('compare_ave', sentence))
                sentence = f"{focus_name} has the {extreme} {len(focus_array)} value of {share_name}"
                sentences.append(get_sentence_setting('compare_val', sentence))
            else:
                sentence = f"The sum value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_sum', sentence))
                sentence = f"{data['title']} of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_ave', sentence))
                sentence = f"The sum value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_val', sentence))
        else:
            if len(compare_array) > 1:
                sentence = f"{focus_name} has the {extreme} sum value of {share_name}"
                sentences.append(get_sentence_setting('compare_sum', sentence))
                sentence = f"{focus_name} has the {extreme} average value of {share_name}"
                sentences.append(get_sentence_setting('compare_ave', sentence))
                sentence = f"{focus_name} has the {extreme} value of {share_name}"
                sentences.append(get_sentence_setting('compare_val', sentence))
            else:
                sentence = f"The sum value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_sum', sentence))
                sentence = f"The value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_ave', sentence))
                sentence = f"The sum value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
                sentences.append(get_sentence_setting('compare_val', sentence))


        if version == 'Chinese':
            if extreme == 'highest':
                extreme = "大"
            else:
                extreme = "小"
            sentence = f"平均而言，{focus_name}是{share_name}中最{extreme}的"
            sentences.append(get_sentence_setting('compare_sum', sentence))
        if len(focus_array) ==1:
            sentence = f"{focus_name} has sum value of {focus_array[0]} and it's {extreme}"
            sentences.append(get_sentence_setting('compare_sum', sentence))

            sentence = f"{focus_name} has average value of {focus_array[0]/len(focus_data[0])} and it's {extreme}"
            sentences.append(get_sentence_setting('compare_ave', sentence))

        sentence = f"{focus_name} has average value of {focus_array[0]/len(focus_data[0])} and it's {extreme}"
        sentences.append(get_sentence_setting('compare_ave', sentence))




    if relation == 'higher' or relation == 'lower':
        relation = relation + " than"
    else:
        degree = "almost"
        relation = "the same as"

    if len(data[main_dimension]) == len(focus_array) + len(compare_array):
        if len(compare_array) > 1:
            sentence = f'The value of {focus_name} is {degree} {relation} others in {share_name}'
        else:
            sentence = f'The value of {focus_name} is {degree} {relation} {compare_name} in {share_name}'

        sentences.append(get_sentence_setting('compare_ave', sentence, sure = False))

    sentence = f"The sum value of {share_name} in {focus_name} is {degree} {relation} {compare_name}"
    if version == 'Chinese':
        sentence = f"{share_name}的总和在{focus_name}中比{compare_name}{relation_chinese[relation]}{degree_chinese[degree]}"
    # shenme = 11
    # sentence = f'the sum value in a is {shenme}'
    sentences.append(get_sentence_setting('compare_sum', sentence))

    sentence = f"{data['title']} of {focus_name} is {degree} {relation} {compare_name} in the category of {share_name}"

    sentences.append(get_sentence_setting('compare_ave', sentence, sure = False))

    return sentences



def cal_compare_max(part_data):
    focus_array = []
    name_array = []
    for line in part_data:
        max = {}
        max['value'] = 0
        max['name'] = ''
        for item in line:
            if max['value'] < item['value']:
                max['value'] = item['value']
                max['name'] = item['share']
        focus_array.append(max['name'])
    for item in part_data[0]:
        name_array.append(item['share'])


    return focus_array, name_array

def cal_compare_min(part_data):
    focus_array = []
    for line in part_data:
        min = {}
        min['value'] = 999999999
        min['name'] = ''
        for item in line:
            if min['value'] > item['value']:
                min['value'] = item['value']
                min['name'] = item['share']
        focus_array.append(min['name'])
    return focus_array

def compare_max(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version = 'English'):
    focus_array, share_name_array = cal_compare_max(focus_data)
    compare_array, share_name_array = cal_compare_max(compare_data)
    # 当在第一个数组中出现的部分不在第二个数组中出现。
    focus_array = list(set(focus_array))
    compare_array = list(set(compare_array))

    focus_other_array = [name for name in share_name_array if name not in focus_array]
    compare_other_array = [name for name in share_name_array if name not in compare_array]

    # print(share_name)
    focal_max_name = get_aggre_name(focus_array, len(share_name), version)
    focal_other_name = get_aggre_name(focus_other_array, 100, version)
    compare_max_name = get_aggre_name(compare_array, len(share_name), version)
    compare_other_name = get_aggre_name(compare_other_array, len(share_name), version)
    ret = [i for i in focus_array if i in compare_array]
    # # print(focal_max_name)
    # # print(compare_max_name)
    sentences = []
    if len(ret) == 0 and len(focus_array) == 1 and len(compare_array) == 1:
        if len(compare_other_array) < 2:
            sentence = f"{focal_max_name} is higher than {focal_other_name} in {focus_name}, while {compare_max_name} is higher than {compare_other_name} in {compare_name}"
        else:
            sentence = f"{focal_max_name} is the maximum in {focus_name}, while {compare_max_name} is the maximum in {compare_name}"
        sentences.append(get_sentence_setting('compare_max', sentence))
    return sentences

def compare_min(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version = 'English'):
    focus_array = cal_compare_min(focus_data)
    compare_array = cal_compare_min(compare_data)
    # 当在第一个数组中出现的部分不在第二个数组中出现。
    focus_array = list(set(focus_array))
    compare_array = list(set(compare_array))
    # print(share_name)
    focal_max_name = get_aggre_name(focus_array, len(share_name), version)
    compare_max_name = get_aggre_name(compare_array, len(share_name), version)
    ret = [i for i in focus_array if i in compare_array]
    # # print(focal_max_name)
    # # print(compare_max_name)
    sentences = []
    if len(ret) == 0 and len(focus_array) == 1 and len(compare_array) == 1:
        sentence = f"{focal_max_name} is the minimum of {focus_name}, while {compare_max_name} is minimum of {compare_name} "
        sentences.append(get_sentence_setting('compare_min', sentence))
    return sentences


def cal_statistic(data, focus_id, compare_id, main_dimension, share_dimension, main_focus, main_compare, share, major_name, second_name, version = 'English'):
    # print('I am here')
    compare_id = list(set(compare_id).difference(set(focus_id)))

    if len(compare_id) == 0:
        # # print("absolute")
        return generate_ccq_absolute(data, focus_id, major_name, second_name, version)


    main_dimension_length = len(data[main_dimension])
    share_dimension_length = len(data[share_dimension])
    focus_data = []
    compare_data = []
    for i in range(main_dimension_length):
        if main_focus[i]:
            name = data[main_dimension][i]
            value = []
            for j in range(share_dimension_length):
                if share[j]:
                    item = {}
                    data_item = data['data_array'][get_id_attribute(data, main_dimension, i, share_dimension, j)]
                    item["id"] = data_item["id"]
                    item["value"] = data_item["q0"]
                    item["main"] = data[main_dimension][data_item[main_dimension]]
                    item["share"] = data[share_dimension][data_item[share_dimension]]
                    value.append(item)
            focus_data.append(value)

        elif main_compare[i]:
            name = data[main_dimension][i]
            value = []
            for j in range(share_dimension_length):
                if share[j]:
                    item = {}
                    data_item = data['data_array'][get_id_attribute(data, main_dimension, i, share_dimension, j)]
                    item["id"] = data_item["id"]
                    item["value"] = data_item["q0"]
                    item["main"] = data[main_dimension][data_item[main_dimension]]
                    item["share"] = data[share_dimension][data_item[share_dimension]]
                    value.append(item)
            compare_data.append(value)
    dimension_length_main = len(data[main_dimension])
    dimension_length_share = len(data[share_dimension])

    if len(focus_data) == 0 or len(focus_data[0]) == 0:
        return []

    focus_name, compare_name, share_name = get_name(data, focus_data, compare_data, dimension_length_main, dimension_length_share, version )

    focus_id = []
    compare_id = []
    for line in focus_data:
        for item in line:
            # print(item)
            focus_id.append(item['id'])

    for line in compare_data:
        for item in line:
            compare_id.append(item['id'])


    if (len(compare_id) == 0):
        return generate_ccq_absolute(data, focus_id, major_name, second_name, version)

    sentences = []
    if sum(share) == 1: # 其中一个维度是1那就尴尬了哈哈哈哈哈
        sentences = sentences + compare_1d(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version)
    else:
        sentences = sentences + compare_sum(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version)
        sentences = sentences + compare_diff(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version)
        sentences = sentences + compare_max(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version)
        sentences = sentences + compare_min(data, focus_data, compare_data, focus_name, compare_name, share_name, main_dimension, version)

    for sentence in sentences:
        sentence['compare_id'] = compare_id
        sentence['focus_id'] = focus_id
    return sentences


# 获取数据类型
def get_data_type(data):
    data_attr = data['data_array'][0].keys()
    if 'c0' in data_attr and 'c1' in data_attr:
        return 'ccq'
    elif 'c0' in data_attr and 'o0' in data_attr:
        return 'ocq'

# 获取新的focus
# def get_new_focus_id(data, focus_id):


# single: The value of {upper_secondary} in {USA} is {value}
def cal_ccq_single_sentence(data, focus_id, focus_main_name, focus_second_name):
    sentences = []
    value = data['data_array'][focus_id[0]]['q0']
    sentence = f'The value of {focus_main_name} in {focus_second_name} is {value}'
    sentences.append(get_sentence_setting('absolute_single', sentence))
    return sentences

def cal_ccq_sum_sentence(data, focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name):
    sum = 0
    for i in focus_id:
        sum = sum + data['data_array'][i]['q0']
    sentences = []
    unit = data['unit']
    sentence = f'The sum value of {focus_main_name} in {focus_second_name} is {sum} {unit}'
    sentences.append(get_sentence_setting('absolute_sum', sentence))
    return sentences

def cal_ccq_average_sentence(data, focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name):
    sum = 0
    for i in focus_id:
        sum = sum + data['data_array'][i]['q0']
    average = sum / len(focus_id)
    sentences = []
    unit = data['unit']

    sentence = f'The average value of {focus_main_name} in {focus_second_name} is {average} {unit}'
    sentences.append(get_sentence_setting('absolute_average', sentence))
    return sentences

def cal_ccq_count_sentence(data, focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name):
    values = [data['data_array'][i]['q0'] for i in focus_id]
    value_max = max(values)
    value_min = min(values)
    sentences = []
    unit = data['unit']

    sentence = f"The value of {focus_second_name} in {focus_main_name} ranges from {value_min} to {value_max} {unit}"
    sentences.append(get_sentence_setting('absolute_range', sentence))

    # higher than:
    if sum(focus_main_dim) == len(focus_main_dim):
        sentence = f"The value of {focus_second_name} ranges from {value_min} to {value_max} {unit}"
    else:
        sentence = f"The value of {focus_main_name} in {focus_second_name} ranges from {value_min} to {value_max} {unit}"
    sentences.append(get_sentence_setting('absolute_range', sentence))

    if sum(focus_main_dim) == len(focus_main_dim):
        sentence = f"All values of {focus_second_name} is higher than {value_min} {unit}"
    else:
        sentence = f"All values of {focus_main_name} in {focus_second_name} is higher than {value_min} {unit}"
    sentences.append(get_sentence_setting('absolute_higher', sentence))

    if sum(focus_main_dim) == len(focus_main_dim):
        sentence = f"All values of {focus_second_name} is lower than {value_max} {unit}"
    else:
        sentence = f"All values of {focus_main_name} in {focus_second_name} is lower than {value_max} {unit}"
    sentences.append(get_sentence_setting('absolute_lower', sentence))

    return sentences


# 计算ccq类型的绝对值：
def cal_ccq_absolute_sentences(data, focus_id, major_name = 'c0', second_name = 'c1'):
    sentences = []

    number_dimension0 = len(data[major_name])
    number_dimension1 = len(data[second_name])
    dimension0 = [0 for i in range(number_dimension0)]
    dimension1 = [0 for i in range(number_dimension1)]
    for id in focus_id:
        item = data['data_array'][id]
        dimension0[item[major_name]] = 1
        dimension1[item[second_name]] = 1

    num_occupy_0 = sum(dimension0)
    num_occupy_1 = sum(dimension1)
    if num_occupy_0 < num_occupy_1:
        main_dim_name = second_name
        second_dim_name = major_name
        focus_main_dim = dimension1
        focus_second_dim = dimension0
    else:
        main_dim_name = major_name
        second_dim_name = second_name
        focus_main_dim = dimension0
        focus_second_dim = dimension1

    focus_main_num = sum(focus_main_dim)
    focus_second_num = sum(focus_second_dim)

    new_focus_id = []
    for item in data['data_array']:
        if dimension0[item[major_name]] > 0 and dimension1[item[second_name]] > 0 :
            new_focus_id.append(item['id'])
    # print(dimension0)
    # print(dimension1)
    # print(new_focus_id)
    focus_main_name_array = [data[main_dim_name][i] for i in range(len(data[main_dim_name])) if focus_main_dim[i] > 0  ]
    focus_second_name_array = [data[second_dim_name][i] for i in range(len(data[second_dim_name])) if focus_second_dim[i] > 0 ]
    # print(f'focus_main_name: {focus_main_name_array}')
    # print(focus_second_name_array)
    focus_main_name = get_aggre_name(focus_main_name_array, len(data[main_dim_name]))
    focus_second_name = get_aggre_name(focus_second_name_array, len(data[second_dim_name]))
    # print(focus_main_name)
    # print(focus_second_name)
    # The value of {upper_secondary} in {USA} is {value}
    sentences = []
    if focus_main_num == 1 and focus_second_num == 1:
        sentences = sentences + cal_ccq_single_sentence(data, new_focus_id, focus_main_name, focus_second_name)
    # The sum value of {those categories} in {USA} is {value}
    else:
        sentences = sentences + cal_ccq_sum_sentence(data, new_focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name)
        sentences = sentences + cal_ccq_average_sentence(data, new_focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name)
        sentences = sentences + cal_ccq_count_sentence(data, new_focus_id, focus_main_dim, focus_second_dim, focus_main_name, focus_second_name)

    add_absolute_ids(sentences, new_focus_id)
    # print(sentences)
    return sentences

def add_absolute_ids(sentences, focus_id = [], compare_id = []):
    for sentence in sentences:
        sentence['focus_id'] = focus_id
        sentence['compare_id'] = compare_id
    return sentences
# 获得计算绝对值的句子
def generate_ccq_absolute(data, focus_id, major_name, second_name, version = 'English'):
    # print(focus_id)
    sentences = []
    sentences = cal_ccq_absolute_sentences(data, focus_id, major_name, second_name)
    return sentences

def generate_ccq_sentence(data, focus_id, compare_id, major_name, second_name, version = 'English'):
    num_major = len(data[major_name])
    num_second = len(data[second_name])
    if len(focus_id) == 0 and len(compare_id) == 0 :
        return []
    if (len(focus_id) == 0):
        focus_id = compare_id
        compare_id = []
    focus_major, focus_second = extract_first_second(data, focus_id, major_name, second_name)
    compare_major, compare_second = extract_first_second(data, compare_id, major_name, second_name)
    major_diff = cal_diff(focus_major, compare_major)
    second_diff = cal_diff(focus_second, compare_second)
    main_dimension_name = major_name
    main_focus = focus_major
    main_compare = compare_major
    share_dimension_name = second_name
    share = numpy.array(compare_second) & numpy.array(focus_second)
    if (major_diff < second_diff):
        main_dimension_name = second_name
        main_focus = focus_second
        main_compare = compare_second
        share_dimension_name = major_name
        share = numpy.array(compare_major) & numpy.array(focus_major)
    else:
        main_dimension_name = major_name
        share_dimension_name = second_name
    return cal_statistic(data, focus_id, compare_id, main_dimension_name, share_dimension_name, main_focus, main_compare, share, major_name, second_name, version)
