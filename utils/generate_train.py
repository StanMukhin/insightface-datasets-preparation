import os

def generate_train(train_dataset_path):
    os.system(f'python -m mxnet.tools.im2rec --list --recursive train {train_dataset_path}')
    os.system(f'python -m mxnet.tools.im2rec --num-thread 16 --quality 100 train {train_dataset_path}')


