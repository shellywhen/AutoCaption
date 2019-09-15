import json
import numpy
import random
from basic_change import add_color, add_type, get_data_type, del_long_name, add_vis_type
from ocq_data_generator import add_small_value, add_small_random

def get_special_ratio():
    if numpy.random.random() > 0.5:
        special_ratio = abs(numpy.random.normal(0, 0.2)) + 1.05
    else:
        special_ratio = abs(0.95 - abs(numpy.random.normal(0, 0.2)))

    return special_ratio
def generate_rule_data(data_type, vis_type, rule_type):
    if data_type == 'ocq':
        return generate_ocq_rule_data(vis_type, rule_type)

def get_special_list(category_num, max_num = 100):
    max_num = min(max_num, category_num/2) + 1
    special_num = numpy.random.randint(1, max_num)
    special_list = [i for i in range(category_num)]
    random.shuffle(special_list)
    special_list = special_list[:special_num]
    return special_list

def interpolate_data(data_content): # random

    for line_index, line in enumerate(data_content):
        keys = list(line.keys())
        for i in range(len(keys) - 1):

            begin_index = keys[i]
            end_index = keys[i + 1]
            # print(f'begin_index: {begin_index} end_index: {end_index}')
            begin_value = line[begin_index]
            end_value = line[end_index]
            # print(f'Begin_index: {begin_index}, value = {line[begin_index]}')
            # print(f'end_index: {end_index}, value = {line[end_index]}')
            random_list = sorted([numpy.random.random() for i in range(end_index - begin_index + 1)])
            min_value = min(random_list)
            max_value = max(random_list)
            random_list = [(value - min_value)/(max_value - min_value) for value in random_list]

            for inter_index in range(begin_index + 1, end_index):
                line[inter_index] = random_list[(inter_index - begin_index)] * (end_value - begin_value) + begin_value
                # print(f'Inter_index: {inter_index}, value = {line[inter_index]}')
        data_content[line_index] = line
    numpy_data = change_dict_numpy(data_content)

    # print(numpy_data)
    return numpy_data

def interpolate_data_linear(data_content):

    for line_index, line in enumerate(data_content):
        keys = list(line.keys())
        for i in range(len(keys) - 1):

            begin_index = keys[i]
            end_index = keys[i + 1]
            # print(f'begin_index: {begin_index} end_index: {end_index}')
            begin_value = line[begin_index]
            end_value = line[end_index]
            # print(f'Begin_index: {begin_index}, value = {line[begin_index]}')
            # print(f'end_index: {end_index}, value = {line[end_index]}')
            random_list = sorted([numpy.random.random() for i in range(end_index - begin_index + 1)])
            min_value = min(random_list)
            max_value = max(random_list)
            random_list = [(value - min_value)/(max_value - min_value) for value in random_list]

            for inter_index in range(begin_index + 1, end_index):
                line[inter_index] = ((end_index - inter_index) * begin_value + (inter_index - begin_index) * end_value) / (end_index - begin_index)
                # print(f'Inter_index: {inter_index}, value = {line[inter_index]}')
        data_content[line_index] = line
    numpy_data = change_dict_numpy(data_content)
    min_value = numpy.min(numpy_data)
    if (min_value < 0.05):
        numpy_data = numpy_data + 0.05 - min_value
    # print(numpy_data)
    return numpy_data

def change_dict_numpy(data_content):
    data = []
    for line in data_content:
        line_keys = list(set(list(line.keys())))
        # print(line_keys)
        line_list = []
        for i in line_keys:
            line_list.append(line[i])
        data.append(line_list)
    data = numpy.asarray(data)
    return data

def generate_data_array(data_full):
    id = 0
    data_array = []
    for cat_id, cat in enumerate(data_full):
        for ord_id, value in enumerate(cat):
            datum = {}
            datum['c0'] = cat_id
            datum['id'] = id
            datum['o0'] = ord_id
            datum['q0'] = value
            id = id + 1
            data_array.append(datum)
    return data_array
def generate_pack_data(data_metrics):
    cat_name_array = ['A', 'B', 'C', 'D', 'E', 'F']
    random.shuffle(cat_name_array)
    category_num, ordinal_num = data_metrics.shape
    data = {}
    data['title'] = 'The Value'
    data['unit'] = ''
    data['c0'] = cat_name_array[:category_num]
    data['o0'] = [str(2010 + i) for i in range(ordinal_num)]
    data['data_array'] = generate_data_array(data_metrics)
    data = add_type(data)
    # data = add_small_random(data)

    return data

