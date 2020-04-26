from os import listdir, makedirs
from os.path import splitext, isfile, join, exists, dirname
from typing import List
import numpy as np

from PIL import Image


def get_all_file_names_in_folder(root_folder: str) -> List[str]:
    try:
        file_names = [splitext(f)[0] for f in listdir(root_folder) if isfile(join(root_folder, f))]

    except FileNotFoundError:
        file_names = []

    return file_names


def open_all_images_in_folder(root_folder: str) -> List[np.array]:
    images = [np.asarray(Image.open(root_folder + '/' + file))
              for file in listdir(root_folder) if (isfile(join(root_folder, file)))]

    return images


def create_directory_if_not_present(path: str):
    if not exists(dirname(path)):
        makedirs(dirname(path))
