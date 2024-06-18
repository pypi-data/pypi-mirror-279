from enum import Enum
from typing import Union

from koyomin.core.interfaces.user import IUser

class LoggedStatus(Enum):
    ONLINE = True
    OFFLINE = False

class User(IUser):
    def __init__(self):
        self.code: Union[str, None] = None
        self.__token: Union[str, None] = None
        self.__refresh_token: Union[str, None] = None
        self.is_logged_in: bool = False

    def add_access_token(self, token: str):
        self.__token = token

    def add_refresh_token(self, refresh_token: str):
        self.__refresh_token = refresh_token
        
    def add_user_code(self, code: str):
        self.code = code

    def set_logged_status(self, status: LoggedStatus) -> None:
        self.is_logged_in = status.value

    def __repr__(self):
        return f"User(token={self.__token})"

user = User()