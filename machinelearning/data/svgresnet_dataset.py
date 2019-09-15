import os.path
import torchvision.transforms as transforms
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import torch
import numpy
import random
import bs4
# from svg.path import parse_path
from data.deal_svg import parse_svg
import random


class SvgresnetDataset(BaseDataset):
    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser
    def parser_svg(svg_file):
        return svg_file;


    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.dir_A = os.path.join(opt.dataroot, opt.phase + 'A')
        self.dir_B = os.path.join(opt.dataroot, opt.phase + 'B')

        # this is only for debug
        self.A_paths = make_dataset(self.dir_A)
        self.B_paths = make_dataset(self.dir_B)


        self.A_paths = sorted(self.A_paths)
        self.B_paths = sorted(self.B_paths)
        self.A_size = len(self.A_paths)
        self.B_size = len(self.B_paths)
        self.need_fix = False
        if opt.fix_size > 0:
            self.need_fix = True
            self.suggest_length = opt.fix_size
        assert(self.A_size == self.B_size)

    def __getitem__(self, index):

        A_path = self.A_paths[index % self.A_size]
        index_B = index % self.B_size
        B_path = self.B_paths[index_B]
        A_numpy = numpy.load(A_path)
        B_numpy = numpy.load(B_path)
        if self.need_fix:
            A_numpy = numpy.pad(A_numpy,((0, self.suggest_length - A_numpy.shape[0]),(0,0)), "constant")
            B_numpy = numpy.pad(B_numpy,((0, self.suggest_length - B_numpy.shape[0]),(0,0)), "constant")
        if self.opt.random_order:
            # print(A_numpy.shape)
            # print(A_path)
            element_number = A_numpy.shape[0]
            order = [i for i in range(element_number)]
            random.shuffle(order)
            A_numpy_list = [ A_numpy[order[i]] for i in range(element_number)]
            B_numpy_list = [ B_numpy[order[i]] for i in range(element_number)]
            A_numpy = numpy.asarray(A_numpy_list)
            B_numpy = numpy.asarray(B_numpy_list)
        if self.opt.random_error:
            shape = B_numpy.shape
            B_random = numpy.zeros(shape)
            for i, element in enumerate(B_numpy):
                for j, channel in enumerate(element):
                    B_random[i][j] = float(channel) + numpy.random.normal(0, 0.2)
            # print(B_random)
            B_random = B_random.transpose()
            B_random = B_random - 0.5
            B_r = torch.FloatTensor(B_random)
        # print(A_numpy.shape)

        A_numpy = A_numpy.transpose()
        B_numpy = B_numpy.transpose()


        A_numpy = A_numpy - 0.5
        B_numpy = B_numpy - 0.5


        A = torch.FloatTensor(A_numpy)
        B = torch.FloatTensor(B_numpy)

        # print(A.shape)
        # print(B.shape)
        if self.opt.random_error:
            return {'A': A,
                    'B': B,
                    'B_r': B_r,
                    'A_paths': A_path,
                    'B_paths': B_path}
        return {'A': A, 'B': B,
                'A_paths': A_path, 'B_paths': B_path}

    def __len__(self):
        if self.opt.random_order:
            return self.A_size * 100
        return max(self.A_size, self.B_size)

    def name(self):
        return 'SvgresnetDataset'
