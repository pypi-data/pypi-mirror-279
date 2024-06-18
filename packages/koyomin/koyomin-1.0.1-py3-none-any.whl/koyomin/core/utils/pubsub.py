from enum import Enum
from typing import Any

from koyomin.core.interfaces.subscriber import ISubscriber


class Event(Enum):
    LOGIN_SUCCESSFULL = 'oauth.success'
    TOKEN_RETRIEVED = 'oauth.token'

class PubSub:
    __TOPIC: dict[Event, list[ISubscriber]] = {}

    @staticmethod
    def publish(event: Event, 
                data: Any) -> bool:
        try:
            if topic := PubSub.__TOPIC.get(event):
                for subscriber in topic:
                    subscriber.do(data)
                return True
            return False
        except Exception as err:
            print(err)
            return False
    
    @staticmethod
    def subscribe(event: Event, 
                  subscriber: ISubscriber):
        if PubSub.__TOPIC.get(event):
            PubSub.__TOPIC[event].append(subscriber)
        else:
            PubSub.__TOPIC[event] = [subscriber]

    @staticmethod
    def unsubscribe(event: Event, 
                    subscriber: ISubscriber):
        if topic := PubSub.__TOPIC.get(event):
            topic.remove(subscriber)