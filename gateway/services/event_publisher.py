import json
import redis
from django.conf import settings


redis_client = redis.Redis.from_url(settings.REDIS_URL)

def publish_user_logged_in_event(claims: dict):
    redis_client.xadd("stream.identity_gateway_service", claims)