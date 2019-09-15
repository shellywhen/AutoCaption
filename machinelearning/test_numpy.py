import os
import torch
import json
from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
from util.visualizer import save_images
from util import html
import numpy
from data.deal_svg import parse_svg_string
import sys
if __name__ == '__main__':
    sys.path.append(os.path.abspath('../server'))
    sys.path.append(os.path.abspath('./'))
    sys.path.append(os.path.abspath('../extracter'))





class use_model:
    def __init__(self, opt):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

def get_data_svg(svg_string):
    A_numpy, id_array = parse_svg_string(svg_string)
    print(id_array)
    data = get_data_numpy(A_numpy)
    return data, id_array

def get_data_numpy(numpy_data):
    data = {}
    A_numpy = numpy_data.transpose() - 0.5
    A_array = A_numpy[numpy.newaxis, :]
    A = torch.FloatTensor(A_array)
    data['A'] = A
    data['B'] = torch.FloatTensor(numpy.array([1,2]))
    data['A_paths'] = ''
    data['B_paths'] = ''
    return data

def get_data_json(json_file):
    with open(json_file) as f:
        data_json = json.load(f)
    svg_string = data_json['svg_string']
    return get_data_svg(svg_string)


def get_data_numpy_file(file_name):
    A_numpy = numpy.load(file_name)
    data = get_data_numpy(A_numpy)
    return data

def parse_to_id_array(output_numpy, id_array):
    output = output_numpy[0].transpose()
    second_dimension_number = output.shape[1]
    sentences_number = second_dimension_number / 3
    assert(sentences_number * 3 == second_dimension_number)

    output_array = numpy.split(output, sentences_number, axis = 1)

    return_array = []
    print(id_array)
    for sentence in output_array:
        compare_id = []
        focus_id = []
        strength = sum([max(sentence[i]) for i in range(len(id_array))])/len(id_array)
        # print(f'The strength is {strength}')
        for i, element in enumerate(sentence):
            if (i >= len(id_array)):
                break
            index = 0
            index = numpy.argmax(element)
            id = id_array[i]
            if index == 2:
                focus_id.append(id)
            elif index == 1:
                compare_id.append(id)
        # print(f'focus: {focus_id}, compare: {compare_id}')
        sentence = {}
        sentence['compare_id'] = compare_id
        sentence['focus_id'] = focus_id
        sentence['strength'] = strength
        return_array.append(sentence)
    return return_array

def initialize(opt):
    opt.model = 'svgresnetgan'
    opt.svgresnet_output = 2
    opt.fix_size = -1
    opt.ngf = 256


def fake_init():

    opt = TestOptions().parse()
    opt.nThreads = 1   # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display
    # print(opt.which_model_netG)

    model = create_model(opt)
    model.setup(opt)
    # test
    # data = get_data_numpy_file('datasets/20180822_fix_max_real_data/trainA/2018_08_20_14_38_19_6309872.npy')
    data, id_array = get_data_json('../server/user_collected_data/2018_08_20_14_38_19_6309872.json')
    model.set_input(data)
    output = model.test()
    focal_array = parse_to_id_array(output, id_array)
    json_data = json.dumps(focal_array, indent=2)
    # print(json_data)

def init_model():
    opt = TestOptions().parse()
    opt.nThreads = 1   # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display
    opt.checkpoints_dir = '../machinelearning/checkpoints'
    model = create_model(opt)
    model.setup(opt)
    return model, opt
    # test
    # data = get_data_numpy_file('datasets/20180822_fix_max_real_data/trainA/2018_08_20_14_38_19_6309872.npy')
    data, id_array = get_data_json('../server/user_collected_data/2018_08_20_14_38_19_6309872.json')
    for i in range(10):
        model.set_input(data)
        output = model.test()
        focal_array = parse_to_id_array(output, id_array)
        json_data = json.dumps(focal_array, indent=2)
        # print(json_data)
    # print(output)
    # print(output.shape)


if __name__ == '__main__':
    # fake_init()
    model, opt = init_model()
    # data, id_array = get_data_json('../server/user_collected_data/2018_08_20_14_38_19_6309872.json')
    # print(data)
    # for i in range(5):
    #     model.set_input(data)
    #     output = model.test()
    #     focal_array = parse_to_id_array(output, id_array)
    #     json_data = json.dumps(focal_array, indent=2)
    #     print(json_data)
    import server
    print(f'SHOW is : {opt.show}')
    server.run_server(opt.server_port, model, opt.show)
