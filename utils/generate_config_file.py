import os
from pathlib import Path

EXAMPLE_CONFIG_PATH = "res/config.py"

def generate_config_file(train_dataset_path, output_set_path):
    with open(EXAMPLE_CONFIG_PATH) as file:
        text = file.read()

    text = text.replace('TRAIN_DATASET_PATH', f'\"{Path(output_set_path).absolute()}\"')
    
    if os.path.isdir(train_dataset_path):
        dirs = os.listdir(train_dataset_path)
        classes_count = len(dirs)

        files_count = 0

        for dirname in dirs:
            dir_path = f'{train_dataset_path}/{dirname}'

            files = os.listdir(dir_path)

            files_count += len(files)

        text = text.replace('CLASSES_COUNT', str(classes_count))
        text = text.replace('IMAGES_COUNT', str(files_count))

    with open('config.py', 'w') as file:
        file.write(text)


