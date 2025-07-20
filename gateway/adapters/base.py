from abc import ABC, abstractmethod
from ..models import TenantConfig

class BaseOIDCAdapter(ABC):

    def __init__(self, tenant):
        self.tenant = tenant

    def decode_token(token: str) -> None:
        metadata = fetch_oidc_metadata(self.tenant.idp_metadata_url)
        jwks_uri = metdata["jwks_uri"]
        jwk_client = PyJWKClient(jwks_uri)
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