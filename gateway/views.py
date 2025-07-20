import jwt
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .adapters.resolver import  resolve_idp_adapter
#from .services.event_publisher import publish_user_logged_in_event

# Create your views here.
def login_callback(request):
    tenant_id = request.POST.get("tenant_id")
    if not tenant_id:
        return JsonResponse({"error": "Missing tenant id."}, status=400)

    try:
        tenant = TenantConfig.objects.get(tenant_id=tenant_id, enabled=True)
    except TenantConfig.DoesNotExist:
        return JsonResponse({"error": "Unknown tenant"}, status=400)

    code = request.POST.get("code")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    adapter =  revolve_idp_adapter(tenant)

    token_data = adapter.exchange_code_for_token(code=code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    if not access_token:
        return JsonResponse({"error": "Missing Access Token"}, status=401)

    claims = adapter.decode_token(access_token)
    normalized = adapter.normalized_claims(claims)

    publish_user_logged_in_event(normalized)

    response = redirect(tenant.frontend_post_login_url)
    response.set_cookie(
        key=f"refresh_token_{tenant_id}", value=refresh_token, httponly=True, 
        samesite="None", domain=settings.COOKIES_DOMAIN, path=settings.COOKIES_PATH, secure=True
    )

    return response

def me(request):
    tenant_id = request.POST.get("tenant_id")
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not access_token:
        return JsonResponse({"error": "Missing token"}, status=400)

    try:
        tenant = TenantConfig.objects.get(tenant_id=tenant_id, enabled=True)
    except TenantConfig.DoesNotExist:
        return JsonResponse({"error": "Unknown tenant"}, status=400)

    adapter = resolve_idp_adapter(tenant)
    claims = adapter.decode_token(access_token)
    normalized = adapter.normalized_claims(claims)

    return JsonResponse(normalized)

def refresh_token(request):
    tenant_id = request.POST.get("tenant_id")
    if not tenant_id:
        return JsonResponse({"error": "Missing tenant id."}, status=400)

    refresh_token = request.COOKIES.get(f"refresh_token_{tenant_id}")
    if not refresh_token:
        return JsonResponse({"error": "Missing Refresh Token"}, status=400)

    try:
        tenant = TenantConfig.objects.get(tenant_id=tenant_id, enabled=True)
    except TenantConfig.DoesNotExist:
        return JsonResponse({"error": "Unknown tenant"}, status=400)

    adapter =  revolve_idp_adapter(tenant)

    token_data = adapter.refresh_token(token=refresh_token)
    new_access_token = token_data.get("access_token")
    new_refresh_token = token_data.get("refresh_token")

    if not new_access_token or not new_refresh_token:
        return JsonResponse({"error": "No access/refresh token in response"}, status=40)

    claims = adapter.decode_token(new_access_token)
    normalized = adapter.normalized_claims(claims)

    response = JsonResponse({
        "access_token": new_access_token,
        "sub": normalized.get("sub")
    })

    # Decision: frontend to request via refresh_token & let frontend have the access token in mem or localStorage via post-login?

    response.set_cookie(
        key=f"refresh_token_{tenant_id}", value=refresh_token, httponly=True, 
        samesite="None", domain=settings.COOKIES_DOMAIN, path=settings.COOKIES_PATH, secure=True
    )

    return response

