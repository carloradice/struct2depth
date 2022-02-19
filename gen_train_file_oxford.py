import glob
import os
import random


INPUT_DIR = '/media/RAIDONE/radice/datasets/oxford/struct2depth'
OUTPUT_DIR = '/media/RAIDONE/radice/neural-networks-data/struct2depth/splits'


def main():

    files = []
    for file in glob.glob(INPUT_DIR + '/*/*/*/*-fseg.png'):

        basename = os.path.basename(file).split('-')[0]
        dirname = os.path.dirname(file)
        files.append('{} {}\n'.format(dirname, basename))

    random.shuffle(files)

    files = files[:50000]

    print(len(files))
    f = open(os.path.join(OUTPUT_DIR, 'oxford_train_files.txt'), 'w')
    f.writelines(files)
    f.close()


if __name__ == '__main__':
    main()