# -*- coding: UTF-8 -*-

import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler

###############################################################################
# Helper Functions
###############################################################################


def get_norm_layer(norm_type='instance'):
    if norm_type == 'batch':
        norm_layer = functools.partial(nn.BatchNorm2d, affine=True)
    elif norm_type == 'instance':
        norm_layer = functools.partial(nn.InstanceNorm2d, affine=False, track_running_stats=True)
    elif norm_type == 'none':
        norm_layer = None
    else:
        raise NotImplementedError('normalization layer [%s] is not found' % norm_type)
    return norm_layer


def get_scheduler(optimizer, opt):
    if opt.lr_policy == 'lambda':
        def lambda_rule(epoch):
            lr_l = 1.0 - max(0, epoch + 1 + opt.epoch_count - opt.niter) / float(opt.niter_decay + 1)
            return lr_l
        scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda_rule)
    elif opt.lr_policy == 'step':
        scheduler = lr_scheduler.StepLR(optimizer, step_size=opt.lr_decay_iters, gamma=0.1)
    elif opt.lr_policy == 'plateau':
        scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.2, threshold=0.01, patience=5)
    else:
        return NotImplementedError('learning rate policy [%s] is not implemented', opt.lr_policy)
    return scheduler


def init_weights(net, init_type='normal', gain=0.02):
    def init_func(m):
        classname = m.__class__.__name__
        if hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
            if init_type == 'normal':
                init.normal_(m.weight.data, 0.0, gain)
            elif init_type == 'xavier':
                init.xavier_normal_(m.weight.data, gain=gain)
            elif init_type == 'kaiming':
                init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
            elif init_type == 'orthogonal':
                init.orthogonal_(m.weight.data, gain=gain)
            else:
                raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
            if hasattr(m, 'bias') and m.bias is not None:
                init.constant_(m.bias.data, 0.0)
        elif classname.find('BatchNorm2d') != -1:
            init.normal_(m.weight.data, 1.0, gain)
            init.constant_(m.bias.data, 0.0)

    print('initialize network with %s' % init_type)
    net.apply(init_func)


def init_net(net, init_type='normal', init_gain=0.02, gpu_ids=[]):
    if len(gpu_ids) > 0:
        assert(torch.cuda.is_available())
        net.to(gpu_ids[0])
        net = torch.nn.DataParallel(net, gpu_ids)
    init_weights(net, init_type, gain=init_gain)
    return net


