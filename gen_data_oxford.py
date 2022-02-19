
from absl import app
import numpy as np
import cv2
import os, glob


SEQ_LENGTH = 3
WIDTH = 416
HEIGHT = 128
STEPSIZE = 1
INPUT_DIR = '/media/RAIDONE/radice/datasets/oxford/data'
OUTPUT_DIR = '/media/RAIDONE/radice/datasets/oxford/struct2depth'

FX = 983.044006
FY = 983.044006
CX = 643.646973
CY = 493.378998


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


def crop(img, fx, fy, cx, cy):
    # Perform center cropping, preserving 50% vertically.
    middle_perc = 0.50
    left = 1-middle_perc
    half = left/2
    a = img[int(img.shape[0]*(half)):int(img.shape[0]*(1-half)), :]
    cy /= (1/middle_perc)

    # Resize to match target height while not preserving aspect ratio.
    wdt = WIDTH
    x_scaling = float(wdt)/a.shape[1]
    y_scaling = 128.0/a.shape[0]
    b = cv2.resize(a, (wdt, 128))

    # Adjust intrinsics.
    fx*=x_scaling
    fy*=y_scaling
    cx*=x_scaling
    cy*=y_scaling

    # Perform center cropping horizontally.
    remain = b.shape[1] - 416
    cx /= (b.shape[1]/416)
    c = b[:, int(remain/2):b.shape[1]-int(remain/2)]

    return c, fx, fy, cx, cy


def run_all():
  ct = 0

black = np.zeros((HEIGHT, WIDTH*3))

if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR = OUTPUT_DIR + '/'

for d in glob.glob(INPUT_DIR + '/*'):
    date = os.path.basename(d)

    print('Processing sequence', date)

    for subfolder in glob.glob(d + '/stereo/*'):
        ct = 1
        folder = os.path.basename(subfolder)
        if not os.path.exists(os.path.join(OUTPUT_DIR, date, 'stereo', folder)):
            os.makedirs(os.path.join(OUTPUT_DIR, date, 'stereo', folder))

        files = glob.glob(subfolder + '/*.png')
        files = [file for file in files if not 'disp' in file and not 'flip' in file and not 'seg' in file]
        files = sorted(files)

        for i in range(SEQ_LENGTH, len(files)+1, STEPSIZE):
            imgnum = str(ct).zfill(10)
            if os.path.exists(os.path.join(OUTPUT_DIR, date, 'stereo', folder,  '{}.png'.format(imgnum))):
                ct+=1
                continue
            big_img = np.zeros(shape=(HEIGHT, WIDTH*SEQ_LENGTH, 3))
            wct = 0

            for j in range(i-SEQ_LENGTH, i):  # Collect frames for this sample.
                img = cv2.imread(files[j])

                # Adjust intrinsics.
                c, fx, fy, cx, cy = crop(img, FX, FY, CX, CY)


                big_img[:,wct*WIDTH:(wct+1)*WIDTH] = c
                wct+=1

            cv2.imwrite(os.path.join(OUTPUT_DIR, date, 'stereo', folder, '{}.png'.format(imgnum)), big_img)
            cv2.imwrite(os.path.join(OUTPUT_DIR, date, 'stereo', folder, '{}-fseg.png'.format(imgnum)), black)
            f = open(os.path.join(OUTPUT_DIR, date, 'stereo', folder, '{}_cam.txt'.format(imgnum)), 'w')
            f.write(str(fx) + ',0.0,' + str(cx) + ',0.0,' + str(fy) + ',' + str(cy) + ',0.0,0.0,1.0')
            f.close()
            ct+=1


def main(_):
  run_all()


if __name__ == '__main__':
  app.run(main)