def change_coordinate_to_id(coor, ordinal_num):
    return coor[0] * ordinal_num + coor[1]


def get_big_small_index(array):
    sorted_array = sorted(array)
    diff = [sorted_array[i + 1] - sorted_array[i] for i in range(len(array) - 1)]
    max_diff_index = diff.index(max(diff))
    small_max = sorted_array[max_diff_index]
    big_min = sorted_array[max_diff_index + 1]
    small_index = [array.index(value) for value in array if value <= small_max]
    big_index = [array.index(value) for value in array if value >= big_min]
    return small_index, big_index

def judge_big_diff(data_full, small_index, big_index):
    big_min = min([min(data_full[i]) for i in big_index])
    small_max = max([max(data_full[i]) for i in small_index])
    return big_min - small_max

def judge_special(before, after, max_value = 1):
    if abs((before - after)/(before + after)) > 0.5 and abs(before) + abs(after) > 0.05:
        return True
    else:
        return False

def extract_trend_special(value_array):
    if len(value_array) <= 2:
        return [i for i in range(len(value_array))]

    max_value = max(value_array)
    value_array = [value / max_value for value in value_array]

    index_special = []
    index_special.append(0)
    diff_ratio = [{'index': i, 'diff_ratio': abs(value_array[i - 1] + value_array[i + 1] - value_array[i] * 2)} for i in range(1, len(value_array) - 1)]
    def get_diff_ratio(item):
        return item['diff_ratio']
    def get_index(item):
        return item['index']
    diff_ratio_sorted = sorted(diff_ratio, key = get_diff_ratio, reverse = True)
    number = len(diff_ratio_sorted)
    if number == 1:
        if judge_special(value_array[1] - value_array[0], value_array[2] - value_array[1]):
            index_special.append(1)
    else:
        print(diff_ratio_sorted)
        diff_ratio_chosen = diff_ratio_sorted[:int(number / 2)]
        print(diff_ratio_chosen)
        diff_ratio_chosen = sorted(diff_ratio_chosen, key = get_index)
        for item in diff_ratio_chosen:
            if judge_special(value_array[item['index']] - value_array[item['index'] - 1], value_array[item['index'] + 1] - value_array[item['index']]):
                index_special.append(item['index'])
    index_special.append(len(value_array) - 1)
    print(index_special)
    return index_special

def extract_trend_special_old(value_array):
    # uniform:
    if len(value_array) <= 2:
        return [i for i in range(len(value_array))]

    max_value = max(value_array)
    value_array = [value / max_value for value in value_array]
    index_special = []
    index_special.append(0)
    for i in range(1, len(value_array) - 1):
        if judge_special(value_array[i] - value_array[i-1], value_array[i+1] - value_array[i]):
            index_special.append(i)
    index_special.append(len(value_array) - 1)
    return index_special

def get_begin_end_value(begin_value, trend):
    end_value = begin_value * (1 + trend / 20) + trend / 50 # relative and absolute part
    if end_value < 0:
        add_value = 0.02 - end_value
        begin_value = begin_value + add_value
        end_value = end_value + add_value
    return begin_value, end_value