def define_G(input_nc, output_nc, ngf, which_model_netG, norm='batch', use_dropout=False, init_type='normal', init_gain=0.02, gpu_ids=[], svgresnet_output=3, need_mid = False, resnet_layer = 12):
    netG = None
    norm_layer = get_norm_layer(norm_type=norm)

    if which_model_netG == 'resnet_9blocks':
        netG = ResnetGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=9)
    elif which_model_netG == 'resnet_6blocks':
        netG = ResnetGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=6)
    elif which_model_netG == 'unet_128':
        netG = UnetGenerator(input_nc, output_nc, 7, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif which_model_netG == 'unet_256':
        netG = UnetGenerator(input_nc, output_nc, 8, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif which_model_netG == 'svg2image':
        netG = SvgImageGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif which_model_netG == "uniformsvgimage":
        netG = UniformSvgImageGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif which_model_netG == "svgresnet":
        netG = SvgResnetGenerator(input_nc, output_nc, ngf, norm_layer=nn.BatchNorm1d, use_dropout=use_dropout, svgresnet_output=svgresnet_output, need_mid = need_mid, resnet_layer = resnet_layer)
    else:
        raise NotImplementedError('Generator model name [%s] is not recognized' % which_model_netG)
    return init_net(netG, init_type, init_gain, gpu_ids)


def define_D(input_nc, ndf, which_model_netD,
             n_layers_D=3, norm='batch', use_sigmoid=False, init_type='normal', init_gain=0.02, gpu_ids=[], leak_value = 0.2):
    netD = None
    norm_layer = get_norm_layer(norm_type=norm)

    if which_model_netD == 'basic':
        netD = NLayerDiscriminator(input_nc, ndf, n_layers=3, norm_layer=norm_layer, use_sigmoid=use_sigmoid)
    elif which_model_netD == 'n_layers':
        netD = NLayerDiscriminator(input_nc, ndf, n_layers_D, norm_layer=norm_layer, use_sigmoid=use_sigmoid)
    elif which_model_netD == 'pixel':
        netD = PixelDiscriminator(input_nc, ndf, norm_layer=norm_layer, use_sigmoid=use_sigmoid)
    elif which_model_netD == 'discri1d':
        netD = NLayerDiscriminator1d(input_nc, ndf, n_layers_D, norm_layer=nn.BatchNorm1d, use_sigmoid=use_sigmoid, leak_value=leak_value)
    elif which_model_netD == 'resnet_dis1d':
        netD = NLayerDiscriminator1d(input_nc, ndf, n_layers_D, norm_layer=nn.BatchNorm1d, use_sigmoid=use_sigmoid, leak_value=leak_value)
    else:
        raise NotImplementedError('Discriminator model name [%s] is not recognized' %
                                  which_model_netD)
    return init_net(netD, init_type, init_gain, gpu_ids)


##############################################################################
# Classes
##############################################################################


# Defines the GAN loss which uses either LSGAN or the regular GAN.
# When LSGAN is used, it is basically same as MSELoss,
# but it abstracts away the need to create the target label tensor
# that has the same size as the input
class GANLoss(nn.Module):
    def __init__(self, use_lsgan=True, target_real_label=1.0, target_fake_label=0.0):
        super(GANLoss, self).__init__()
        self.register_buffer('real_label', torch.tensor(target_real_label))
        self.register_buffer('fake_label', torch.tensor(target_fake_label))
        if use_lsgan:
            self.loss = nn.MSELoss()
        else:
            self.loss = nn.BCELoss()

    def get_target_tensor(self, input, target_is_real):
        if target_is_real:
            target_tensor = self.real_label
        else:
            target_tensor = self.fake_label
        # print(target_tensor.)
        return target_tensor.expand_as(input)

    def __call__(self, input, target_is_real):
        target_tensor = self.get_target_tensor(input, target_is_real)
        return self.loss(input, target_tensor)




# Defines the generator that consists of Resnet blocks between a few
# downsampling/upsampling operations.
# Code and idea originally from Justin Johnson's architecture.
# https://github.com/jcjohnson/fast-neural-style/
class ResnetGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, ngf=64, norm_layer=nn.BatchNorm2d, use_dropout=False, n_blocks=6, padding_type='reflect'):
        assert(n_blocks >= 0)
        super(ResnetGenerator, self).__init__()
        self.input_nc = input_nc
        self.output_nc = output_nc
        self.ngf = ngf
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm2d
        else:
            use_bias = norm_layer == nn.InstanceNorm2d

        model = [nn.ReflectionPad2d(3),
                 nn.Conv2d(input_nc, ngf, kernel_size=7, padding=0,
                           bias=use_bias),
                 norm_layer(ngf),
                 nn.ReLU(True)]

        n_downsampling = 2
        for i in range(n_downsampling):
            mult = 2**i
            model += [nn.Conv2d(ngf * mult, ngf * mult * 2, kernel_size=3,
                                stride=2, padding=1, bias=use_bias),
                      norm_layer(ngf * mult * 2),
                      nn.ReLU(True)]

        mult = 2**n_downsampling
        for i in range(n_blocks):
            model += [ResnetBlock(ngf * mult, padding_type=padding_type, norm_layer=norm_layer, use_dropout=use_dropout, use_bias=use_bias)]

        for i in range(n_downsampling):
            mult = 2**(n_downsampling - i)
            model += [nn.ConvTranspose2d(ngf * mult, int(ngf * mult / 2),
                                         kernel_size=3, stride=2,
                                         padding=1, output_padding=1,
                                         bias=use_bias),
                      norm_layer(int(ngf * mult / 2)),
                      nn.ReLU(True)]
        model += [nn.ReflectionPad2d(3)]
        model += [nn.Conv2d(ngf, output_nc, kernel_size=7, padding=0)]
        model += [nn.Tanh()]

        self.model = nn.Sequential(*model)

    def forward(self, input):
        return self.model(input)


# Define a resnet block
class ResnetBlock(nn.Module):
    def __init__(self, dim, padding_type, norm_layer, use_dropout, use_bias):
        super(ResnetBlock, self).__init__()
        self.conv_block = self.build_conv_block(dim, padding_type, norm_layer, use_dropout, use_bias)

    def build_conv_block(self, dim, padding_type, norm_layer, use_dropout, use_bias):
        conv_block = []
        p = 0
        if padding_type == 'reflect':
            conv_block += [nn.ReflectionPad2d(1)]
        elif padding_type == 'replicate':
            conv_block += [nn.ReplicationPad2d(1)]
        elif padding_type == 'zero':
            p = 1
        else:
            raise NotImplementedError('padding [%s] is not implemented' % padding_type)

        conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias),
                       norm_layer(dim),
                       nn.ReLU(True)]
        if use_dropout:
            conv_block += [nn.Dropout(0.5)]

        p = 0
        if padding_type == 'reflect':
            conv_block += [nn.ReflectionPad2d(1)]
        elif padding_type == 'replicate':
            conv_block += [nn.ReplicationPad2d(1)]
        elif padding_type == 'zero':
            p = 1
        else:
            raise NotImplementedError('padding [%s] is not implemented' % padding_type)
        conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias),
                       norm_layer(dim)]

        return nn.Sequential(*conv_block)

    def forward(self, x):
        out = x + self.conv_block(x)
        return out

