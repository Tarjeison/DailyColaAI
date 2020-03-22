import requests
from models.dto.user_info_model import UserInfoDto


class InstagramApiClient:
    api_token: str
    user_info: UserInfoDto
    instagram_base_path: str = 'https://graph.instagram.com/'

    def __init__(self, api_token_file_path: str):
        token_file = open(api_token_file_path, "r")
        self.api_token = token_file.readline()
        self.user_info = UserInfoDto.from_json(self.get_user_info().content)

    def get_user_info(self):
        url = self.instagram_base_path + 'me?fields=id,username&access_token=' + self.api_token
        return requests.get(url)

    def get_user_media_list(self):
        url = self.instagram_base_path + self.user_info.id + '/media?fields=id,caption&access_token=' + self.api_token
        return requests.get(url)

    def get_media_url(self, media_id: str):
        url = self.instagram_base_path + media_id + '?fields=media_url&access_token=' + self.api_token
        return requests.get(url)
