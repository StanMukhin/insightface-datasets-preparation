import os
import numpy as np
import cv2
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True


def make_dir_if_not_exists(path):
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)



def imread(img_path):
    image = Image.open(img_path)
    image = np.asarray(image)
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = image[:, :, : 3]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