# Defines the resnet1D generator.
# https://github.com/jcjohnson/fast-neural-style/

class SvgResnetGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, ngf=64, norm_layer=nn.BatchNorm1d, use_dropout=False, n_blocks=6, padding_type='reflect', svgresnet_output=3, need_mid=False, resnet_layer = 12):
        super(SvgResnetGenerator, self).__init__()
        assert(len(input_nc) == len(output_nc))
        self.input_parts = len(input_nc)
        # exec("self.debug_embedding = nn.Conv1d(sum(input_nc), sum(output_nc), kernel_size = 1)")
        self.embedding = []
        self.input_nc = input_nc
        self.output_nc = output_nc
        for i in range(self.input_parts):
            model = [nn.Conv1d(input_nc[i], output_nc[i], kernel_size = 1),
                    nn.BatchNorm1d(output_nc[i])]
            exec("self.embedding{} = nn.Sequential(*model)".format(i))

        total_nc = sum(output_nc)
        self.total_nc = total_nc
        self.linear = nn.Conv1d(total_nc, total_nc, kernel_size = 1)
        self.resnet1d = Resnet1dGenerator(total_nc, svgresnet_output, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=resnet_layer) # 3 代表着生成一个句子。第一个维度表示是否关键部分、第二个维度表示是否被比较部分、第三个维度表示不重要。
            # type_encoder = [nn.Conv1d(3, type_out_nc, kernel_size = 1),
                            # nn.BatchNorm1d(type_out_nc)]
        self.need_mid = need_mid




    def forward(self, input):
        # print(input.data.shape)
        input_array = torch.split(input, self.input_nc, dim = 1) #  这边根据input——nc的数组对输入的数据进行分裂
        assert(len(input_array) == len(self.input_nc))
        embedding_results = []
        for i in range(self.input_parts):
            exec("embedding_results.append(self.embedding{}(input_array[i]))".format(i)) # 对每个模块输出一部分
        total = torch.cat(embedding_results, 1)
        # assert(self.total_nc == total.data.shape[1])
        # total = self.debug_embedding(input)
        mid = self.linear(total)
        output = self.resnet1d(mid)

        # print(output.data.shape)
        # print(self.need_mid)
        if self.need_mid:
            return output, mid
        return output

