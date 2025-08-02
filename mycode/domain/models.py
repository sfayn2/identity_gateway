from typing import Optional, Tuple
from dataclasses import dataclass, field
from mycode.domain import exceptions

@dataclass
class Tenant:
    tenant_id: str
    idp_provider: str
    client_id: str
    _client_secret: str = field(repr=False) #make private & hide from repr
    issuer: str
    audience: str
    redirect_uri: str

    idp_token_endpoint_url: str
    idp_jwks_uri: str
    idp_authorization_url: str
    idp_logout_url: str

    frontend_post_login_url: str
    frontend_post_logout_url: Optional[str] = "/"

    enabled: bool
    allowed_email_domains: Optional[List[str]] = field(default_factory=list)

    @property
    def client_secret(self):
        raise exceptions.TenantException("Direct access to client secret is not allowed, Use secure accessors.")

    def get_client_secret(self) -> str:
        return self._client_secret

    def masked_client_secret(self) -> str:
        secret = self._client_secret
        if not secret:
            return "[None]"
            return f"{secret[:4]}...{secret[-4:]}"

    def authorize(self, idp: IdPPort) -> str:
        self._ensure_active()
        return idp.get_authorization_url()

    def logout_url(self) -> str:
        self._ensure_active()
        return self.frontend_post_logout_url

    def login_callback(self, code: str, idp: IdPPort) -> TokenSet:
        self._ensure_active()
        token_data = idp.exchange_code_for_token(code)
        claims = idp.decode_token(token_data.access_token)

        self._validate_claims(claims)

        return token_data

    def refresh(self, refresh_token: str, idp: IdPPort) -> Tuple[TokenSet, Claims]:
        self._ensure_active()
        token_data = idp.refresh_token(refresh_token)

        if not token_data.access_token or not token_data.refresh_token:
            raise exceptions.RefreshTokenException("Missing token data")

        claims = idp.decode_token(token_data.access_token)
        normalized = idp.normalize_claims(claims)

        self._validate_claims(normalized)

        return token_data, normalized

    def _ensure_active(self) -> bool:
        if not self.enabled:
            raise TenantException(f"Tenant {self.tenant_id} is disabled.")

    def _validate_claims(self, claims: Claims):
        if claims.tenant_id != self.tenant_id:
            raise TenantException(f"[SECURITY] Token claims belong to tenant {claims.tenant_id}, expected {self.tenant_id}")

        if not claims.email or "@" not in claims.email:
            raise TenantException("Invalid email address in token claims.")

        if self.allowed_email_domains and not self._email_in_allowed_domains(claims.email):
            raise TenantException(f"Email domain not allowed {claims.email}")

    def _email_in_allowed_domains(self, email: str) -> bool:
        domain = email.split("@")[-1].lower()
        return any(domain == allowed.lower() for allowed in self.allowed_email_domains)



