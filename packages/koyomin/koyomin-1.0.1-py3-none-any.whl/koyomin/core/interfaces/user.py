from abc import ABC, abstractmethod

class IUser(ABC):
    @abstractmethod
    def add_access_token(self, token: str):
        ...