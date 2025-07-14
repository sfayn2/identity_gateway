import jwt
from jwt import PyJWKClient
from django.conf import settings
from .base import IdPAdapter


class KeycloakIdPAdapter(IdPAdapter):
    def __init__(self, issuer: str, audience: str = None):
        self.issuer = issuer
        self.audience = audience

        self.jwks_url = settings.IDP_CERTS
        self.jwks_client = PyJWKClient(self.jwks_url)

    def decode_token(self, token: str) -> str:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=self.issuer,
            audience=self.audience
        )
        return decoded

    def normalize_claims(self, claims: dict, token_type: str) -> dict:
        return {
            "event_type":  "identity_gateway_service.events.UserLoggedInEvent",
            "sub": claims.get("sub"),
            "token_type": claims.get("token_type"),
            "tenant_id": claims.get("tenant_id"),
            "roles": claims.get("realm_access", {}).get("roles", [])
        }
