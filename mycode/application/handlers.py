from typing import Tuple
from mycode.domain import models, exceptions
from mycode.infrastructure import adapters
from mycode.infrastructure import repositories

from mycode.application import commands, queries, dtos

def handle_login(
     cmd: commands.LoginCommand, 
     tenant_repo: repositories.TenantRepository,
     idp_service: adapters.IdPAdapter
) -> dtos.LoginResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    authorization_url = tenant.authorize(idp)

    return dtos.LoginResponse(
        authorization_url=authorization_url
    )

def handle_logout(
     cmd: commands.LogoutCommand, 
     tenant_repo: repositories.TenantRepository,
     idp_service: adapters.IdPAdapter
) -> dtos.LogoutResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    logout_url = tenant.logout_url()
    #idp = idp_service.resolve_idp(tenant)
    return dtos.LogoutResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        frontend_post_logout_url=logout_url
    )


def handle_login_callback(
     cmd: commands.LoginCallbackCommand, 
     tenant_repo: repositories.TenantRepository,
     idp_service: adapters.IdPAdapter
) -> dtos.LoginCallbackResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    token_data = tenant.login_callback(cmd.code, idp)

    return dtos.LoginCallbackResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        refresh_token=token_data.refresh_token, 
        frontend_post_login_url=tenant.frontend_post_login_url
    )

def handle_me(
    qry: queries.MeQuery,
    tenant_repo: repositories.TenantRepository,
    idp_service: adapters.IdPAdapter
) -> dtos.Claims:
    tenant = tenant_repo.get_tenant(qry.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    claims = idp.decode_token(qry.access_token)

    return idp.normalize_claims(claims)

def handle_refresh_token(
    cmd: commands.RefreshTokenCommand, 
    tenant_repo: repositories.TenantRepository,
    idp_service: adapters.IdPAdapter
) -> dtos.RefreshTokenResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    normalized, token_data = tenant.refresh(cmd.refresh_token, idp)

    #token_data = idp.refresh_token(cmd.refresh_token)

    #if not token_data.access_token or not token_data.refresh_token:
    #    raise exceptions.RefreshTokenException("Missing token data")

    #claims = idp.decode_token(token_data.access_token)

    #if claims.tenant_id != cmd.tenant_id:
    #    raise exceptions.RefreshTokenException("Invalid tenant in token")

    #normalized = idp.normalize_claims(claims)

    return dtos.RefreshTokenResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        refresh_token=token_data.refresh_token,
        access_token=token_data.access_token,
        sub=normalized.sub,
        name=normalized.name,
        email=normalized.email
    )


