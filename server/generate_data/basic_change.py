import random
import numpy

def add_color(data, single = False):
    color = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
    random.shuffle(color)
    if single:
        data['color'] = [color[0] for i in range(len(color))]
    else:
        data['color'] = color
    return data

def add_type(data):
    type = get_data_type(data)
    data['type'] = type
    return data

def get_data_type(data):
    data_attr = data['data_array'][0].keys()

    if 'c0' in data_attr and 'c1' in data_attr:
        return 'ccq'
    elif 'c0' in data_attr and 'o0' in data_attr:
        return 'ocq'
    elif 'c0' in data_attr:
        return 'cq'
    elif 'o0' in data_attr:
        return 'oq'

def add_vis_type(data):
    if 'vis_type' in data:
        return data
    if data['type'] == 'oq' or data['type'] == 'cq':
        choice = ['load_bar_chart_1d', 'load_bar_chart_1d_horizontal']
        data['vis_type'] = choice[numpy.random.randint(0, len(choice))]
    elif data['type'] == 'ocq' or data['type'] == 'ccq':
        choice = ['load_group_bar_chart', 'load_group_bar_chart_horizontal', 'load_stack_bar_chart', 'load_stack_bar_chart_horizontal']
        data['vis_type'] = choice[numpy.random.randint(0, len(choice))]
    return data

# delete very long name
def del_long_name(data, delete_dimension = 'c0'):
    names = [data[delete_dimension][i] for i in range(len(data[delete_dimension]))]
    names_len = [len(name) for name in names]
    max_name_len = max(names_len)
    if (max_name_len > 50 / len(names)):
        names = [''.join([word[0:2] for word in name.split(' ') if len(word)>1]).upper() for name in names ]
    data['c0'] = names
    return data
