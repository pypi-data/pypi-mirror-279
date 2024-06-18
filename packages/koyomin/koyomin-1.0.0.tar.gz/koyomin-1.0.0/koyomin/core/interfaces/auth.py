from abc import ABC, abstractmethod
from oauthlib.oauth2 import WebApplicationClient
from koyomin.callbacks.server import OauthServer


class IOAuthAdapter(ABC):

    oauth_client: WebApplicationClient
    oauth_server: OauthServer

    @abstractmethod
    def prepare_login_url(self) -> str:
        ...
    
    @abstractmethod
    def is_logged_in(self) -> bool:
        ...