class Resnet1dGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, ngf=64, norm_layer=nn.BatchNorm1d, use_dropout=False, n_blocks=6, padding_type='reflect'):
        assert(n_blocks >= 0)
        super(Resnet1dGenerator, self).__init__()
        self.input_nc = input_nc
        self.output_nc = output_nc
        self.ngf = ngf
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm1d
        else:
            use_bias = norm_layer == nn.InstanceNorm1d

        model = [nn.ReflectionPad1d(3),
                 nn.Conv1d(input_nc, ngf, kernel_size=7, padding=0,
                           bias=use_bias),
                 norm_layer(ngf),
                 nn.ReLU(True)]

        n_downsampling = 0
        for i in range(n_downsampling):
            mult = 2**i
            model += [nn.Conv1d(ngf * mult, ngf * mult * 2, kernel_size=3,
                                stride=2, padding=1, bias=use_bias),
                      norm_layer(ngf * mult * 2),
                      nn.ReLU(True)]

        mult = 2**n_downsampling
        for i in range(n_blocks):
            model += [Resnet1dBlock(ngf * mult, padding_type=padding_type, norm_layer=norm_layer, use_dropout=use_dropout, use_bias=use_bias)]

        for i in range(n_downsampling):
            mult = 2**(n_downsampling - i)
            model += [nn.ConvTranspose1d(ngf * mult, int(ngf * mult / 2),
                                         kernel_size=3, stride=2,
                                         padding=1, output_padding=1,
                                         bias=use_bias),
                      norm_layer(int(ngf * mult / 2)),
                      nn.ReLU(True)]
        model += [nn.ReflectionPad1d(3)]
        model += [nn.Conv1d(ngf, output_nc, kernel_size=7, padding=0)]
        model += [nn.Tanh()]

        self.model = nn.Sequential(*model)

    def forward(self, input):
        output = self.model(input)
        return output


# Define a resnet block
class Resnet1dBlock(nn.Module):
    def __init__(self, dim, padding_type, norm_layer, use_dropout, use_bias):
        super(Resnet1dBlock, self).__init__()
        self.conv_block = self.build_conv_block(dim, padding_type, norm_layer, use_dropout, use_bias)

    def build_conv_block(self, dim, padding_type, norm_layer, use_dropout, use_bias):
        conv_block = []
        p = 0
        if padding_type == 'reflect':
            conv_block += [nn.ReflectionPad1d(1)]
        elif padding_type == 'replicate':
            conv_block += [nn.ReplicationPad1d(1)]
        elif padding_type == 'zero':
            p = 1
        else:
            raise NotImplementedError('padding [%s] is not implemented' % padding_type)

        conv_block += [nn.Conv1d(dim, dim, kernel_size=3, padding=p, bias=use_bias),
                       norm_layer(dim),
                       nn.ReLU(True)]
        if use_dropout:
            conv_block += [nn.Dropout(0.5)]

        p = 0
        if padding_type == 'reflect':
            conv_block += [nn.ReflectionPad1d(1)]
        elif padding_type == 'replicate':
            conv_block += [nn.ReplicationPad1d(1)]
        elif padding_type == 'zero':
            p = 1
        else:
            raise NotImplementedError('padding [%s] is not implemented' % padding_type)
        conv_block += [nn.Conv1d(dim, dim, kernel_size=3, padding=p, bias=use_bias),
                       norm_layer(dim)]

        return nn.Sequential(*conv_block)

    def forward(self, x):
        out = x + self.conv_block(x)
        return out



# Defines the Unet generator.
# |num_downs|: number of downsamplings in UNet. For example,
# if |num_downs| == 7, image of size 128x128 will become of size 1x1
# at the bottleneck
class UnetGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, num_downs, ngf=64,
                 norm_layer=nn.BatchNorm2d, use_dropout=False):
        super(UnetGenerator, self).__init__()

        # construct unet structure
        unet_block = UnetSkipConnectionBlock(ngf * 8, ngf * 8, input_nc=None, submodule=None, norm_layer=norm_layer, innermost=True)
        for i in range(num_downs - 5):
            unet_block = UnetSkipConnectionBlock(ngf * 8, ngf * 8, input_nc=None, submodule=unet_block, norm_layer=norm_layer, use_dropout=use_dropout)
        unet_block = UnetSkipConnectionBlock(ngf * 4, ngf * 8, input_nc=None, submodule=unet_block, norm_layer=norm_layer)
        unet_block = UnetSkipConnectionBlock(ngf * 2, ngf * 4, input_nc=None, submodule=unet_block, norm_layer=norm_layer)
        unet_block = UnetSkipConnectionBlock(ngf, ngf * 2, input_nc=None, submodule=unet_block, norm_layer=norm_layer)
        unet_block = UnetSkipConnectionBlock(output_nc, ngf, input_nc=input_nc, submodule=unet_block, outermost=True, norm_layer=norm_layer)

        self.model = unet_block

    def forward(self, input):
        return self.model(input)


