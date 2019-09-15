
#coding=utf-8
import json
import numpy
import numpy as np
import math
from numpy.linalg import cholesky
import random
from basic_change import add_color, add_type, get_data_type, del_long_name, add_vis_type
from ocq_data_generator import add_small_value, add_small_random

import matplotlib.pyplot as plt


# type: trend, cluster, outliers
# there

def generate_line_data(begin, end, sigma = 0.05, total_number = 100):
    data = []
    delta_x = begin[0] - end[0]
    delta_y = begin[1] - end[1]
    delta_distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    x_unit = - delta_y / delta_distance
    y_unit = delta_x / delta_distance
    for i in range(total_number):
        rate = numpy.random.uniform(0,1)
        original_x = begin[0] + rate * (end[0] - begin[0])
        original_y = begin[1] + rate * (end[1] - begin[1]) # 我们首先搞一个初始的位置
        uniform_error = numpy.random.normal(0, sigma) # 我们接着设定一个随机变量
        data.append([original_x + uniform_error * x_unit, original_y + uniform_error * y_unit]) # 然后在直线的垂直方向加
    data = numpy.asarray(data)
    return data

def generate_class_data(center = [0.5, 0.5], total_number = 100, sigma = [0.05, 0.05], corr = 0):
    cov_xy = corr * sigma[0] * sigma[1]
    cov = [[sigma[0] * sigma[0], cov_xy],[cov_xy, sigma[1] * sigma[1]]]
    x = np.random.multivariate_normal(center, cov, total_number)
    print(x)
    return x

def generate_scatter_data(type_number = 1, total_number = 25):
    data = []
    return data


if __name__ == '__main__':
    # x = generate_class_data(corr = 0.5)
    x = generate_class_data(center = [0.5, 0.5], corr = 0.5)
    y = generate_class_data(center = [0.9, 0.9], corr = 0.5, total_number = 2)

    x = np.concatenate((x,y), axis = 0)
    #
    # x = np.concatenate((x, generate_class_data(center = [0.2, 0.2], corr = 0.9)), axis = 0)
    # x = np.concatenate((x, generate_line_data(begin = [0.2, 0.2], end = [0.9, 0.9], sigma = 0.02)), axis = 0)
    # x = np.concatenate((x, generate_line_data(begin = [0.2, 0.2], end = [0.2, 0.9], sigma = 0.02)), axis = 0)
    print(x.shape)

    # sampleNo = 250
    # mean = (1,1)
    # cov = [[1,1],[1,1]]
    # x = np.random.multivariate_normal(mean, cov, sampleNo)
    plt.axis([0,1,0,1])
    plt.scatter(x[:,0], x[:,1], marker = 'o', color = 'black', alpha = 0.2)
    plt.show()

    # plt.subplot(144)
    # plt.plot(s[:,0],s[:,1],'+')
    # plt.show()
