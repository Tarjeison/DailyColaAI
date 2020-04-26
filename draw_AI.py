from instapi.image_repository import InstagramRepository
from instapi.image_handler import ImageHandler
from processing.pre_processing import PreProcessor

if __name__ == '__main__':
    repo = InstagramRepository("api_token.txt")
    handler = ImageHandler(repo)
    handler.update_image_folder()

    pre_processor = PreProcessor()
    pre_processor.update_processed_images()
