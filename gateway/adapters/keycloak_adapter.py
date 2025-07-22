import jwt
import requests
from jwt import PyJWKClient
from django.conf import settings
from .base import BaseOIDCAdapter, fetch_oidc_metadata
from .dtos import NormalizedClaims



class KeycloakIdPAdapter(BaseOIDCAdapter):
    
    def normalize_claims(self, claims: dict) -> dict:
        return NormalizedClaims(
            event_type="identity_gateway_service.events.UserLoggedInEvent",
            sub=claims.get("sub"),
            tenant_id=claims.get("tenant_id"),
            roles=claims.get("resource_access").get("ecommerce_app").get("roles")
        )

    def exchange_code_for_token(self, code: str) -> dict:
        metadata = fetch_oidc_metadata(self.tenant.idp_metadata_url)
        token_endpoint = metadata["token_endpoint"]
        response = requests.post(
            token_endpoint,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.tenant.redirect_uri,
                "client_id": self.tenant.client_id,
                "client_secret": self.tenant.client_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()

    def refresh_token(self, token: str) -> dict:
        metadata = fetch_oidc_metadata(self.tenant.idp_metadata_url)
        token_endpoint = metadata["token_endpoint"]
        response = requests.post(
            token_endpoint,
            data={
                "grant_type": "refresh_token",
                "refresh_token": token,
                "client_id": self.tenant.client_id,
                "client_secret": self.tenant.client_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()


