# AutoCaption

## To run the code 



cd machinelearning

python3 test_numpy.py --name 20180918_full_ocq_rule_more_channels --model svgresnetgan  --svgresnet_output 6 --fix_size -1 --ngf 384 --input_nc_array 3,6,3,1,1,1,15,15,15 --output_nc_array 3,10,3,3,3,3,3,3,3 --server_port 8000 --gpu_ids -1 --show
