import os
from pathlib import Path

import cv2
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

import numpy as np

from tqdm import tqdm

from utils.utils import imread

def make_dir_if_not_exists(path):
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

def zero_padding(src):
    if src.shape[0] > src.shape[1]:
        top = 0
        bottom = 0
        left = int((src.shape[0] - src.shape[1]) / 2)
        right = (src.shape[0] - src.shape[1]) - left

        image = cv2.copyMakeBorder(src, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    else:
        print('That staff hasn\'t been realized!')

    # cv2.imwrite('temp.jpg', image)

    return image


def get_files_count(dataset_path):
    count = 0
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        for filename in filenames:
            if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                path = os.sep.join([dirpath, filename])
                count += 1

    return count


def crop_zeropad_resize_images(input_dataset_path, output_dataset_path, point, size, resize_shape):
    make_dir_if_not_exists(output_dataset_path)

    min_x = point[0]
    min_y = point[1]

    max_x = min_x + size[0]
    max_y = min_y + size[1]

    files_count = get_files_count(input_dataset_path)
    pbar = tqdm(total=files_count)
    
    for (dirpath, dirnames, filenames) in os.walk(input_dataset_path):
        output_dir_path = dirpath.replace(input_dataset_path, output_dataset_path)
        # make_dir_if_not_exists(output_dir_path)

        for filename in filenames:
            if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.sep.join([dirpath, filename])
                # img = cv2.imread(img_path)
                # print(img_path)
                img = imread(img_path)

                output_img_path = img_path.replace(input_dataset_path, output_dataset_path)

                if img.shape[0] == 640 or img.shape[1] == 640:
                    make_dir_if_not_exists(output_dir_path)
                    
                    crop = img[min_y:max_y, min_x:max_x]
                    crop = zero_padding(crop)

                    resized = cv2.resize(crop, resize_shape)

                    cv2.imwrite(output_img_path, resized)

                pbar.update(1)
    pbar.close()
