import json
from dataclasses import dataclass
from typing import List


@dataclass
class ImageInfo:
    id: str
    caption: str


@dataclass
class PagingCursors:
    before: str
    after: str


@dataclass
class PagingInfo:
    cursors: PagingCursors
    next: str


@dataclass
class MediaListResponse:
    image_info_list: List[ImageInfo]
    paging_info: PagingInfo

    def __init__(self, response: json):
        self.image_info_list = list()
        for image_info in response['data']:
            self.image_info_list.append(
                ImageInfo(image_info['id'], image_info['caption'])
            )

        paging_next = None
        try:
            paging_next = response['paging']['next']
        except KeyError:
            pass

        self.paging_info = PagingInfo(PagingCursors(response['paging']['cursors']['before'],
                                                    response['paging']['cursors']['after']), paging_next)