# Defines the submodule with skip connection.
# X -------------------identity---------------------- X
#   |-- downsampling -- |submodule| -- upsampling --|
class UnetSkipConnectionBlock(nn.Module):
    def __init__(self, outer_nc, inner_nc, input_nc=None,
                 submodule=None, outermost=False, innermost=False, norm_layer=nn.BatchNorm2d, use_dropout=False):
        super(UnetSkipConnectionBlock, self).__init__()
        self.outermost = outermost
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm2d
        else:
            use_bias = norm_layer == nn.InstanceNorm2d
        if input_nc is None:
            input_nc = outer_nc
        downconv = nn.Conv2d(input_nc, inner_nc, kernel_size=4,
                             stride=2, padding=1, bias=use_bias)
        downrelu = nn.LeakyReLU(0.2, True)
        downnorm = norm_layer(inner_nc)
        uprelu = nn.ReLU(True)
        upnorm = norm_layer(outer_nc)

        if outermost:
            upconv = nn.ConvTranspose2d(inner_nc * 2, outer_nc,
                                        kernel_size=4, stride=2,
                                        padding=1)
            down = [downconv]
            up = [uprelu, upconv, nn.Tanh()]
            model = down + [submodule] + up
        elif innermost:
            upconv = nn.ConvTranspose2d(inner_nc, outer_nc,
                                        kernel_size=4, stride=2,
                                        padding=1, bias=use_bias)
            down = [downrelu, downconv]
            up = [uprelu, upconv, upnorm]
            model = down + up
        else:
            upconv = nn.ConvTranspose2d(inner_nc * 2, outer_nc,
                                        kernel_size=4, stride=2,
                                        padding=1, bias=use_bias)
            down = [downrelu, downconv, downnorm]
            up = [uprelu, upconv, upnorm]

            if use_dropout:
                model = down + [submodule] + up + [nn.Dropout(0.5)]
            else:
                model = down + [submodule] + up

        self.model = nn.Sequential(*model)

    def forward(self, x):
        if self.outermost:
            return self.model(x)
        else:
            return torch.cat([x, self.model(x)], 1)


# Defines the PatchGAN discriminator with the specified arguments.
class NLayerDiscriminator(nn.Module):
    def __init__(self, input_nc, ndf=64, n_layers=3, norm_layer=nn.BatchNorm2d, use_sigmoid=False):
        super(NLayerDiscriminator, self).__init__()
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm2d
        else:
            use_bias = norm_layer == nn.InstanceNorm2d

        kw = 4
        padw = 1
        sequence = [
            nn.Conv2d(input_nc, ndf, kernel_size=kw, stride=2, padding=padw),
            nn.LeakyReLU(0.2, True)
        ]

        nf_mult = 1
        nf_mult_prev = 1
        for n in range(1, n_layers):
            nf_mult_prev = nf_mult
            nf_mult = min(2**n, 8)
            sequence += [
                nn.Conv2d(ndf * nf_mult_prev, ndf * nf_mult,
                          kernel_size=kw, stride=2, padding=padw, bias=use_bias),
                norm_layer(ndf * nf_mult),
                nn.LeakyReLU(0.2, True)
            ]

        nf_mult_prev = nf_mult
        nf_mult = min(2**n_layers, 8)
        sequence += [
            nn.Conv2d(ndf * nf_mult_prev, ndf * nf_mult,
                      kernel_size=kw, stride=1, padding=padw, bias=use_bias),
            norm_layer(ndf * nf_mult),
            nn.LeakyReLU(0.2, True)
        ]

        sequence += [nn.Conv2d(ndf * nf_mult, 1, kernel_size=kw, stride=1, padding=padw)]

        if use_sigmoid:
            sequence += [nn.Sigmoid()]

        self.model = nn.Sequential(*sequence)

    def forward(self, input):
        return self.model(input)

