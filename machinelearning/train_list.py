python3 train.py --dataroot ./datasets/facades --name 20180804try --model svg2image --gpu_ids -1

python3 test.py --dataroot ./datasets/facades --name 20180804try --model svg2image --gpu_ids 0

change it into MSE loss
change the

python3 train.py --dataroot ./datasets/facades --name 20180806_test --model svg2image

python3 train.py --dataroot ./datasets/facades --name 20180807_change_embedding --model svg2image


python3 train.py --dataroot ./datasets/facades --name 20180807_without_D --model svg2image

python3 train.py --dataroot ./datasets/facades --name 20180807_try_resnet --model pix2pix --which_model_netG resnet_9blocks --dataset_mode aligned

I forgot an important part of the model, Relu and LeakyReLU are missed from the model, So I add back to see the effect.

python3 train.py --dataroot ./datasets/facades --name 20180808_try_resnet --model svgresnet --gpu_ids -1 --display_frec 40
# In my own computer, it's like this.

python3 train.py --dataroot ./datasets/facades --name 20180808_try_resnet --model svgresnet  --display_freq 40

python3 train.py --dataroot ./datasets/20180809_svg2focal --name 20180809_try_resnet --model svgresnet  --display_freq 40

python3 test.py --dataroot ./datasets/20180809_svg2focal --name 20180809_try_resnet --model svgresnet

python3 train.py --dataroot ./datasets/20180811_svg2min3 --name 20180811_min3_resnet --model svgresnet  --display_freq 40

python3 test.py --dataroot ./datasets/20180811_svg2min3 --name 20180811_min3_resnet --model svgresnet

python3 train.py --dataroot ./datasets/20180809_svg2focal --name 20180811_max_resnet --model svgresnet

python3 test.py --dataroot ./datasets/20180809_svg2focal --name 20180811_max_resnet --model svgresnet

20180812

python3 train.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3 --model svgresnet  --svgresnet_output 2

python3 test.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3 --model svgresnet  --svgresnet_output 2

python3 train.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3_batchsize_4 --model svgresnet  --svgresnet_output 2 --batchSize 4 --gpu_ids 0,1

python3 test.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3_batchsize_4 --model svgresnet  --svgresnet_output 2

python3 train.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3_batchsize_36 --model svgresnet  --svgresnet_output 2 --batchSize 36

python3 test.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180812_svg2max_min3_batchsize_36 --model svgresnet  --svgresnet_output 2

20180814
python3 train.py --dataroot ./datasets/20180812_svg2max_min3 --name 20180814_svg2max_min3 --model svgresnet  --svgresnet_output 2

20180820
python3 train.py --dataroot ./datasets/20180820_real_data --name 20180820_try --model svgresnet  --svgresnet_output 2 --fix_size -1

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180820_try --model svgresnet  --svgresnet_output 2 --fix_size -1

20180821

python3 test.py --dataroot ./datasets/20180821_real_data --name 20180820_try --model svgresnet  --svgresnet_output 2 --fix_size -1

20180822

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_try_discriminate --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_try_discriminate --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --no_lsgan

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --no_lsgan

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_more --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.5

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_more --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_08 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_08 --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 train.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_08_input_normal --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8

python3 test.py --dataroot ./datasets/20180820_real_data --name 20180822_discriminator_lumbda_100_no_sigmoid_leak_08_input_normal --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_discr_la_100_no_sig_le_8_in_nor_right_max --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8

python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_discr_la_100_no_sig_le_8_in_nor_right_max --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 test.py --dataroot ./datasets/20180822_self --name 20180822_discr_la_100_no_sig_le_8_in_nor_right_max --model svgresnetgan  --svgresnet_output 2 --fix_size -1

python3 test_numpy.py --dataroot ./datasets/20180822_self --name 20180822_discr_la_100_no_sig_le_8_in_nor_right_max --model svgresnetgan  --svgresnet_output 2 --fix_size -1


python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order

python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1
python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --random_order
python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1


