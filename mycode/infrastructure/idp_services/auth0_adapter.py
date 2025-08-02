import jwt
from mycode.application import ports, dtos

class Auth0IdPAdapter(ports.IdPPort):

    def decode_token(self, token: str) -> str:
        return jwt.decode(token, options={"verify_signature": False, algorithms:["RS256"]})

    def normalize_claims(self, claims: dict, token_type: str) -> dict:
        return {
            "event_type":  "identity_gateway_service.events.UserLoggedInEvent",
            "sub": claims.get("sub"),
            "tenant_id": claims.get("https://store.com/tenant_id"),
            "roles": claims.get("roles", [])
        }
