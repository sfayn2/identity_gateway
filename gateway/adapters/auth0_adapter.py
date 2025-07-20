import jwt
from .base import BaseOIDCAdapter

class Auth0IdPAdapter(BaseOIDCAdapter):

    def decode_token(self, token: str) -> str:
        return jwt.decode(token, options={"verify_signature": False, algorithms:["RS256"]})

    def normalize_claims(self, claims: dict, token_type: str) -> dict:
        return {
            "event_type":  "identity_gateway_service.events.UserLoggedInEvent",
            "sub": claims.get("sub"),
            "tenant_id": claims.get("https://store.com/tenant_id"),
            "roles": claims.get("roles", [])
        }
