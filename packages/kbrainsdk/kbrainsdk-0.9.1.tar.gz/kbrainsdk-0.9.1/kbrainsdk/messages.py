from typing import Any
from kbrainsdk.validation.messages import validate_create_subscription, validate_servicebus_message, validate_servicebus_queue, validate_servicebus_topic
from kbrainsdk.apibase import APIBase

class Messages(APIBase):

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        return super().__init__(*args, **kwds)
    
    def publish_message(self, message: str, topic_name: str, application_properties: dict | None = None) -> None:
        validate_servicebus_message(message)
        validate_servicebus_topic(topic_name)
        self._publish_message(message, topic_name, application_properties)

    def create_topic(self, topic_name: str) -> None:
        validate_servicebus_topic(topic_name)
        self._create_topic(topic_name)

    def create_queue(self, queue_name: str) -> None:
        validate_servicebus_queue(queue_name)
        self._create_queue(queue_name)

    def create_subscription(self, topic_name: str, subscription_name: str) -> None:
        validate_create_subscription(topic_name, subscription_name)
        self._create_subscription(topic_name, subscription_name)

    

