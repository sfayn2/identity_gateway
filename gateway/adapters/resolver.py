import jwt
from django.conf import settings
from .keycloak_adapter import KeycloakIdPAdapter
from .auth0_adapter import Auth0IdpAdapter

def resolve_idp_adapter(token: str):
    unverified = jwt.decode(token, options={"verify_signature": False})
    issuer = unverified.get("iss", "")

    #provider_info = settings.IDP_PROVIDERS.get(issuer)
    #if not provider_info:
    #    raise ValueError(f"Unsupported issuer: {issuer}")

    #idp_type = provider_info["type"]
    #audience = provider_info["audience"]

    if settings.ACTIVE_IDP == "keycloak"
        return Auth0IdPAdapter(
            issuer, settings.IDP_AUD
        )
    elif settings.ACTIVE_IDP == "auth0"
        return KeycloakIdPAdapter(
            issuer, settings.IDP_AUD
        )
    else:
        raise ValueError(f"Unsupported IDP Type: {idp_type}")