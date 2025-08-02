from __future__ import annotations
from typing import Tuple
from mycode.domain import models, exceptions, events
from mycode.application import commands, queries, dtos

def handle_login(
     cmd: commands.LoginCommand, 
     tenant_repo: repositories.TenantRepository,
     idp_service: ports.IdPPort
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
     idp_service: ports.IdPPort
) -> dtos.LogoutResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    logout_url = tenant.logout_url()
    #idp = idp_service.resolve_idp(tenant)
    return dtos.LogoutResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        frontend_post_logout_url=logout_url
    )

def _dispatch_events(tenant_agg: models.Tenant, event_bus: EventBus):
    #TODO simplify?
    for event in tenant_agg._events:
        event_bus.publish(event)
    tenant_agg.events.clear()


def handle_login_callback(
     cmd: commands.LoginCallbackCommand, 
     tenant_repo: repositories.TenantRepository,
     idp_service: ports.IdPPort,
     event_bus: EventBus
) -> dtos.LoginCallbackResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    token_data = tenant.login_callback(cmd.code, idp)

    _dispatch_events(tenant_agg=tenant, event_bus=event_bus)


    return dtos.LoginCallbackResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        refresh_token=token_data.refresh_token, 
        frontend_post_login_url=tenant.frontend_post_login_url
    )

def handle_me(
    qry: queries.MeQuery,
    tenant_repo: repositories.TenantRepository,
    idp_service: ports.IdPPort
) -> dtos.Claims:
    tenant = tenant_repo.get_tenant(qry.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    claims = tenant.me(qry.access_token)

    return claims

def handle_refresh_token(
    cmd: commands.RefreshTokenCommand, 
    tenant_repo: repositories.TenantRepository,
    idp_service: ports.IdPPort
) -> dtos.RefreshTokenResponse:
    tenant = tenant_repo.get_tenant(cmd.tenant_id)
    idp = idp_service.resolve_idp(tenant)
    normalized, token_data = tenant.refresh(cmd.refresh_token, idp)

    return dtos.RefreshTokenResponse(
        cookie_name=f"refresh_token_{cmd.tenant_id}",
        refresh_token=token_data.refresh_token,
        access_token=token_data.access_token,
        sub=normalized.sub,
        name=normalized.name,
        email=normalized.email
    )


