from dataclasses import dataclass
import os
import requests


@dataclass
class AuthConfig:
  authorization_endpoint: str
  token_endpoint: str
  revoke_endpoint: str
  certs: str

def get_config() -> AuthConfig:
    config = requests.get(f"{os.getenv('CONFIG_ENDPOINT', 'https://auth.shogun.minorin.io')}/oauth/config")
    data = config.json()
    return AuthConfig(authorization_endpoint=data.get('authorization_endpoint'),
                      token_endpoint=data.get('token_endpoint'),
                      revoke_endpoint=data.get('revoke_endpoint'),
                      certs=data.get('certs'))

config = get_config()