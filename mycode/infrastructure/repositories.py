import json
from mycode.domain import models, repositories
from gateway import models as django_models

class DjangoTenantRepository(repositories.TenantRepositoryAbstract):
    def get_tenant(self, tenant_id: str) -> models.Tenant:
        config = TenantConfig.objects.get(tenant_id=tenant_id, enabled=True)
        return models.Tenant(
            tenant_id=config.tenant_id,
            idp_provider=config.idp_provider,
            client_id=config.client_id,
            client_secret=config.client_secret,
            issuer=config.issuer,
            audience=config.audience,
            redirect_uri=config.redirect_uri,
            idp_token_endpoint_url=config.idp_token_endpoint_url,
            idp_jwks_uri=config.idp_jwks_uri,
            idp_authorization_url=config.idp_authorization_url,
            idp_logout_url=config.idp_logout_url,
            frontend_post_login_url=config.frontend_post_login_url,
            frontend_post_logout_url=config.frontend_post_logout_url,
            enabled=config.enabled,
            allowed_email_domains=json.loads(config.allowed_email_domains)
        )