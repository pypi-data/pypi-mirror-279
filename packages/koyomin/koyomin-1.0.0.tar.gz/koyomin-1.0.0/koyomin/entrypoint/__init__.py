from enum import Enum
import time
from oauthlib.oauth2 import WebApplicationClient
import requests
import uvicorn

from koyomin.callbacks.server import OauthServer
from koyomin.core.interfaces.subscriber import ISubscriber
from koyomin.core.utils.get_oauth_config import AuthConfig, config
from koyomin.entities.user import user, User
from koyomin.callbacks.server import server

class SupportedMethods(Enum):
    S256 = "S256"

class ILogonSubscriber(ISubscriber):
    code: str

class Koyomin:
    def __init__(self,
                 client_id: str = "default",
                 code_challenge_method: SupportedMethods = SupportedMethods.S256,
                 config: AuthConfig = config,
                 user: User = user) -> None:
        self.user: User = user
        self.__client = WebApplicationClient(client_id=client_id)
        self.__server = OauthServer(config=uvicorn.Config(server, port=9712, log_level="critical"))
        self.__config = config
        
        if not isinstance(code_challenge_method, SupportedMethods):
            raise Exception("Code challenge method must be of type SupportedMethods.")
        
        self.__client.code_challenge_method = code_challenge_method.value

    def __enter__(self):
        self.__server.run_in_thread()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__server.shutdown_server_in_thread()

    def start_server(self) -> None:
        self.__server.run_in_thread()

    def stop_server(self) -> None:
        self.__server.shutdown_server_in_thread()

    def __create_code_challenge(self, code_verifier: str) -> str:
        return self.__client.create_code_challenge(code_verifier=code_verifier,
                                                   code_challenge_method=self.__client.code_challenge_method)
    
    def __create_code_verifier(self, length: int) -> str:
        return self.__client.create_code_verifier(length=length)
    
    def set_client_id(self, client_id: str) -> None:
        self.__client.client_id = client_id
    
    def set_code_challenge_method(self, 
                                  code_challenge_method: SupportedMethods) -> None:
        if not isinstance(code_challenge_method, SupportedMethods):
            raise Exception("Code challenge method must be of type SupportedMethods.")
        self.__client.code_challenge_method = code_challenge_method.value

    def prepare_login_url(self, scopes: list[str]) -> str:
        self.__client.code_verifier = self.__create_code_verifier(48)
        self.__client.code_challenge = self.__create_code_challenge(code_verifier=self.__client.code_verifier)
        return self.__client.prepare_authorization_request(authorization_url=self.__config.authorization_endpoint,
                                                           callback_uri="http://localhost:9712/oauth/callback",
                                                           callback_redirect="false",
                                                           code_challenge=self.__client.code_challenge,
                                                           code_challenge_method=self.__client.code_challenge_method,
                                                           scope=scopes)[0]
    
    def fetch_token(self):
        uri, headers, params = self.__client.prepare_token_request(token_url=self.__config.token_endpoint,
                                                                   code_verifier=self.__client.code_verifier,
                                                                   code=self.user.code)
        
        response = requests.get(url=f'{uri}?{params}')
        
        if response.status_code != 200:
            return False
        
        data = response.json()
        
        self.user.add_access_token(token=data.get("access_token"))
        self.user.add_refresh_token(refresh_token=data.get("refresh_token"))

        return True

    def wait_for_logon(self):
        print('Waiting for successfull login...')
        print('Press CTRL + C to cancel.')
        try:
            while not self.user.is_logged_in:
                time.sleep(1.5)
                
                if self.user.code is None:
                    continue
                
                logged = self.fetch_token()
                
                if logged:
                    print("Logged Successfully!")
                    break
        except KeyboardInterrupt:
            print("Login cancelled.")
