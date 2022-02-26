#!/bin/bash

#output_dir="/media/RAIDONE/radice/neural-networks-data/predictions/s2d-kitti-416x128"
#model_checkpoint="/media/RAIDONE/radice/neural-networks-data/struct2depth/models/kitti-416x128/model-495792"
#input_list_file="/media/RAIDONE/radice/neural-networks-data/splits/kitti_test_files.txt"
#dataset="kitti"
#
#python inference.py \
#    --logtostderr \
#    --file_extension png \
#    --depth \
#    --output_dir $output_dir \
#    --model_ckpt $model_checkpoint \
#    --dataset $dataset \
#    --input_list_file $input_list_file

output_dir="/media/RAIDONE/radice/neural-networks-data/predictions/s2d-kitti360-416x128"
model_checkpoint="/media/RAIDONE/radice/neural-networks-data/struct2depth/models/kitti-416x128/model-495792"
input_list_file="/media/RAIDONE/radice/neural-networks-data/splits/kitti360_test_files.txt"
dataset="kitti360"

python inference.py \
    --logtostderr \
    --file_extension png \
    --depth \
    --output_dir $output_dir \
    --model_ckpt $model_checkpoint \
    --dataset $dataset \
    --input_list_file $input_list_file

#output_dir="/media/RAIDONE/radice/neural-networks-data/predictions/s2d-oxford-416x128"
#model_checkpoint="/media/RAIDONE/radice/neural-networks-data/struct2depth/models/oxford-416x128/model-1162500"
#input_list_file="/media/RAIDONE/radice/neural-networks-data/splits/oxford_radar_test_files.txt"
#dataset="oxford"
#
#python inference.py \
#    --logtostderr \
#    --file_extension png \
#    --depth \
#    --output_dir $output_dir \
#    --model_ckpt $model_checkpoint \
#    --inference_crop $dataset \
#    --dataset $dataset \
#    --input_list_file $input_list_file