class NLayerDiscriminator1d(nn.Module):
    def __init__(self, input_nc, ndf=64, n_layers=3, norm_layer=nn.BatchNorm1d, use_sigmoid=False, leak_value = 0.2):
        super(NLayerDiscriminator1d, self).__init__()
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm1d
        else:
            use_bias = norm_layer == nn.InstanceNorm1d

        kw = 4
        padw = 1
        sequence = [
            nn.Conv1d(input_nc, ndf, kernel_size=kw, stride=2, padding=padw),
            nn.LeakyReLU(leak_value, True)
        ]

        nf_mult = 1
        nf_mult_prev = 1
        for n in range(1, n_layers):
            nf_mult_prev = nf_mult
            nf_mult = min(2**n, 8)
            sequence += [
                nn.Conv1d(ndf * nf_mult_prev, ndf * nf_mult,
                          kernel_size=kw, stride=2, padding=padw, bias=use_bias),
                norm_layer(ndf * nf_mult),
                nn.LeakyReLU(leak_value, True)
            ]

        nf_mult_prev = nf_mult
        nf_mult = min(2**n_layers, 8)
        sequence += [
            nn.Conv1d(ndf * nf_mult_prev, ndf * nf_mult,
                      kernel_size=kw, stride=1, padding=padw, bias=use_bias),
            norm_layer(ndf * nf_mult),
            nn.LeakyReLU(leak_value, True)
        ]

        sequence += [nn.Conv1d(ndf * nf_mult, 1, kernel_size=kw, stride=1, padding=padw)]

        if use_sigmoid:
            sequence += [nn.Sigmoid()]

        self.model = nn.Sequential(*sequence)

    def forward(self, input):
        # print(input.data.shape)
        output = self.model(input)
        # print(output.data.shape)
        return output

class PixelDiscriminator(nn.Module):
    def __init__(self, input_nc, ndf=64, norm_layer=nn.BatchNorm2d, use_sigmoid=False):
        super(PixelDiscriminator, self).__init__()
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.InstanceNorm2d
        else:
            use_bias = norm_layer == nn.InstanceNorm2d

        self.net = [
            nn.Conv2d(input_nc, ndf, kernel_size=1, stride=1, padding=0),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(ndf, ndf * 2, kernel_size=1, stride=1, padding=0, bias=use_bias),
            norm_layer(ndf * 2),
            nn.LeakyReLU(0.2, True),
            nn.Conv2d(ndf * 2, 1, kernel_size=1, stride=1, padding=0, bias=use_bias)]

        if use_sigmoid:
            self.net.append(nn.Sigmoid())

        self.net = nn.Sequential(*self.net)

    def forward(self, input):
        return self.net(input)



# the generator that generates image from svg
# hope this can work.

class UniformSvgImageGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, ngf = 64, norm_layer=nn.BatchNorm1d, use_dropout=False):
        super(UniformSvgImageGenerator, self).__init__()
        self.image_encoder = ImageEncoder(4, 1024, ngf)
        self.svg_encoder = SvgEncoder(input_nc, 1024, ngf)
        self.connection = nn.Linear(1024, 1024)
        self.decoder = ImageDecoder(1024, output_nc, ngf)
    def forward(self, input_svg, input_image):
        med_svg_vec = self.svg_encoder(input_svg)
        med_img_vec = self.image_encoder(input_image)
        med_img_fake_vec = self.connection(med_svg_vec)
        image = self.decoder(med_img_vec)
        image2 = self.decoder(med_img_fake_vec)
        return image, image2, med_img_vec, med_img_fake_vec




class SvgImageGenerator(nn.Module):
    def __init__(self, input_nc, output_nc, ngf = 64, norm_layer=nn.BatchNorm1d, use_dropout=False):
        super(SvgImageGenerator, self).__init__()
        self.encoder = SvgEncoder(input_nc, 1024, ngf)
        self.connection = nn.Linear(1024, 1024)
        self.decoder = ImageDecoder(1024, output_nc, ngf)



    def forward(self, input):
        med_vec = self.encoder(input)
        med_vec = med_vec.view([-1,1024])
        med_vec_attention = self.connection(med_vec)
        med_vec_attention = med_vec_attention.view([-1, 1024, 1, 1])
        output = self.decoder(med_vec_attention)
        return output



