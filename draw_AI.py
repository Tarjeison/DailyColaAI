from datetime import datetime

from generation.GAN.traning import train_gan
from instapi.image_handler import ImageHandler
from instapi.image_repository import InstagramRepository
from processing.pre_processing import PreProcessor
from publishing.email import send_email_with_image_attachment
from utils.file_utils import get_all_file_names_in_folder

if __name__ == '__main__':
    repo = InstagramRepository("data/secrets/api_token.txt")
    handler = ImageHandler(repo)
    handler.update_image_folder()

    pre_processor = PreProcessor()
    pre_processor.update_processed_images()

    # Build the model of the day
    timestamp = str(datetime.now())
    model_name = 'daily_cola'
    train_gan(model_name='daily_cola', data_name=timestamp)

    # Publish image with last model result
    # TODO: Revise and move some logic away from main
    img_root_path = 'data/images/generated/{}/{}'.format(model_name, timestamp)
    generated_images = get_all_file_names_in_folder(img_root_path)
    generated_images.sort()
    img_path = img_root_path + '/{}.png'.format(generated_images[-1])
    email_password_fd = open('data/secrets/email_password.txt', "r")
    email_password = email_password_fd.readline()
    email_recipient_fd = open('data/secrets/email_recipient.txt', "r")
    email_recipient = email_recipient_fd.readline()
    send_email_with_image_attachment(img_path, 'dailycolaai@gmail.com', email_password,
                                     'dailcolaai@gmail.com', email_recipient)