python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_128 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 128

python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order_ngf_128 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 128
python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order_ngf_128 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --random_order  --ngf 128
python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_128 --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 128


python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256

python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order_ngf_256 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256
python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order_ngf_256 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --random_order  --ngf 256
python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256 --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 256


python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_1024 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 1024

# Tring:

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_small_encoder --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3

python3 test.py --dataroot ./datasets/20180822_self --name 20180822_random_order_ngf_256_small_encoder --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3

python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_small_encoder --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --random_error


#To try:

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_small_encoder --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 2,2,2,2,2,2,2,2

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_small_encoder_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3

python3 test.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180822_random_order_ngf_256_small_encoder_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180823_try_pair --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180823_try_pair --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 1

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180823_try_pair --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 0

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180823_try_pair_no_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 1 --random_error

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180824_try_pair_l1_10_gan_0 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --random_error --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0

python3 train.py --dataroot ./datasets/20180822_fix_max_real_data --name 20180824_try_pair_l1_10_gan_0_no_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0

20180825
python3 train.py --dataroot ./datasets/20180825_many_people --name 20180825_many_people --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0

python3 train.py --dataroot ./datasets/20180825_many_people --name 20180825_many_people_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_error

python3 test.py --dataroot ./datasets/20180825_many_people --name 20180825_many_people_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3  --gpu_ids 0

python3 test_numpy.py --dataroot ./datasets/20180825_many_people --name 20180825_many_people_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1  --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3  --gpu_ids -1


20180826

python3 test.py --dataroot ./datasets/20180822_self --name 20180824_try_pair_l1_10_gan_0_no_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --gpu_ids -1

python3 test_numpy.py --dataroot ./datasets/20180822_self --name 20180824_try_pair_l1_10_gan_0_no_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --random_order --ngf 256 --output_nc_array 3,3,3,3,3,3,3,3 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180826_ljc_data --name 20180826_jiangliuchen_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_error

20180827

python3 train.py --dataroot ./datasets/20180827_liucan_cq --name 20180827_liucan_cq_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_error

python3 train.py --dataroot ./datasets/20180827_liucan_cq --name 20180827_liucan_cq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_error

python3 test_numpy.py --name 20180827_liucan_cq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180827_liucan_cq --name 20180827_liucan_cq_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --random_order --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_error --continue_train

python3 train.py --dataroot ./datasets/20180827_liucan_cq --name 20180827_liucan_cq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --leak_value 0.8 --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --continue_train

20180828
python3 test_numpy.py --name 20180827_liucan_cq_random_error --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3

python3 test_numpy.py --name 20180827_liucan_cq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3 --gpu_ids -1

python3 test.py --dataroot ./datasets/20180828_liucan_oq --name 20180828_liucan_oq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 1 --fix_size -1  --ngf 256 --output_nc_array 3,10,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180828_liucan_oq --name 20180828_liucan_oq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --leak_value 0.8 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0

python3 test_numpy.py --name 20180828_liucan_oq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --gpu_ids -1

python3 test.py --dataroot ./datasets/20180828_liucan_oq --name 20180828_liucan_oq_random_error_no_random_order --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180828_liucan_oq --name 20180828_liucan_oq_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0 --random_order --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180828_liucan_oq_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3

20180903
python3 train.py --dataroot ./datasets/20180903_rule_ocq --name 20180903_rule_ocq_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180903_rule_ocq_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3

python3 train.py --dataroot ./datasets/20180903_rule_ocq --name 20180903_rule_ocq_random_error_random_order --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --leak_value 0.8 --random_error --random_order

20180904
python3 train.py --dataroot ./datasets/20180903_rule_ocq --name 20180903_rule_ocq_resnet_20 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --leak_value 0.8 --resnet_layer 20

