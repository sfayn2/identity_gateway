from pydantic import BaseModel

class Tenant(BaseModel):
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

class Claims(BaseModel):
    event_type: str
    name: str
    email: str
    sub: str
    tenant_id: str
    roles: list


class TokenSet(BaseModel):
    access_token: str
    refresh_token: str

class LoginCallbackResponse(BaseModel):
    cookie_name: str
    refresh_token: str
    frontend_post_login_url: str

class LoginResponse(BaseModel):
    authorization_url: str

class LogoutResponse(BaseModel):
    cookie_name: str
    frontend_post_logout_url: str

class RefreshTokenResponse(BaseModel):
    cookie_name: str
    refresh_token: str
    access_token: str
    sub: str
    name: str
    email: str