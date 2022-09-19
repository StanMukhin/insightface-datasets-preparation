import os
from pathlib import Path
import Augmentor

from tqdm import tqdm

from utils.utils import make_dir_if_not_exists

def get_augmentor(full_dir_path, new_full_dir_path):
    p = Augmentor.Pipeline(full_dir_path, new_full_dir_path)
    # p.gaussian_distortion(0.2, 7, 7, 5, "bell", "in")
    # p.flip_left_right(0.5)
    # p.rotate(0.2, 10, 10)
    # p.skew(0.2, 0.3)
    p.zoom(probability = 0.8, min_factor = 1.0, max_factor = 1.1)
    # p.random_brightness(1, 0.5, 1.5) # Too much!
    # p.random_brightness(1, 0.75, 1.25)
    p.random_brightness(1, 0.85, 1.15)
    p.random_color(0.2, 0, 1.1)
    p.random_contrast(0.2, 1, 1.1)
    # p.random_distortion(0.2, 5, 5, 5)
    # p.shear(0.2, 1, 2)

    return p

def augment_images(input_dataset_path, output_dataset_path, sample_count):
    input_dataset_path = Path(input_dataset_path).absolute().as_posix()
    output_dataset_path = Path(output_dataset_path).absolute().as_posix()

    make_dir_if_not_exists(output_dataset_path)

    for (dirpath, dirnames, filenames) in os.walk(input_dataset_path):
        for dirname in dirnames:
            full_dir_path = Path(dirpath, dirname).as_posix()
            new_full_dir_path = full_dir_path.replace(input_dataset_path, output_dataset_path)
            make_dir_if_not_exists(new_full_dir_path)

    for (dirpath, dirnames, filenames) in os.walk(input_dataset_path):
        for dirname in tqdm(dirnames):
            full_dir_path = Path(dirpath, dirname).as_posix()
            new_full_dir_path = full_dir_path.replace(input_dataset_path, output_dataset_path)
            if len(os.listdir(full_dir_path)) < sample_count:
                p = get_augmentor(full_dir_path, new_full_dir_path)
                p.sample(sample_count)
            else:
                print(f'Doesn\'t need to augment, sample_count ({sample_count}) '
                    f'less then files count {len(os.listdir(full_dir_path))}')
                files = os.listdir(full_dir_path)
                for file in files:
                    os.system(f'cp {full_dir_path}/{file} {new_full_dir_path}')


if __name__ == '__main__':
    input_dir_path = "test"
    output_dir_path = "output"

    make_dir_if_not_exists(output_dir_path)

    p = get_augmentor(input_dir_path, output_dir_path)

    p.sample(30)