python3 train.py --dataroot ./datasets/20180903_rule_ocq --name 20180903_rule_ocq_resnet_20_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --leak_value 0.8 --resnet_layer 20 --random_error &

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_random_error --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 10  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_resnet_15_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --resnet_layer 15

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_resnet_15_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --resnet_layer 15

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_512_resnet_15_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 512 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --resnet_layer 15

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_512_resnet_15_random_error_L_100_larger_encoder --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 512 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 10,10,10,10,10,10,20,20,20 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --resnet_layer 15

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_512_random_error_L_100_larger_encoder --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 512 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 10,10,10,10,10,10,20,20,20 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 train.py --dataroot ./datasets/20180904_rule_ocq --name 20180904_rule_ocq_resnet_20_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --resnet_layer 20

20180904

python3 test_numpy.py --name 20180904_rule_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8111

python3 train.py --dataroot ./datasets/20180905_rule_ocq --name 20180905_rule_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180905_rule_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 1 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8111 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180904_comper_trend_ave_ocq --name 20180904_comper_trend_ave_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error &

python3 test_numpy.py --name 20180904_comper_trend_ave_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8112 --gpu_ids -1

20180905

python3 train.py --dataroot ./datasets/20180905_comper_trend_ave_noorder_ocq --name 20180905_comper_trend_ave_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error &

python3 test_numpy.py --name 20180905_comper_trend_ave_ocq_random_error_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8113 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180905_com_tr_a_noorder_large_ocq --name 20180905_com_large_dataset_random_error_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error &

20180910

python3 train.py --dataroot ./datasets/20180910_sum_trend_compare_ave_trend_ocq --name 20180910_many_L_100 --model svgresnetgan  --svgresnet_output 2 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error &

20180911

python3 train.py --dataroot ./datasets/20180911_order_ocq --name 20180911_order_ocq_L100 --model svgresnetgan  --svgresnet_output 3 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error &

python3 test_numpy.py --name 20180911_order_ocq_L100 --model svgresnetgan  --svgresnet_output 3 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8114 --gpu_ids -1

20180914

python3 train.py --dataroot ./datasets/20180914_rule_ocq --name 20180914_rule_ocq_L100 --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error --continue_train

python3 test_numpy.py --name 20180914_rule_ocq_L100 --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8115 --gpu_ids -1

20180915
python3 train.py --dataroot ./datasets/20180915_ocq_order_new_parse --name 20180915_ocq_order_new_parse --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180915_ocq_order_new_parse --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8115 --gpu_ids -1

20180916
python3 train.py --dataroot ./datasets/20180916_rule_ocq --name 20180916_rule_ocq --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180916_rule_ocq --model svgresnetgan  --svgresnet_output 5 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8115 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180916_full_ocq_rule --name 20180916_full_ocq_rule --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180916_full_ocq_rule --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8115 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180916_full_ocq_rule --name 20180916_full_ocq_rule_larger_encoder --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,5,5,5,5,5,5,5 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 train.py --dataroot ./datasets/20180916_full_ocq_rule --name 20180916_full_ocq_rule_deeper --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --resnet_layer 20 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 train.py --dataroot ./datasets/20180916_full_ocq_rule --name 20180916_full_ocq_rule_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180916_full_ocq_rule_deeper --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --resnet_layer 20 --server_port 8115 --gpu_ids -1

python3 test_numpy.py --name 20180916_full_ocq_rule_larger_encoder --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 256 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,5,5,5,5,5,5,5 --server_port 8115 --gpu_ids -1

python3 train.py --dataroot ./datasets/20180916_ocq_rule_real --name 20180916_ocq_rule_real_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180916_ocq_rule_real_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8115 --gpu_ids -1

20180918

python3 train.py --dataroot ./datasets/20180918_full_ocq_rule --name 20180918_full_ocq_rule_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --pair_discr --lambda_L1 100  --lambda_G_GAN 0  --leak_value 0.8 --random_error

python3 test_numpy.py --name 20180918_full_ocq_rule_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8888 --gpu_ids -1

20180919

python3 test_numpy.py --name 20180918_full_ocq_rule_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8000 --gpu_ids -1 --show