def generate_single_complex_stack_data(rule_type, vis_type = 'load_stack_bar_chart', ordinal_min = 5, ordinal_max = 10, category_min = 2, category_max = 6):

        while True:
            ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
            category_num = numpy.random.randint(category_min, category_max)
            if ordinal_num * category_num < 30:
                break;
        # print("category_num")
        # print(category_num)
        begin_num = numpy.random.random()
        cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
        # 归一化，最大值为1
        max_cat_begin_value = max(cat_begin_value)
        cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

        small_cat, big_cat = get_big_small_index(cat_begin_value)
        #
        while True:
            normal_trend = numpy.random.uniform(-10, 10)
            special_trend = numpy.random.uniform(-10, 10)
            if abs(normal_trend - special_trend) > 7 and abs(normal_trend) > 0.5 and abs(special_trend) > 0.5:
                break
        # print(normal_trend)
        # print(special_trend)
        special_list = get_special_list(category_num, max_num  = 1)
        # print(f'special_list: {special_list}')
        data_content = []
        focus_coor = []
        compare_coor = []
        sentences = []
        need_complex_trend = False

        for i in range(category_num):
            this_focus = {}
            this_focus[0] = cat_begin_value[i]
            special_index = i
            begin_value = this_focus[0]
            if special_index in special_list:
                if begin_value > 0.2 * sum(cat_begin_value) or special_index == 0:
                    need_complex_trend = True
                    middle_index = numpy.random.randint(1, ordinal_num - 1)
                    end_value = this_focus[0] * (numpy.random.uniform(0.5, 1.8))
                    if numpy.random.random() > 0.5:
                        middle_value = max(begin_value, end_value) * numpy.random.uniform(1.2, 2)
                    else:
                        middle_value = min(begin_value, end_value) * numpy.random.uniform(0.3, 0.8)

                    this_focus[middle_index] = middle_value

                    this_focus[ordinal_num - 1] = end_value
                    focus_coor.append([special_index, 0])
                    focus_coor.append([special_index, middle_index])
                    focus_coor.append([special_index, ordinal_num - 1])
                else:
                    trend = special_trend
                    focus_coor.append([i, 0])
                    focus_coor.append([i, ordinal_num - 1])
                    this_focus[0], this_focus[ordinal_num - 1] = get_begin_end_value(begin_value, trend)
                # print(f'this_focus: {this_focus}')
            else:
                trend = normal_trend
                compare_coor.append([special_index, 0])
                compare_coor.append([special_index, ordinal_num - 1])
                begin_value, end_value = get_begin_end_value(begin_value, trend)
                this_focus[0] = begin_value
                this_focus[ordinal_num - 1] = end_value
            data_content.append(this_focus)

        if need_complex_trend:
            focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
            compare_id = []
            sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'all_trend'})


        if 2 * len(special_list) < category_num:
            focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
            compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
            sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})


        data_full = interpolate_data(data_content)
        diff_max = judge_big_diff(data_full, small_cat, big_cat)

        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]

        index_special = extract_trend_special(sum_value)
        focus_id = []
        compare_id = []
        for i in range(category_num):
            for j in range(ordinal_num):
                if j in index_special:
                    focus_id.append(change_coordinate_to_id([i,j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'sum_trend'})

        for i in range(category_num):
            average_percent = sum([data_full[i][j] / sum_value[j] for j in range(ordinal_num)])


        data = generate_pack_data(data_full)
        data = add_color(data)
        data = add_small_value(data)
        data['vis_type'] = vis_type
        data['major_name'] = 'o0'
        data['second_name'] = 'c0'
        data['pre_gen_focus'] = sentences

        return data



# 基础款stack——data
def generate_ocq_stack_data(rule_type, vis_type = 'load_stack_bar_chart', ordinal_min = 3, ordinal_max = 10, category_min = 2, category_max = 6):

        while True:
            ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
            category_num = numpy.random.randint(category_min, category_max)
            if ordinal_num * category_num < 30:
                break;
        # print("category_num")
        # print(category_num)
        begin_num = numpy.random.random()
        cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
        # 归一化，最大值为1
        max_cat_begin_value = max(cat_begin_value)
        cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

        small_cat, big_cat = get_big_small_index(cat_begin_value)
        #
        while True:
            normal_trend = numpy.random.uniform(-10, 10)
            special_trend = numpy.random.uniform(-10, 10)
            if abs(normal_trend - special_trend) > 7 and abs(normal_trend) > 0.5 and abs(special_trend) > 0.5:
                break
        # print(normal_trend)
        # print(special_trend)
        special_list = get_special_list(category_num)
        # print(f'special_list: {special_list}')
        data_content = []
        focus_coor = []
        compare_coor = []

        for i in range(category_num):
            this_focus = {}
            this_focus[0] = cat_begin_value[i]
            if i in special_list:
                trend = special_trend
                focus_coor.append([i, 0])
                focus_coor.append([i, ordinal_num - 1])
            else:
                trend = normal_trend
                compare_coor.append([i, 0])
                compare_coor.append([i, ordinal_num - 1])
            this_focus[ordinal_num - 1] = this_focus[0] * (1 + trend/10.0)
            data_content.append(this_focus)
        sentences = []
        if 2 * len(special_list) < category_num or category_num == 2:
            focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
            compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
            sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})


        data_full = interpolate_data(data_content)
        diff_max = judge_big_diff(data_full, small_cat, big_cat)

        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]

        index_special = extract_trend_special(sum_value)
        focus_id = []
        compare_id = []
        for i in range(category_num):
            for j in range(ordinal_num):
                if j in index_special:
                    focus_id.append(change_coordinate_to_id([i,j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'sum_trend'})

        data = generate_pack_data(data_full)
        data = add_color(data)
        data = add_small_value(data)
        data['vis_type'] = vis_type
        data['major_name'] = 'o0'
        data['second_name'] = 'c0'
        data['pre_gen_focus'] = sentences

        return data
# 其中有一个地方有特殊值： stack 的
def generate_single_special_stack_data(rule_type, vis_type = 'load_stack_bar_chart', ordinal_min = 3, ordinal_max = 10, category_min = 2, category_max = 6):

        while True:
            ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
            category_num = numpy.random.randint(category_min, category_max)
            if ordinal_num * category_num < 30:
                break;
        # print("category_num")
        # print(category_num)
        begin_num = numpy.random.random()
        cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
        # 归一化，最大值为1
        max_cat_begin_value = max(cat_begin_value)
        cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

        small_cat, big_cat = get_big_small_index(cat_begin_value)
        #
        while True:
            normal_trend = numpy.random.uniform(-10, 10)
            special_trend = numpy.random.uniform(-10, 10)
            if abs(normal_trend - special_trend) > 7 and abs(normal_trend) > 0.5 and abs(special_trend) > 0.5:
                break
        # print(normal_trend)
        # print(special_trend)
        special_list = get_special_list(category_num)
        # print(f'special_list: {special_list}')
        data_content = []
        focus_coor = []
        compare_coor = []

        for i in range(category_num):
            this_focus = {}
            this_focus[0] = cat_begin_value[i]
            if i in special_list:
                trend = special_trend
                focus_coor.append([i, 0])
                focus_coor.append([i, ordinal_num - 1])
            else:
                trend = normal_trend
                compare_coor.append([i, 0])
                compare_coor.append([i, ordinal_num - 1])
            this_focus[ordinal_num - 1] = this_focus[0] * (1 + trend/10.0)
            data_content.append(this_focus)
        sentences = []
        if 2 * len(special_list) < category_num or category_num == 2:
            focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
            compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
            sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})



        data_full = interpolate_data(data_content)
        diff_max = judge_big_diff(data_full, small_cat, big_cat)

        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]

        if ordinal_num > 4:
            special_cat = numpy.random.randint(category_num)
            special_ord = numpy.random.randint(1, ordinal_num -1)
            special_ratio = get_special_ratio()
            if special_ratio > 1:
                original_value = data_full[special_cat][special_ord]
                current_value = max(data_full[special_cat][special_ord - 1], data_full[special_cat][special_ord + 1]) * special_ratio
                data_full[special_cat][special_ord] = current_value
                data_diff = abs(current_value - original_value)
            else:
                original_value = data_full[special_cat][special_ord]
                current_value = min(data_full[special_cat][special_ord - 1], data_full[special_cat][special_ord + 1]) * special_ratio
                data_full[special_cat][special_ord] = current_value
                data_diff = abs(current_value - original_value)

            if data_diff > sum(cat_begin_value) * 0.07:
                diff_ratio_this = abs(data_full[special_cat][special_ord + 1] + data_full[special_cat][special_ord - 1] - 2 * data_full[special_cat][special_ord])
                if (special_ord == 1):
                    diff_ratio_previous = 0
                else:
                    diff_ratio_previous = abs(data_full[special_cat][special_ord] + data_full[special_cat][special_ord - 2] - 2 * data_full[special_cat][special_ord - 1])
                if (special_ord == ordinal_num - 2):
                    diff_ratio_next = 0
                else:
                    diff_ratio_next = abs(data_full[special_cat][special_ord] + data_full[special_cat][special_ord + 2] - 2 * data_full[special_cat][special_ord + 1])
                if diff_ratio_previous > diff_ratio_next and diff_ratio_previous > diff_ratio_this:
                    special_ord = special_ord - 1
                elif diff_ratio_next > diff_ratio_previous and diff_ratio_next > diff_ratio_this:
                    special_ord = special_ord + 1

                focus_id = []
                compare_id = []
                focus_id.append(change_coordinate_to_id([special_cat, special_ord - 1], ordinal_num))
                focus_id.append(change_coordinate_to_id([special_cat, special_ord], ordinal_num))
                focus_id.append(change_coordinate_to_id([special_cat, special_ord + 1], ordinal_num))
                sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'local_trend'})

        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]
        index_special = extract_trend_special(sum_value)
        focus_id = []
        compare_id = []
        for i in range(category_num):
            for j in range(ordinal_num):
                if j in index_special:
                    focus_id.append(change_coordinate_to_id([i,j], ordinal_num))



        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'sum_trend'})

        data = generate_pack_data(data_full)
        data = add_color(data)
        data = add_small_value(data)
        data['vis_type'] = vis_type
        data['major_name'] = 'o0'
        data['second_name'] = 'c0'
        data['pre_gen_focus'] = sentences

        return data

