#!/bin/bash

output_dir="/media/RAIDONE/radice/neural-networks-data/struct2depth/predictions/kitti/"
model_checkpoint="/media/RAIDONE/radice/neural-networks-data/struct2depth/models/kitti/model-56340"
input_list_file="/media/RAIDONE/radice/neural-networks-data/struct2depth/splits/kitti_test_files.txt"

python inference.py \
    --logtostderr \
    --file_extension png \
    --depth \
    --output_dir $output_dir \
    --model_ckpt $model_checkpoint \
    --input_list_file $input_list_file