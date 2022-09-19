import os
import random

from tqdm import tqdm

from utils.utils import make_dir_if_not_exists

def train_validation_split(input_dataset_path, train_dataset_path, valid_dataset_path, ratio):
    classes_dirs = os.listdir(input_dataset_path)

    train_dirs_count = int(len(classes_dirs) * ratio)
    valid_dirs_count = len(classes_dirs) - train_dirs_count
    
    if train_dirs_count >= len(classes_dirs):
        train_dirs_count = len(classes_dirs)
        os.system(f'cp -rf {input_dataset_path} {train_dataset_path}')
    elif train_dirs_count <= 0:
        os.system(f'cp -rf {input_dataset_path} {valid_dataset_path}')
    else:
        make_dir_if_not_exists(train_dataset_path)
        make_dir_if_not_exists(valid_dataset_path)

        train_dirs = random.sample(classes_dirs, train_dirs_count)

        for dirname in tqdm(classes_dirs):
            dir_path = f'{input_dataset_path}/{dirname}'
            if dirname in train_dirs:
                os.system(f'cp -rf {dir_path} {train_dataset_path}')
            else:
                os.system(f'cp -rf {dir_path} {valid_dataset_path}')

