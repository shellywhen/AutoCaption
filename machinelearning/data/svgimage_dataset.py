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


class SvgimageDataset(BaseDataset):
    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser
    def parser_svg(svg_file):
        return svg_file;


    def initialize(self, opt):
        # self.A_size = 1000
        # self.B_size = 1000
        #
        # return
        self.opt = opt
        self.root = opt.dataroot
        # self.dir_A = os.path.join(opt.dataroot, opt.phase + 'A')
        # self.dir_B = os.path.join(opt.dataroot, opt.phase + 'B')

        # this is only for debug
        self.dir_A = "./datasets/svg2image/svg"
        self.dir_B = "./datasets/svg2image/img"

        self.A_paths = make_dataset(self.dir_A)
        self.B_paths = make_dataset(self.dir_B)

        self.A_paths = sorted(self.A_paths)
        self.B_paths = sorted(self.B_paths)
        self.A_size = len(self.A_paths)
        self.B_size = len(self.B_paths)
        transform_list = []
        osize = [opt.loadSize, opt.loadSize]
        transform_list.append(transforms.Resize(osize, Image.BICUBIC))
        transform_list.append(transforms.ToTensor())

        self.transform = transforms.Compose(transform_list)

    def __getitem__(self, index):

        # A_numpy = numpy.random.rand(12,7)
        # A = torch.FloatTensor(A_numpy)
        # B_numpy = numpy.random.rand(3,64,64)
        # B = torch.FloatTensor(B_numpy)
        # path = "./" + str(index) + ".png" # this is only a fake one
        # return {"A": A, "B": B, "A_paths": path, "B_paths": path}

        A_path = self.A_paths[index % self.A_size]
        if self.opt.serial_batches:
            index_B = index % self.B_size
        else:
            index_B = random.randint(0, self.B_size - 1)
        B_path = self.B_paths[index_B]
        # print('(A, B) = (%d, %d)' % (index_A, index_B))
        # A_img = Image.open(A_path).convert('RGB')
        if self.opt.output_nc == 4:
            B_img = Image.open(B_path).convert('RGBA')
        elif self.opt.output_nc == 3:
            B_img = Image.open(B_path).convert("RGB")
        # B_img.resize((self.opt.loadSize, self.opt.loadSize))


        # A = self.transform(A_img)
        # print("real_B",B_img)
        B_numpy = numpy.asarray(B_img).astype("float64") * 2 / 255 - 1
        # B_numpy.transpose((2,0,1))
        # print(B_numpy.shape)

        B = self.transform(B_img)
        # print("what:???", B)
        # print(numpy.max())
        # print(B)


        # B = torch.FloatTensor(B_numpy)

        input_nc = self.opt.input_nc
        output_nc = self.opt.output_nc

        A_svg = parse_svg(A_path)
        A = torch.FloatTensor(A_svg)

        if output_nc == 1:  # RGB to gray
            tmp = B[0, ...] * 0.299 + B[1, ...] * 0.587 + B[2, ...] * 0.114
            B = tmp.unsqueeze(0)
        return {'A': A, 'B': B,
                'A_paths': A_path, 'B_paths': B_path}

    def __len__(self):
        return max(self.A_size, self.B_size)

    def name(self):
        return 'UnalignedDataset'
