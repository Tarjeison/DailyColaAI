from instapi import instagram_api_client
from models.dto.media_list_information import MediaListResponse

if __name__ == '__main__':
    client = instagram_api_client.InstagramApiClient('api_token.txt')

    media_list = MediaListResponse(client.get_user_media_list().json())
    first_id = media_list.image_info_list[0].id
    print(first_id)

    first_media_url_response = client.get_media_url(first_id)
    print(first_media_url_response.content)
