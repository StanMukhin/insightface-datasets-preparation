import os
from pathlib import Path

from utils.utils import make_dir_if_not_exists

GENERATED_FILES = ['train.idx', 'train.lst', 'train.rec', 'config.py', 'temp/lfw.bin']

def move_train_and_valid_sets_to_one_folder(output_folder):
    make_dir_if_not_exists(output_folder)

    for file in GENERATED_FILES:
        if os.path.isfile(file):
            os.system(f'mv {file} {output_folder}')

