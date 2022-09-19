import os
from pathlib import Path

from utils.augment_images import augment_images
from utils.rename_images import rename_images
from utils.crop_zeropad_resize_images import crop_zeropad_resize_images
from utils.train_validation_split import train_validation_split
from utils.generate_train import generate_train
from utils.generate_validation import generate_validation
from utils.generate_config_file import generate_config_file
from utils.move_train_and_valid_sets_to_one_folder import move_train_and_valid_sets_to_one_folder


if_need_to_augment = True
if_need_to_crop_zeropad_resize = True
if_need_to_rename = True

# if_need_to_augment = False
# if_need_to_crop_zeropad_resize = False
# if_need_to_rename = False


if_need_to_create_example_training_config_file = True

DATASET_NAME = 'dataset'
OUTPUT_TRAIN_VALID_FOLDER_NAME = 'output'

TRAIN_VALID_SPLIT_RATIO = 1 # if TRAIN_VALID_SPLIT_RATIO=0 it will create validation dataset only
                              # if TRAIN_VALID_SPLIT_RATIO=1 it will create train dataset only

def main():
    # os.system(f'rm -rf dataset_*')
    # os.system(f'rm -rf temp')
    # os.system(f'rm -rf {OUTPUT_TRAIN_VALID_FOLDER_NAME}')

    augmented_dataset = f'{DATASET_NAME}_augmented'
    crop_zeropad_resized_dataset = f'{DATASET_NAME}_cropped_zeropadded_resized'
    renamed_dataset = f'{DATASET_NAME}_renamed'
    train_dataset = f'{DATASET_NAME}_train'
    valid_dataset = f'{DATASET_NAME}_valid'

    current_folder = DATASET_NAME

    if not os.path.isdir(train_dataset) or not os.path.isdir(valid_dataset):
        if if_need_to_augment:
            print('Start augmenting')
            # augment_images(current_folder, augmented_dataset, 100)
            augment_images(current_folder, augmented_dataset, 10)
            current_folder = augmented_dataset

        if if_need_to_crop_zeropad_resize:
            print('Start cropping zeropadding and resizing')
            point = (200, 25)
            crop_shape = (250, 375)
            resize_shape = (112, 112)
            crop_zeropad_resize_images(current_folder, crop_zeropad_resized_dataset,
                point, crop_shape, resize_shape)
            current_folder = crop_zeropad_resized_dataset

        # current_folder = crop_zeropad_resized_dataset
        if if_need_to_rename:
            print('Start renaming')
            rename_images(current_folder, renamed_dataset)
            current_folder = renamed_dataset

        print('Start train/validation spliting')
        train_validation_split(current_folder, train_dataset, valid_dataset, ratio=TRAIN_VALID_SPLIT_RATIO)

    if os.path.isdir(train_dataset):
        print('Start train generation')
        generate_train(train_dataset)

    if os.path.isdir(valid_dataset):
        print('Start validation generation')
        generate_validation(valid_dataset)
    
    if if_need_to_create_example_training_config_file:
        generate_config_file(train_dataset, OUTPUT_TRAIN_VALID_FOLDER_NAME)
    move_train_and_valid_sets_to_one_folder(OUTPUT_TRAIN_VALID_FOLDER_NAME)

    print('Dataset creation finished!')
    print(f'Data that you need located here: \"{Path(OUTPUT_TRAIN_VALID_FOLDER_NAME).absolute()}\"')

if __name__ == '__main__':
    main()
