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
    idp_metadata_url = models.URLField(null=True, blank=True) #optional for discovery

    frontend_post_login_url = models.URLField()
    enabled = models.BooleanField(default=True)