class ImageDecoder(nn.Module):
    def __init__(self, input_nc, output_nc, ngf = 64, norm_layer=nn.BatchNorm2d, use_dropout=False):
        super(ImageDecoder, self).__init__()
        model = [   nn.ConvTranspose2d(1024, 512, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(512), # 2 * 2
                    nn.ReLU(),
                    nn.ConvTranspose2d(512,  256, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(256), # 4 * 4
                    nn.ReLU(),
                    nn.ConvTranspose2d(256,  128, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(128), # 8 * 8
                    nn.ReLU(),
                    nn.ConvTranspose2d(128,  64,  kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(64), # 16 * 16
                    nn.ReLU(),
                    nn.ConvTranspose2d(64,   32, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(32), # 32 * 32
                    nn.ReLU(),
                    nn.ConvTranspose2d(32,   output_nc, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.Tanh()] # 64 * 64

        self.model = nn.Sequential(*model)

    def forward(self, input):
        output = self.model(input)
        # print(output.data.shape)
        return output




class SvgEncoder(nn.Module):
    def __init__(self, input_nc, output_nc, ngf = 64, norm_layer=nn.BatchNorm1d, use_dropout=False):
        super(SvgEncoder, self).__init__()
        type_out_nc = 32
        color_out_nc = 32
        position_out_nc = 64
        combine_in_nc = type_out_nc + color_out_nc + position_out_nc
        type_encoder = [nn.Conv1d(3, type_out_nc, kernel_size = 1),
                        nn.BatchNorm1d(type_out_nc)]
        color_encoder = [nn.Conv1d(3, color_out_nc, kernel_size = 1),
                        nn.BatchNorm1d(color_out_nc)]
        position_encoder = [nn.Conv1d(6, position_out_nc, kernel_size = 1),
                        nn.BatchNorm1d(position_out_nc)]

        self.type_encoder = nn.Sequential(*type_encoder) # 注意，我们的type是每种占用一个位置
        self.color_encoder = nn.Sequential(*color_encoder)
        self.position_encoder = nn.Sequential(*position_encoder)

        model = [nn.Conv1d(in_channels = 128, out_channels = 256, kernel_size = 3),
                nn.BatchNorm1d(256), # 5
                nn.LeakyReLU(0.2),
                nn.Conv1d(in_channels = 256, out_channels = 512, kernel_size = 3),
                nn.BatchNorm1d(512), # 3
                nn.LeakyReLU(0.2),
                nn.Conv1d(in_channels = 512, out_channels = 1024, kernel_size = 3)
                ] #(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)[source]
        self.combine_encoder = nn.Sequential(*model)

    def forward(self, x):
        # print("input: ",x.data.shape)
        type_in, position_in, color_in = torch.split(x,[3,6,3],dim = 1)
        type_out = self.type_encoder(type_in)
        position_out = self.position_encoder(position_in)
        color_out = self.color_encoder(color_in)
        total = torch.cat([type_out,position_out,color_out], 1)
        # print("total: ", total.data.shape)

        return self.combine_encoder(total)

class ImageEncoder(nn.Module):
    def  __init__(self, input_nc, output_nc, ngf = 64, norm_layer=nn.BatchNorm2d, use_dropout=False):
        super(ImageDecoder, self).__init__()
        model = [   nn.Conv2d(input_nc, 32, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(32), # 32 * 32
                    nn.Conv2d(32,  64, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(64), # 16 * 16
                    nn.Conv2d(64,  128, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(128), # 8 * 8
                    nn.Conv2d(128,  256,  kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(256), # 4 * 4
                    nn.Conv2d(256,   256, kernel_size = 4, stride = 2 , padding  = 1),
                    nn.BatchNorm2d(256), # 2 * 2
                    nn.Conv2d(256,   1024, kernel_size = 4, stride = 2 , padding  = 1)] # 64 * 64
        self.model = nn.Sequential(*model)

    def forward(self, input):
        output = self.model(input)
        return output

def print_network(net):
    num_params = 0
    for param in net.parameters():
        num_params += param.numel()
    print(net)
    print('Total number of parameters: %d' % num_params)
