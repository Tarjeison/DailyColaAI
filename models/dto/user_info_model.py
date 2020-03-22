from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class UserInfoDto:
    id: str
    username: str

