import os.path
import torchvision.transforms as transforms
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import torch
import numpy
import random
import bs4
from svg.path import parse_path
from data.deal_svg import parse_svg
from data.deal_svg import parse_svg_string



class SvgresnetDataset(BaseDataset):
    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser
    def parser_svg(svg_file):
        return svg_file;


    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)
        self.AB_paths = sorted(make_dataset(self.dir_AB))


    def __getitem__(self, index):

        AB_path = self.AB_paths[index]
        with open(AB_path) as f:
            datum = json.load(f)

        svg_string = datum['svg_string']
        sentences = datum['sentences']

        A_numpy, id_array = parse_svg_string(svg_string)

        B_list = []
        for id in id_array:
            choice = []
            for sentence in sentences:
                selected = 0
                compare_id = sentence['compare_id']
                focus_id = sentence['focus_id']
                if id in focus_id:
                    selected = 2
                elif id in compare_id:
                    selected = 1
                this_choice = [0,0,0]
                this_choice[selected] = 1
                choice = choice + this_choice
            B_list.append(choice)





        B_path = self.B_paths[index_B]
        A_numpy = numpy.load(A_path)
        B_numpy = numpy.load(B_path)
        A_numpy = numpy.pad(A_numpy,((0, self.suggest_length - A_numpy.shape[0]),(0,0)), "constant")
        B_numpy = numpy.pad(B_numpy,((0, self.suggest_length - B_numpy.shape[0]),(0,0)), "constant")
        A_numpy = A_numpy.transpose()
        B_numpy = B_numpy.transpose()
        A = torch.FloatTensor(A_numpy)
        B = torch.FloatTensor(B_numpy)
        # print(A.shape)
        # print(B.shape)
        return {'A': A, 'B': B,
                'A_paths': A_path, 'B_paths': B_path}

    def __len__(self):
        return len(self.AB_paths)

    def name(self):
        return 'SvgresnetDataset'
