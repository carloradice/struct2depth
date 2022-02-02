import os
import random
import argparse

INPUT_DIR = '/media/RAIDONE/radice/datasets/kitti/'
OUTPUT_DIR = '/media/RAIDONE/radice/neural-networks-data/struct2depth/splits'


def fill_data(lines):
    data = []
    folder = 'struct2depth'
    count = 0
    for line in lines:
        path = line.rstrip().split()[0]
        path = path.split('/')

        date = path[0]
        sequence = path[1]
        # folder = 'image_02' or 'image_03'
        basename = path[4].split('.')[0]

        # Se esiste il file, aggiungerlo allo split
        # Ci sono meno di 22600 * 2 files poichè se il file è il primo o l'ultimo di una sequenza non viene
        # considerato in quanto la tripletta non avrebbe una delle 3 immagini
        fl = os.path.join(INPUT_DIR, folder, date, sequence, 'image_02', 'data', '{}.png'.format(basename))
        fr = os.path.join(INPUT_DIR, folder, date, sequence, 'image_03', 'data', '{}.png'.format(basename))
        if os.path.isfile(fl):
            l = os.path.join(INPUT_DIR, folder, date, sequence, 'image_02', 'data') + ' ' + '{}{}'.format(basename, '\n')
            data.append(l)
        if os.path.isfile(fr):
            r = os.path.join(INPUT_DIR, folder, date, sequence, 'image_03', 'data') + ' ' + '{}{}'.format(basename, '\n')
            data.append(r)
        count += 1
        print('{}/{}'.format(count, len(lines)))

    return data


def gen_train_file():
    file = open(INPUT_DIR + 'eigen_train_files.txt', 'r')
    lines = file.readlines()
    print(len(lines))
    train = fill_data(lines=lines)
    print(len(train))
    random.shuffle(train)
    file = open(os.path.join(OUTPUT_DIR, 'kitti_train_files.txt'), 'w')
    file.writelines(train)


if __name__ == '__main__':
    gen_train_file()