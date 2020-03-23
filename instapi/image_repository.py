import requests

from instapi.instagram_api_client import InstagramApiClient
from models.dto.media_list_information import MediaListResponse


class ImageRepository:
    apiClient: InstagramApiClient
    image_folder_path: str

    def __init__(self, api_token, image_folder_path='images/'):
        self.apiClient = InstagramApiClient(api_token)
        self.image_folder_path = image_folder_path

    def get_all_image_ids(self):
        image_ids = []

        media_list_response = self.apiClient.get_user_media_list()
        media_list_response.raise_for_status()

        media_list = MediaListResponse(media_list_response.json())

        image_ids += [media_info.id for media_info in media_list.image_info_list]
        while media_list.paging_info.next is not None:
            media_list_response = requests.get(media_list.paging_info.next)
            media_list_response.raise_for_status()
            media_list = MediaListResponse(media_list_response.json())
            image_ids += [media_info.id for media_info in media_list.image_info_list]

        return image_ids
