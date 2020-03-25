from instapi.image_repository import InstagramRepository
from instapi.image_handler import ImageHandler

if __name__ == '__main__':

    repo = InstagramRepository('api_token.txt')
    handler = ImageHandler(repo, 'images/')
    handler.update_image_folder()
