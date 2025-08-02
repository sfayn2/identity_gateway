from django.db import models

# Create your models here.
class TenantConfig(models.Model):
    tenant_id = models.CharField(max_length=100, unique=True)
    idp_provider = models.CharField(max_length=64)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    issuer = models.CharField(max_length=100)
    audience = models.CharField(max_length=100)
    redirect_uri = models.URLField()

    #idp_metadata_url = models.URLField(null=True, blank=True) #optional for discovery
    idp_token_endpoint_url = models.URLField(null=True, blank=True) 
    idp_jwks_uri = models.URLField(null=True, blank=True) 
    idp_authorization_url = models.URLField(null=True, blank=True) 
    idp_logout_url = models.URLField(null=True, blank=True) 

    frontend_post_login_url = models.URLField()
    frontend_post_logout_url = models.URLField()

    allowed_email_domains = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tenant_id} | {self.idp_provider} ({self.client_id}) | {self.frontend_post_login_url}"
