
# Copyright 2018 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

""" Offline data generation for the KITTI dataset."""

import os
from absl import app
from absl import flags
from absl import logging
import numpy as np
import cv2
import os, glob

import alignment
from alignment import compute_overlap
from alignment import align


SEQ_LENGTH = 3
WIDTH = 416
HEIGHT = 128
STEPSIZE = 1
INPUT_DIR = '/media/RAIDONE/radice/datasets/kitti/data'
OUTPUT_DIR = '/media/RAIDONE/radice/datasets/kitti/struct2depth'


def get_line(file, start):
    file = open(file, 'r')
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    ret = None
    for line in lines:
        nline = line.split(': ')
        if nline[0]==start:
            ret = nline[1].split(' ')
            ret = np.array([float(r) for r in ret], dtype=float)
            ret = ret.reshape((3,4))[0:3, 0:3]
            break
    file.close()
    return ret


def run_all():
  ct = 0

black = np.zeros((HEIGHT, WIDTH*3))

if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR = OUTPUT_DIR + '/'

for d in glob.glob(INPUT_DIR + '/*/'):
    date = d.split('/')[-2]

    if date == 'test-velodyne-gt':
        continue

    file_calibration = d + 'calib_cam_to_cam.txt'
    calib_raw = [get_line(file_calibration, 'P_rect_02'), get_line(file_calibration, 'P_rect_03')]

    for d2 in glob.glob(d + '*/'):
        seqname = d2.split('/')[-2]
        print('Processing sequence', seqname)
        for subfolder in ['image_02/data', 'image_03/data']:
            ct = 1
            seqname = d2.split('/')[-2]
            if not os.path.exists(os.path.join(OUTPUT_DIR, date, seqname, subfolder)):
                os.makedirs(os.path.join(OUTPUT_DIR, date, seqname, subfolder))

            calib_camera = calib_raw[0] if subfolder=='image_02/data' else calib_raw[1]
            folder = d2 + subfolder
            files = glob.glob(folder + '/*.png')
            files = [file for file in files if not 'disp' in file and not 'flip' in file and not 'seg' in file]
            files = sorted(files)
            for i in range(SEQ_LENGTH, len(files)+1, STEPSIZE):
                imgnum = str(ct).zfill(10)
                if os.path.exists(OUTPUT_DIR + seqname + '/' + imgnum + '.png'):
                    ct+=1
                    continue
                big_img = np.zeros(shape=(HEIGHT, WIDTH*SEQ_LENGTH, 3))
                wct = 0

                for j in range(i-SEQ_LENGTH, i):  # Collect frames for this sample.
                    img = cv2.imread(files[j])
                    ORIGINAL_HEIGHT, ORIGINAL_WIDTH, _ = img.shape

                    zoom_x = WIDTH/ORIGINAL_WIDTH
                    zoom_y = HEIGHT/ORIGINAL_HEIGHT

                    # Adjust intrinsics.
                    calib_current = calib_camera.copy()
                    calib_current[0, 0] *= zoom_x
                    calib_current[0, 2] *= zoom_x
                    calib_current[1, 1] *= zoom_y
                    calib_current[1, 2] *= zoom_y

                    calib_representation = ','.join([str(c) for c in calib_current.flatten()])

                    img = cv2.resize(img, (WIDTH, HEIGHT))
                    big_img[:,wct*WIDTH:(wct+1)*WIDTH] = img
                    wct+=1

                cv2.imwrite(os.path.join(OUTPUT_DIR, date, seqname, subfolder, '{}.png'.format(imgnum)), big_img)
                cv2.imwrite(os.path.join(OUTPUT_DIR, date, seqname, subfolder, '{}-fseg.png'.format(imgnum)), black)
                f = open(os.path.join(OUTPUT_DIR, date, seqname, subfolder, '{}_cam.txt'.format(imgnum)), 'w')
                f.write(calib_representation)
                f.close()
                ct+=1


def main(_):
  run_all()


if __name__ == '__main__':
  app.run(main)
