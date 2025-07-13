from __future__ import annotations
import json
import redis

redis_client = redis.Redis.from_url('redis://localhost:6379')


event = {
    "event_type": "identity_gateway_service.events.UserLoggedInEvent",
    "sub": "abc123",
    "token_type": "Bearer",
    "tenant_id": "t-123",
    "roles": json.dumps(["customer"])
}

redis_client.xadd("stream.identity_gateway_service", event)