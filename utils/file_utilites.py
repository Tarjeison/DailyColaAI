from os import listdir
from os.path import splitext, isfile, join
from typing import List


def get_all_file_names_in_folder(root_folder: str) -> List[str]:
    file_names = [splitext(f)[0] for f in listdir(root_folder) if isfile(join(root_folder, f))]
    return file_names

