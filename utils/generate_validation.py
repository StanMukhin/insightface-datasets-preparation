import os
from utils import face_image
from utils.utils import make_dir_if_not_exists
from utils.pairs_generator import GeneratePairs

import mxnet as mx
from mxnet import ndarray as nd
import pickle
from utils import lfw


def dir2lst(input_dir, file_path):
    dataset = face_image.get_dataset_common(input_dir, 2)

    lines = []
    for item in dataset:
        s = "%d\t%s\t%d" % (1, item.image_path, int(item.classname))
        lines.append(s)
        # print("%d\t%s\t%d" % (1, item.image_path, int(item.classname)))

    text = '\n'.join(lines)

    with open(file_path, 'w') as file:
        file.write(text)


def create_pairs(data_dir, pairs_file_path):
    img_ext = ".jpg"
    generatePairs = GeneratePairs(data_dir, pairs_file_path, img_ext)
    generatePairs.generate()


def face2rec2(valid_dataset_path):
    os.system(f'python3 utils/face2rec2.py {valid_dataset_path}')


def lfw2pack(valid_dataset_path):
    # parser.add_argument('--data-dir', default='', help='')
    # parser.add_argument('--image-size', type=str, default='112,96', help='')
    # parser.add_argument('--output', default='', help='path to save.')
    # args = parser.parse_args()
    lfw_dir = valid_dataset_path
    image_size = [112, 112]
    lfw_pairs = lfw.read_pairs('temp/pairs.txt')
    lfw_paths, issame_list = lfw.get_paths(lfw_dir, lfw_pairs, 'jpg')
    lfw_bins = []
    #lfw_data = nd.empty((len(lfw_paths), 3, image_size[0], image_size[1]))
    i = 0
    for path in lfw_paths:
        with open(path, 'rb') as fin:
            _bin = fin.read()
            lfw_bins.append(_bin)
            #img = mx.image.imdecode(_bin)
            #img = nd.transpose(img, axes=(2, 0, 1))
            #lfw_data[i][:] = img
            i+=1
            if i%1000==0:
                print('loading lfw', i)

    with open('temp/lfw.bin', 'wb') as f:
        pickle.dump((lfw_bins, issame_list), f, protocol=pickle.HIGHEST_PROTOCOL)

def generate_validation(valid_dataset_path):
    make_dir_if_not_exists('temp')
    lst_file_path = 'temp/lfw.lst'
    pairs_file_path = 'temp/pairs.txt'

    print(valid_dataset_path)

    dir2lst(valid_dataset_path, lst_file_path)
    create_pairs(valid_dataset_path, pairs_file_path)
    face2rec2(valid_dataset_path)

    os.system(f'mv {valid_dataset_path}/lfw.idx temp')
    os.system(f'mv {valid_dataset_path}/lfw.rec temp')

    lfw2pack(valid_dataset_path)




