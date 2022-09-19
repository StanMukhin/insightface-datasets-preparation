import os
from pathlib import Path
from tqdm import tqdm

from utils.utils import make_dir_if_not_exists

def get_files_count(dataset_path):
    count = 0
    max_count_of_files_in_dir = 0
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        for filename in filenames:
            if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                path = os.sep.join([dirpath, filename])
                count += 1

        if len(filenames) > max_count_of_files_in_dir:
            max_count_of_files_in_dir = len(filenames)

    return max_count_of_files_in_dir, count

def rename_images(input_dataset_path, output_dataset_path):
    input_dataset_path = Path(input_dataset_path).absolute().as_posix()
    output_dataset_path = Path(output_dataset_path).absolute().as_posix()
    # output_dataset_path = output_dataset_path.replace('-', '')

    make_dir_if_not_exists(output_dataset_path)

    for (dirpath, dirnames, filenames) in os.walk(input_dataset_path):
        for dirname in dirnames:
            full_dir_path = Path(dirpath, dirname).as_posix()
            new_full_dir_path = full_dir_path.replace(input_dataset_path, output_dataset_path)
            # new_full_dir_path = new_full_dir_path.replace('-', '')
            make_dir_if_not_exists(new_full_dir_path)

    max_count_of_files_in_dir, files_count = get_files_count(input_dataset_path)
    zero_pad_num = 4

    if zero_pad_num >= len(str(max_count_of_files_in_dir)):
        print('Danger...')
    
    pbar = tqdm(total=files_count)

    for (dirpath, dirnames, filenames) in os.walk(input_dataset_path):
        for filename_index in range(len(filenames)):
            filename = filenames[filename_index]
            full_file_path = Path(dirpath, filename).as_posix()
            extension = Path(full_file_path).suffix
            if extension == '.jpeg':
                extension = '.jpg'
            new_file_name = f'{Path(full_file_path).parent.name}'
            new_file_name = f'{new_file_name}_{str(filename_index + 1).zfill(zero_pad_num)}{extension}'
            new_full_file_path = Path(Path(full_file_path).parent, new_file_name).as_posix()
            new_full_file_path = new_full_file_path.replace(input_dataset_path, output_dataset_path)
            # new_full_file_path = new_full_file_path.replace('-', '')

            os.system(f'cp {full_file_path} {new_full_file_path}')

            pbar.update(1)

    pbar.close()








