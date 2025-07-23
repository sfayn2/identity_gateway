import requests
from abc import ABC, abstractmethod
from ..models import TenantConfig
import jwt
from jwt import PyJWKClient

def fetch_oidc_metadata(metadata_url: str) -> dict:
    response = requests.get(metadata_url)
    response.raise_for_status()

    return response.json()

class BaseOIDCAdapter(ABC):

    def __init__(self, tenant):
        self.tenant = tenant

    def get_authorization_url(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def decode_token(self, token: str) -> None:
        #metadata = fetch_oidc_metadata(self.tenant.idp_metadata_url)
        #jwks_uri = metadata["jwks_uri"]
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