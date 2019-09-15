import torch
from util.image_pool import ImagePool
from .base_model import BaseModel
from torch.autograd import Variable
from . import networks


class SvgResnetGanModel(BaseModel):
    def name(self):
        return 'SvgResnetGanModel'

    @staticmethod
    def modify_commandline_options(parser, is_train=True):

        # changing the default values to match the pix2pix paper
        # (https://phillipi.github.io/pix2pix/)
        parser.set_defaults(pool_size=0, no_lsgan=False, norm='batch')
        parser.set_defaults(dataset_mode='svgresnet')
        parser.set_defaults(which_model_netG='svgresnet')
        parser.set_defaults(which_model_netD='discri1d')
        parser.set_defaults(lambda_L1=100)
        parser.set_defaults(n_layers_D=1)
        parser.set_defaults(loadSize=64)
        parser.set_defaults(fineSize=64)
        parser.set_defaults(output_nc=4)
        parser.set_defaults(lambda_G_GAN=1)
        parser.set_defaults(gpu_ids='0')
        if is_train:
            parser.add_argument('--lambda_L1', type=float, default=100.0, help='weight for L1 loss')

        return parser

    def initialize(self, opt):
        BaseModel.initialize(self, opt)
        self.random_error = opt.random_error
        self.sentences_number = opt.svgresnet_output

        self.isTrain = opt.isTrain
        self.need_mid = opt.need_mid
        if self.isTrain:
            if opt.pair_discr:
                self.need_mid = True

        # specify the training losses you want to print out. The program will call base_model.get_current_losses
        self.loss_names = ['G_MSE', 'G_GAN']

        # TODO: Add the pair D
        # specify the images you want to save/display. The program will call base_model.get_current_visuals

        self.visual_names = ['fake_B', 'real_B'] #['show_fake_B', 'show_real_B'] # currently, we don't need to visual
        if self.random_error:
            self.visual_names.append("random_B")


        # specify the models you want to save to the disk. The program will call base_model.save_networks and base_model.load_networks
        if self.isTrain:
            self.model_names = ['G','D_answer', 'D_pair']
        else:  # during test time, only load Gs
            self.model_names = ['G']
        # load/define networks
        input_nc = [int(i) for i in opt.input_nc_array.split(",")]
        output_nc = [int(i) for i in opt.output_nc_array.split(",")]
        print(input_nc)
        print(output_nc)

        self.netG = networks.define_G(input_nc, output_nc, opt.ngf,
                                      opt.which_model_netG, opt.norm, not opt.no_dropout, opt.init_type, opt.init_gain, self.gpu_ids, opt.svgresnet_output * 3, self.need_mid, opt.resnet_layer)

        if self.isTrain:
            self.pair_discr = opt.pair_discr
            if self.pair_discr:
                self.loss_names.append('D_pair')
                self.loss_names.append('G_pair')
                self.need_mid = True # 强制需要mid，

            use_sigmoid = opt.no_lsgan
            self.netD_answer = networks.define_D(opt.svgresnet_output * 3, opt.ndf,
                                          opt.which_model_netD,
                                          opt.n_layers_D, opt.norm, use_sigmoid, opt.init_type, opt.init_gain, self.gpu_ids, opt.leak_value)
            if opt.pair_discr:
                self.netD_pair = networks.define_D(3 + sum(output_nc), opt.ndf,
                                              opt.which_model_netD,
                                              opt.n_layers_D, opt.norm, use_sigmoid, opt.init_type, opt.init_gain, self.gpu_ids, opt.leak_value)


        if self.isTrain:
            # self.fake_AB_pool = ImagePool(opt.pool_size)
            # define loss functions
            self.criterionGAN = networks.GANLoss(use_lsgan=not opt.no_lsgan).to(self.device)
            self.criterionMSE = torch.nn.MSELoss() # I change to L2 loss

            # initialize optimizers
            self.optimizers = []
            self.optimizer_G = torch.optim.Adam(self.netG.parameters(),
                                                lr=opt.lr, betas=(opt.beta1, 0.999))
            self.optimizer_D_answer = torch.optim.Adam(self.netD_answer.parameters(),
                                                lr=opt.lr, betas=(opt.beta1, 0.999))
            self.optimizers.append(self.optimizer_G)
            self.optimizers.append(self.optimizer_D_answer)
            if opt.pair_discr:
                self.optimizer_D_pair = torch.optim.Adam(self.netD_pair.parameters(),
                                                    lr=opt.lr, betas=(opt.beta1, 0.999))
                self.optimizers.append(self.optimizer_D_pair)

        print('---------- Networks initialized -------------')
        networks.print_network(self.netG)
        if self.isTrain:
            networks.print_network(self.netD_answer)

            if opt.pair_discr:
                networks.print_network(self.netD_pair)
        print('-----------------------------------------------')

    def set_input(self, input):
        AtoB = self.opt.which_direction == 'AtoB'
        self.real_A = input['A'].to(self.device)
        self.real_B = input['B'].to(self.device)# modify this part to derect from A to B
        if self.random_error:
            self.random_B = input['B_r'].to(self.device)
            # print(self.real_A.shape)
            # print(self.real_B.shape)
            # print(self.random_B.shape)

        # self.show_real_B =
        self.image_paths = input['A_paths'] # note that, here we don't need the A_path

    def forward(self):
        if self.need_mid:
            self.fake_B, self.mid_A = self.netG(self.real_A)
        else:
            self.fake_B = self.netG(self.real_A)

        if not self.isTrain:
            return self.fake_B.cpu().numpy() + 0.5

    def backward_D(self):
        # Fake
        # stop backprop to the generator by detaching fake_B
        fake_B = Variable(self.fake_B.data)
        # print("the shape of fake_B is: ")
        # print(fake_B.data.shape)
        pred_fake = self.netD_answer(fake_B)
        self.loss_D_fake = self.criterionGAN(pred_fake, False)

        # Real
        real_B = self.real_B
        if self.random_error:
            real_B = self.random_B
        pred_real = self.netD_answer(real_B)
        self.loss_D_real = self.criterionGAN(pred_real, True)

        # Combined loss
        self.loss_D = (self.loss_D_fake + self.loss_D_real) * 0.5

        self.loss_D.backward()

    def backward_D_pair(self):
        # Fake
        # stop backprop to the generator by detaching fake_B
        # TODO: 如果是空白的话，那么不计入loss，这部分可能要输入的形式进行一定的变化，我们的

        fake_B_array = torch.split(self.fake_B, 3, dim = 1)
        real_B = self.real_B
        if self.random_error:
            real_B = self.random_B

        real_B_array = torch.split(real_B, 3, dim = 1)
        # print(real_B_array[0].shape)
        assert(real_B_array[0].shape[1] == 3)
        assert(len(real_B_array) == self.sentences_number)
        assert(len(fake_B_array) == self.sentences_number)

        self.loss_array = []

        for i in range(self.sentences_number):

            # Fake
            fake_AB = Variable(torch.cat((self.mid_A.data, fake_B_array[i].data), 1))

            # print("the shape of fake_B is: ")
            # print(fake_B.data.shape)
            pred_fake = self.netD_pair(fake_AB)
            loss_D_fake = self.criterionGAN(pred_fake, False)

            # Real
            real_AB = Variable(torch.cat((self.mid_A.data, real_B_array[i].data), 1))

            pred_real = self.netD_pair(real_AB)
            loss_D_real = self.criterionGAN(pred_real, True)

            # Combined loss
            loss_D = (loss_D_fake + loss_D_real) * 0.5
            self.loss_array.append(loss_D)

        self.loss_D_pair = self.loss_array[0]
        for i in range(1, self.sentences_number):
            self.loss_D_pair = self.loss_D_pair + self.loss_array[i]
        self.loss_D_pair = self.loss_D_pair / self.sentences_number
        self.loss_D_pair.backward()

    def backward_G(self):
        # First, G(A) should fake the discriminator
        fake_B = self.fake_B
        pred_fake = self.netD_answer(fake_B)
        self.loss_G_GAN = self.criterionGAN(pred_fake, True)

        # Second, G(A) = B
        # print(self.fake_B.shape)
        # print(self.real_B.shape)
        self.loss_G_MSE = self.criterionMSE(self.fake_B, self.real_B) * self.opt.lambda_L1

        self.loss_G_GAN = self.loss_G_GAN * self.opt.lambda_G_GAN

        self.loss_G = self.loss_G_GAN + self.loss_G_MSE

        if self.pair_discr:
            loss_pair_array = []
            fake_B_array = torch.split(self.fake_B, 3, dim = 1)
            for fake_B in fake_B_array:
                fake_AB = torch.cat((Variable(self.mid_A.data), fake_B), 1)
                pred_fake = self.netD_pair(fake_AB)
                loss_pair_array.append(self.criterionGAN(pred_fake, True))
            self.loss_G_pair = loss_pair_array[0]
            for i in range(1, len(loss_pair_array)):
                self.loss_G_pair = self.loss_G_pair + loss_pair_array[i]
            self.loss_G_pair = self.loss_G_pair / self.sentences_number * self.opt.lambda_G_Pair
            self.loss_G = self.loss_G + self.loss_G_pair

        self.loss_G.backward()

    def optimize_parameters(self):
        self.forward()
        # update D
        self.set_requires_grad(self.netD_answer, True)
        self.optimizer_D_answer.zero_grad()
        self.backward_D()
        self.optimizer_D_answer.step()
        self.set_requires_grad(self.netD_answer, False)

        if self.pair_discr:
            self.set_requires_grad(self.netD_pair, True)
            self.optimizer_D_pair.zero_grad()
            self.backward_D_pair()
            self.optimizer_D_pair.step()
            self.set_requires_grad(self.netD_pair, False)

        # update G
        self.optimizer_G.zero_grad()
        self.backward_G()
        self.optimizer_G.step()
    # def make_show(B):
    #     self.
