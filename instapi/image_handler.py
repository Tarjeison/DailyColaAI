from instapi.image_repository import InstagramRepository
from utils.file_utilites import get_all_file_names_in_folder


class ImageHandler:
    image_repository: InstagramRepository
    root_folder: str
    image_extension: str

    def __init__(self, image_repository: InstagramRepository, root_folder: str, image_extension: str = '.jpg'):
        self.image_repository = image_repository
        self.root_folder = root_folder
        self.image_extension = image_extension

    def update_image_folder(self):
        print('Updating images...')
        image_ids_repo = self.image_repository.get_all_image_ids()
        image_ids_folder = get_all_file_names_in_folder(self.root_folder)
        new_image_ids = list(set(image_ids_repo) - set(image_ids_folder))
        print('Found {} new images'.format(len(new_image_ids)))

        for image_id in new_image_ids:
            print('Downloading image {} of {}'.format(new_image_ids.index(image_id), len(new_image_ids)))
            image_url = self.image_repository.get_image_url_from_id(image_id)
            image_raw = self.image_repository.get_image_from_url(image_url.media_url)

            file = open(self.root_folder + image_id + self.image_extension, 'wb')
            file.write(image_raw)
            file.close()
