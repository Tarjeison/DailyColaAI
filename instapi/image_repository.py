from typing import List

import requests

from instapi.instagram_api_client import InstagramApiClient
from models.dto.image_url import ImageUrlResponse
from models.dto.media_list_information import MediaListResponse


class InstagramRepository:
    apiClient: InstagramApiClient

    def __init__(self, api_token):
        self.apiClient = InstagramApiClient(api_token)

    def get_all_image_ids(self) -> List[str]:
        image_ids = []

        media_list_response = self.apiClient.get_user_media_list()
        media_list_response.raise_for_status()

        media_list = MediaListResponse(media_list_response.json())
        # fancy
        image_ids += [media_info.id for media_info in media_list.image_info_list]
        while media_list.paging_info.next is not None:
            media_list_response = requests.get(media_list.paging_info.next)
            media_list_response.raise_for_status()
            media_list = MediaListResponse(media_list_response.json())
            image_ids += [media_info.id for media_info in media_list.image_info_list]

        return image_ids

    def get_image_url_from_id(self, media_id: str) -> ImageUrlResponse:
        url_response = self.apiClient.get_media_url(media_id)
        url_response.raise_for_status()
        return ImageUrlResponse.from_json(url_response.content)

    def get_image_from_url(self, url) -> bytes:
        image_response = requests.get(url)
        image_response.raise_for_status()
        return image_response.content
