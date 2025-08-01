from typing import Optional
from dataclasses import dataclass

@dataclass
class Tenant:
    tenant_id: str
    idp_provider: str
    client_id: str
    client_secret: str
    issuer: str
    audience: str
    redirect_uri: str

    idp_token_endpoint_url: str
    idp_jwks_uri: str
    idp_authorization_url: str
    idp_logout_url: str

    frontend_post_login_url: str
    frontend_post_logout_url: str

    enabled: bool