# 其中有一个地方有特殊值： 所有的stack
def generate_all_special_stack_data(rule_type, vis_type = 'load_stack_bar_chart', ordinal_min = 5, ordinal_max = 10, category_min = 2, category_max = 6):

        while True:
            ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
            category_num = numpy.random.randint(category_min, category_max)
            if ordinal_num * category_num < 30:
                break;
        # print("category_num")
        # print(category_num)
        begin_num = numpy.random.random()
        cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
        # 归一化，最大值为1
        max_cat_begin_value = max(cat_begin_value)
        cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

        small_cat, big_cat = get_big_small_index(cat_begin_value)
        #
        while True:
            normal_trend = numpy.random.uniform(-10, 10)
            special_trend = numpy.random.uniform(-10, 10)
            if abs(normal_trend - special_trend) > 7 and abs(normal_trend) > 0.5 and abs(special_trend) > 0.5:
                break
        # print(normal_trend)
        # print(special_trend)
        special_list = get_special_list(category_num)
        # print(f'special_list: {special_list}')
        data_content = []
        focus_coor = []
        compare_coor = []

        for i in range(category_num):
            this_focus = {}
            this_focus[0] = cat_begin_value[i]
            if i in special_list:
                trend = special_trend
                focus_coor.append([i, 0])
                focus_coor.append([i, ordinal_num - 1])
            else:
                trend = normal_trend
                compare_coor.append([i, 0])
                compare_coor.append([i, ordinal_num - 1])
            this_focus[ordinal_num - 1] = this_focus[0] * (1 + trend/10.0)
            data_content.append(this_focus)
        sentences = []
        if 2 * len(special_list) < category_num or category_num == 2:
            focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
            compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
            sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})



        data_full = interpolate_data(data_content)
        diff_max = judge_big_diff(data_full, small_cat, big_cat)
        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]




        special_ord = numpy.random.randint(1, ordinal_num - 1)
        special_ratio = get_special_ratio()
        if special_ratio > 1:
            special_ratio = special_ratio * max(sum_value[special_ord - 1], sum_value[special_ord + 1]) / sum_value[special_ord]
        else:
            special_ratio = special_ratio * min(sum_value[special_ord - 1], sum_value[special_ord + 1]) / sum_value[special_ord]

        diff_ratio_this = abs(sum_value[special_ord + 1] + sum_value[special_ord - 1] - 2 * sum_value[special_ord])
        if (special_ord == 1):
            diff_ratio_previous = 0
        else:
            diff_ratio_previous = abs(sum_value[special_ord] + sum_value[special_ord - 2] - 2 * sum_value[special_ord - 1])
        if (special_ord == ordinal_num - 2):
            diff_ratio_next = 0
        else:
            diff_ratio_next = abs(sum_value[special_ord] + sum_value[special_ord + 2] - 2 * sum_value[special_ord + 1])
        if diff_ratio_previous > diff_ratio_next and diff_ratio_previous > diff_ratio_this:
            special_ord = special_ord - 1
        elif diff_ratio_next > diff_ratio_previous and diff_ratio_next > diff_ratio_this:
            special_ord = special_ord + 1

        focus_id = []
        compare_id = []
        for i in range(category_num):
            data_full[i][special_ord] = data_full[i][special_ord] * special_ratio
            focus_id.append(change_coordinate_to_id([i, special_ord - 1], ordinal_num))
            focus_id.append(change_coordinate_to_id([i, special_ord], ordinal_num))
            focus_id.append(change_coordinate_to_id([i, special_ord + 1], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'local_sum_trend'})
        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'local_trend'})

        sum_value = [sum([data_full[i][j] for i in range(category_num)]) for j in range(ordinal_num)]
        index_special = extract_trend_special(sum_value)
        focus_id = []
        compare_id = []
        for i in range(category_num):
            for j in range(ordinal_num):
                if j in index_special:
                    focus_id.append(change_coordinate_to_id([i,j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'sum_trend'})

        data = generate_pack_data(data_full)
        data = add_color(data)
        data = add_small_value(data)
        data['vis_type'] = vis_type
        data['major_name'] = 'o0'
        data['second_name'] = 'c0'
        data['pre_gen_focus'] = sentences

        return data

# 其中有一个项比较复杂，其余的保持正常，
def generate_single_complex_data(rule_type, vis_type = 'load_group_bar_chart', ordinal_min = 3, ordinal_max = 10, category_min = 2, category_max = 6, main_dim = 'c0', second_dim = 'o0'):
    while True:
        ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
        category_num = numpy.random.randint(category_min, category_max)
        if ordinal_num * category_num < 30:
            break;
    # print("category_num")
    # print(category_num)
    begin_num = numpy.random.random()
    cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
    # 归一化，最大值为1
    max_cat_begin_value = max(cat_begin_value)
    cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

    small_cat, big_cat = get_big_small_index(cat_begin_value)
    normal_trend = numpy.random.uniform(-10, 10)
    # print(normal_trend)
    special_list = get_special_list(category_num, max_num = 1)
    data_content = []
    focus_coor = []
    compare_coor = []
    for i in range(category_num):
        this_focus = {}
        this_focus[0] = cat_begin_value[i]
        if i in special_list:
            begin_value = this_focus[0]
            middle_index = numpy.random.randint(1, ordinal_num - 1)
            end_value = this_focus[0] * (numpy.random.uniform(0.5, 1.8))
            if numpy.random.random() > 0.5:
                middle_value = max(begin_value, end_value) * numpy.random.uniform(1.2, 2)
            else:
                middle_value = min(begin_value, end_value) * numpy.random.uniform(0.3, 0.8)

            this_focus[middle_index] = middle_value

            this_focus[ordinal_num - 1] = end_value

            focus_coor.append([i, 0])
            focus_coor.append([i, middle_index])
            focus_coor.append([i, ordinal_num - 1])
            # print(f'this_focus: {this_focus}')
        else:
            trend = normal_trend
            compare_coor.append([i, 0])
            compare_coor.append([i, ordinal_num - 1])
            this_focus[ordinal_num - 1] = this_focus[0] * (1 + trend/10.0)
        data_content.append(this_focus)



    focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
    compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
    sentences = []
    sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})

    data_full = interpolate_data(data_content)
    diff_max = judge_big_diff(data_full, small_cat, big_cat)
    if diff_max > 0.1:
        focus_id = []
        compare_id = []
        for i in range(category_num):
            if i in small_cat:
                for j in range(ordinal_num):
                    focus_id.append(change_coordinate_to_id([i, j], ordinal_num))
            elif i in big_cat:
                for j in range(ordinal_num):
                    compare_id.append(change_coordinate_to_id([i, j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_ave'})


    data = generate_pack_data(data_full)
    data = add_color(data)
    data = add_small_value(data)
    data['vis_type'] = vis_type
    data['major_name'] = 'c0'
    data['second_name'] = 'o0'
    data['pre_gen_focus'] = sentences
    return data

# 有个蜜汁凸起
def generate_a_special_prominent(rule_type, vis_type = 'load_group_bar_chart', ordinal_min = 4, ordinal_max = 10, category_min = 2, category_max = 6, main_dim = 'c0', second_dim = 'o0'):
    while True:
        ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
        category_num = numpy.random.randint(category_min, category_max)
        if ordinal_num * category_num < 30:
            break;
    # print("category_num")
    # print(category_num)
    begin_num = numpy.random.random()
    cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
    # 归一化，最大值为1
    max_cat_begin_value = max(cat_begin_value)
    cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

    small_cat, big_cat = get_big_small_index(cat_begin_value)

    normal_trend = numpy.random.uniform(-10, 10)

    data_content = []
    focus_coor = []
    for i in range(category_num):
        this_focus = {}
        this_focus[0] = cat_begin_value[i]
        trend = normal_trend
        focus_coor.append([i, 0])
        focus_coor.append([i, ordinal_num - 1])
        this_focus[0], this_focus[ordinal_num - 1] = get_begin_end_value(this_focus[0], trend)
        data_content.append(this_focus)


    focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
    compare_id = []
    sentences = []
    sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'all_trend'})


    data_full = interpolate_data(data_content)
    special_list = get_special_list(category_num, max_num = 1)
    focus_id = []
    compare_id = []
    special_ord = numpy.random.randint(1, ordinal_num - 1)
    special_ratio = get_special_ratio()
    for i in range(category_num):
        if i in special_list:
            if special_ratio > 1:
                data_full[i][special_ord] = max(data_full[i][special_ord - 1], data_full[i][special_ord + 1]) * special_ratio
            else:
                data_full[i][special_ord] = min(data_full[i][special_ord - 1], data_full[i][special_ord + 1]) * special_ratio
            # focus_id.append(change_coordinate_to_id([i, 0],ordinal_num))
            special_cat = i
            diff_ratio_this = abs(data_full[special_cat][special_ord + 1] + data_full[special_cat][special_ord - 1] - 2 * data_full[special_cat][special_ord])
            if (special_ord == 1):
                diff_ratio_previous = 0
            else:
                diff_ratio_previous = abs(data_full[special_cat][special_ord] + data_full[special_cat][special_ord - 2] - 2 * data_full[special_cat][special_ord - 1])
            if (special_ord == ordinal_num - 2):
                diff_ratio_next = 0
            else:
                diff_ratio_next = abs(data_full[special_cat][special_ord] + data_full[special_cat][special_ord + 2] - 2 * data_full[special_cat][special_ord + 1])
            if diff_ratio_previous > diff_ratio_next and diff_ratio_previous > diff_ratio_this:
                special_ord = special_ord - 1
            elif diff_ratio_next > diff_ratio_previous and diff_ratio_next > diff_ratio_this:
                special_ord = special_ord + 1
            focus_id.append(change_coordinate_to_id([i, special_ord - 1], ordinal_num))
            focus_id.append(change_coordinate_to_id([i, special_ord], ordinal_num))
            focus_id.append(change_coordinate_to_id([i, special_ord + 1], ordinal_num))
            # focus_id.append(change_coordinate_to_id([i, ordinal_num - 1],ordinal_num))
    focus_id = list(set(focus_id))
    sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'local_trend'})

    diff_max = judge_big_diff(data_full, small_cat, big_cat)
    if diff_max > 0.1:
        focus_id = []
        compare_id = []
        for i in range(category_num):
            if i in small_cat:
                for j in range(ordinal_num):
                    focus_id.append(change_coordinate_to_id([i, j], ordinal_num))
            elif i in big_cat:
                for j in range(ordinal_num):
                    compare_id.append(change_coordinate_to_id([i, j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_ave'})

    data = generate_pack_data(data_full)
    data = add_color(data)
    data = add_small_value(data)
    data['vis_type'] = vis_type

    main_dim = 'c0'
    second_dim = 'o0'

    data['major_name'] = main_dim
    data['second_name'] = second_dim
    data['pre_gen_focus'] = sentences

    return data


# c0 is main and o0 is second.
def generate_ocq_group_data(rule_type, vis_type = 'load_group_bar_chart', ordinal_min = 3, ordinal_max = 10, category_min = 2, category_max = 6, main_dim = 'c0', second_dim = 'q0'):
    while True:
        ordinal_num = numpy.random.randint(ordinal_min, ordinal_max)
        category_num = numpy.random.randint(category_min, category_max)
        if ordinal_num * category_num < 30:
            break;
    # print("category_num")
    # print(category_num)
    begin_num = numpy.random.random()
    cat_begin_value = [numpy.random.uniform(0.1, 1) for i in range(category_num)]
    # 归一化，最大值为1
    max_cat_begin_value = max(cat_begin_value)
    cat_begin_value = [i/max_cat_begin_value for i in cat_begin_value]

    small_cat, big_cat = get_big_small_index(cat_begin_value)

    #
    while True:
        normal_trend = numpy.random.uniform(-10, 10)
        special_trend = numpy.random.uniform(-10, 10)
        if abs(normal_trend - special_trend) > 7 and abs(normal_trend) > 0.5 and abs(special_trend) > 0.5:
            break
    # print(normal_trend)
    # print(special_trend)
    special_list = get_special_list(category_num)
    if special_trend < normal_trend:
        tmp = normal_trend
        normal_trend = special_trend
        special_trend = tmp
        new_special_list = [i for i in range(category_num) if i not in special_list]
        special_list = new_special_list
    # print(f'special_list: {special_list}')
    data_content = []
    focus_coor = []
    compare_coor = []
    for i in range(category_num):
        this_focus = {}
        this_focus[0] = cat_begin_value[i]
        if i in special_list:
            trend = special_trend
            focus_coor.append([i, 0])
            focus_coor.append([i, ordinal_num - 1])
        else:
            trend = normal_trend
            compare_coor.append([i, 0])
            compare_coor.append([i, ordinal_num - 1])
        this_focus[ordinal_num - 1] = this_focus[0] * (1 + trend/10.0)
        data_content.append(this_focus)



    focus_id = [change_coordinate_to_id(coor, ordinal_num) for coor in focus_coor]
    compare_id = [change_coordinate_to_id(coor, ordinal_num) for coor in compare_coor]
    sentences = []
    sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_trend'})

    data_full = interpolate_data(data_content)
    diff_max = judge_big_diff(data_full, small_cat, big_cat)
    if diff_max > 0.1:
        focus_id = []
        compare_id = []
        for i in range(category_num):
            if i in small_cat:
                for j in range(ordinal_num):
                    focus_id.append(change_coordinate_to_id([i, j], ordinal_num))
            elif i in big_cat:
                for j in range(ordinal_num):
                    compare_id.append(change_coordinate_to_id([i, j], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'compare_ave'})

    # 添加一个神奇的特殊值
    if main_dim == 'c0' and ordinal_num >= 5:
        focus_id = []
        compare_id = []
        special_cat = numpy.random.randint(category_num)
        special_ord = numpy.random.randint(1, ordinal_num -1)
        special_ratio = get_special_ratio()
        if special_ratio > 1:
            data_full[special_cat][special_ord] = max(data_full[special_cat][special_ord - 1], data_full[special_cat][special_ord + 1]) * special_ratio
        else:
            data_full[special_cat][special_ord] = min(data_full[special_cat][special_ord - 1], data_full[special_cat][special_ord + 1]) * special_ratio
        focus_id.append(change_coordinate_to_id([special_cat, special_ord - 1], ordinal_num))
        focus_id.append(change_coordinate_to_id([special_cat, special_ord], ordinal_num))
        focus_id.append(change_coordinate_to_id([special_cat, special_ord + 1], ordinal_num))

        sentences.append({'focus_id': focus_id, 'compare_id': compare_id, 'type': 'local_trend'})



    data = generate_pack_data(data_full)

    data['major_name'] = main_dim
    data['second_name'] = second_dim


    data = add_color(data)
    # data = add_small_value(data)
    data['vis_type'] = vis_type
    data['pre_gen_focus'] = sentences

    return data


def generate_ocq_rule_data(vis_type, rule_type):

    # return generate_all_special_stack_data(vis_type)

    if vis_type == 'load_group_bar_chart':
        if numpy.random.random() > 0.5:
            vis_type = 'load_group_bar_chart_horizontal'
        if numpy.random.random() > 0.5:
            operations = [generate_a_special_prominent, generate_ocq_group_data, generate_single_complex_data]
            main_dim = 'c0'
            second_dim = 'o0'
            return operations[numpy.random.randint(len(operations))](rule_type, vis_type, main_dim = main_dim, second_dim = second_dim)
        else:
            operations = [generate_ocq_group_data, generate_single_complex_data]
            main_dim = 'o0'
            second_dim = 'c0'
            return operations[numpy.random.randint(len(operations))](rule_type, vis_type, main_dim = main_dim, second_dim = second_dim)

    elif vis_type == 'load_stack_bar_chart':
        if numpy.random.random() > 0.5:
            vis_type = 'load_stack_bar_chart_horizontal'
        print(f'vis_type: {vis_type}')
        operations = [generate_ocq_stack_data, generate_single_complex_stack_data, generate_single_special_stack_data, generate_all_special_stack_data]

        return operations[numpy.random.randint(len(operations))](rule_type, vis_type = vis_type)


if __name__ == '__main__':
    data = generate_rule_data('ocq', 'load_group_bar_chart','ocq_common')
    print(data)
