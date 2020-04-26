from generation.GAN.traning import train_gan
from instapi.image_handler import ImageHandler
from instapi.image_repository import InstagramRepository
from processing.pre_processing import PreProcessor

if __name__ == '__main__':
    repo = InstagramRepository("api_token.txt")
    handler = ImageHandler(repo)
    handler.update_image_folder()

    pre_processor = PreProcessor()
    pre_processor.update_processed_images()

    # Training
    train_gan()
