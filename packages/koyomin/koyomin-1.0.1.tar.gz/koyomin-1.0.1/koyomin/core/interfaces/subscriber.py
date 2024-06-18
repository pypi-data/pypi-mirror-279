from typing import Generic, TypeVar


T = TypeVar('T')

class ISubscriber(Generic[T]):
    def do(self, data: T):
        raise NotImplementedError