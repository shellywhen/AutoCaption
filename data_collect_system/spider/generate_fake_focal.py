from deal_svg_copy import parse_svg_full
import numpy
import os

def generate_max(input_name, output_name):
    data_array = parse_svg_full(input_name)
    # print(data_array.shape)
    data_value = [data[13] for data in data_array]
    # print(data_value)

    max_position = numpy.where(data_value == numpy.max(data_value))[0][0]
    # print(max_position)
    output_type = numpy.zeros(len(data_value), dtype = "int64")
    for i in range(max_position, 0, -1):
        if data_value[i] > data_value[i-1] or i == 0:
            output_type[i] = 1
        else:
            break;
    output_type[max_position] = 2

    output_fold = numpy.zeros([len(output_type), 3], dtype = "int64" )
    for i, d in enumerate(output_type):
        output_fold[i][d] = 1
    # print(output_fold)
    numpy.save(output_name, output_fold)
    return output_fold

def generate_min3(input_name, output_name):
    data_array = parse_svg_full(input_name)
    # print(data_array.shape)
    data_value = [data[13] for data in data_array]
    # print(data_value)
    data_sort = numpy.argsort(data_value)[-3:]


    output_type = numpy.zeros(len(data_value), dtype = "int64")
    for index in data_sort:
        output_type[index] = 2

    output_fold = numpy.zeros([len(output_type), 3], dtype = "int64" )
    for i, d in enumerate(output_type):
        output_fold[i][d] = 1
    # print(output_fold)
    numpy.save(output_name, output_fold)
    return output_fold

def generate_max(input_name):
    data_array = parse_svg_full(input_name)
    # print(data_array.shape)
    data_value = [data[13] for data in data_array]
    # print(data_value)

    max_position = numpy.where(data_value == numpy.max(data_value))[0][0]
    # print(max_position)
    output_type = numpy.zeros(len(data_value), dtype = "int64")
    for i in range(max_position, 0, -1):
        if data_value[i] > data_value[i-1] or i == 0:
            output_type[i] = 1
        else:
            break;
    output_type[max_position] = 2

    output_fold = numpy.zeros([len(output_type), 3], dtype = "int64" )
    for i, d in enumerate(output_type):
        output_fold[i][d] = 1
    # print(output_fold)
    return output_fold

def generate_min3(input_name):
    data_array = parse_svg_full(input_name)
    # print(data_array.shape)
    data_value = [data[13] for data in data_array]
    # print(data_value)
    data_sort = numpy.argsort(data_value)[-3:]


    output_type = numpy.zeros(len(data_value), dtype = "int64")
    for index in data_sort:
        output_type[index] = 2

    output_fold = numpy.zeros([len(output_type), 3], dtype = "int64" )
    for i, d in enumerate(output_type):
        output_fold[i][d] = 1
    # print(output_fold)
    return output_fold

def generate_more(input_name, output_name):
    max1 = generate_max(input_name)
    min3 = generate_min3(input_name)
    assert(len(max1) == len(min3))
    output = numpy.concatenate((max1, min3), axis = 1)
    numpy.save(output_name, output)
    return output

def read_focal(filename):
    a = numpy.load(filename)
    return a

def generate_focal():
    filelist = os.listdir("svg")
    for file in filelist:
        input_file_name = "svg/" + file
        output_file_name = "max_min3/" + file[:-4] + ".npy"
        generate_more(input_file_name, output_file_name)
        print(output_file_name)

def change_svg_presentation():
    filelist = os.listdir("svg")
    for file in filelist:
        input_file_name = "svg/" + file
        output_file_name = "svg_npy/" + file[:-4] + ".npy"
        data_array = parse_svg_full(input_file_name)
        numpy.save(output_file_name, data_array)
        print(data_array.shape)
        print(output_file_name)
def check_dimention(index):
    svg_name = "svg_npy/" + index + ".npy"
    focal_name = "focal/" + index + ".npy"
    print(numpy.load(svg_name).shape)
    print(numpy.load(focal_name).shape)

# check_dimention("0349")
generate_focal()
