#!/bin/bash

ckpt_dir="/media/RAIDONE/radice/neural-networks-data/struct2depth/models/oxford-416x128"
data_dir="/media/RAIDONE/radice/datasets/oxford/struct2depth"
imagenet_ckpt="/media/RAIDONE/radice/neural-networks-data/depth-and-motion-learning/models/resnet18/model.ckpt"

python train.py \
  --logtostderr \
  --checkpoint_dir $ckpt_dir \
  --data_dir $data_dir \
  --architecture resnet \
  --imagenet_ckpt $imagenet_ckpt