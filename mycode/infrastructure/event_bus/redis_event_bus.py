import json
import redis


class RedisEventBus(EventBus):
    def __init__(self, redis_client: redis.Redis, stream_name: str = "stream.identity_gateway_service"):
        self.redis = redis_client
        self.stream_name = stream_name

    def publish(self, event: events.DomainEvent) -> None:
        self.redis.xadd(self.stream_name, event)