import requests
from abc import ABC, abstractmethod
import jwt
from jwt import PyJWKClient


class IdPAbstract(ABC):

    def __init__(self, tenant):
        self.tenant = tenant

    @abstractmethod
    def get_authorization_url(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def decode_token(self, token: str) -> None:
        jwk_client = PyJWKClient(self.tenant.idp_jwks_uri)
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=self.tenant.issuer,
            audience=self.tenant.audience
        )

        return decoded


    @abstractmethod
    def normalize_claims(self, claims: dict):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def exchange_code_for_token(self,  code: str):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def refresh_token(token: str) -> None:
        raise NotImplementedError("Subclasses must implement this method")

        