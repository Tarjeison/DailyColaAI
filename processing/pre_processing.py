import cv2
import numpy as np

from utils.file_utils import get_all_file_names_in_folder, create_directory_if_not_present


class PreProcessor:
    image_height: int
    image_width: int
    images_root: str
    processed_images_root: str
    raw_image_extension: str

    def __init__(self, images_root: str = 'data/images/raw/',
                 processed_images_root: str = 'data/images/pre_processed/1/',
                 image_height: int = 256, image_width: int = 256):
        self.image_height = image_height
        self.image_width = image_width
        self.images_root = images_root
        self.processed_images_root = processed_images_root
        create_directory_if_not_present(processed_images_root)

    def update_processed_images(self):
        print('Started pre-processing... Looking for un-processed images.')
        unprocessed_image_ids = get_all_file_names_in_folder(self.images_root)
        processed_image_ids = get_all_file_names_in_folder(self.processed_images_root)

        new_image_ids = list(set(unprocessed_image_ids) - set(processed_image_ids))
        print('A total of {} new images found.'.format(len(new_image_ids)))
        for image_id in new_image_ids:
            print('Processing image {} of {} (id: {}).'.
                  format(new_image_ids.index(image_id) + 1, len(new_image_ids), image_id))

            img = cv2.imread(self.images_root + image_id + '.jpg', cv2.IMREAD_UNCHANGED)
            img = self.resize_image(img)
            img = self.remove_image_noise(img)
            cv2.imwrite(self.processed_images_root + image_id + '.png', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

    def resize_image(self, img: np.ndarray) -> np.ndarray:
        img = cv2.resize(img, (self.image_height, self.image_width), interpolation=cv2.INTER_AREA)
        return img

    def remove_image_noise(self, img: np.ndarray):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (_, blackAndWhiteImage) = cv2.threshold(gray_image, 130, 255, cv2.THRESH_BINARY)
        return blackAndWhiteImage
