import jwt
from django.conf import settings
from .keycloak_adapter import KeycloakIdPAdapter
from .auth0_adapter import Auth0IdPAdapter

def resolve_idp_adapter(tenant):
    match tenant.idp_provider.lower():
        case "keycloak": return KeycloakIdPAdapter(tenant)
        case "auth0": return Auth0IdPAdapter(tenant)
        case _: raise ValueError(f"Unsupported IDP provider {tenant.idp_provider}")

