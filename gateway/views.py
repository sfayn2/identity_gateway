from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .adapters.resolver import  resolve_idp_adapter
from .services.event_publisher import publish_user_logged_in_event

# Create your views here.
def login_callback(request):
    code = request.POST.get("code")
    next_path = request.GET.get("next", "/")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    # Exchange the code for tokens
    token_response = requests.post(
        settings.IDP_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.IDP_REDIRECT_URI,
            "client_id": settings.IDP_CLIENT_ID,
            "client_secret": settings.IDP_CLIENT_SECRET
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if token_response.status_code != 200:
        return JsonResponse({"error": "Token exchange failed"}, status=401)

    token_data = token_response.json()
    #id_token = token_data.get("id_token")
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    token_type = token_data.get("token_type", "Bearer")

    if not access_token:
        return JsonResponse({"error": "Missing Access Token"}, status=401)

    adapter = resolve_idp_adapter(access_token)
    claims = adapter.decode_token(access_token)
    normalized = adapter.normalized_claims(claims, token_type=token_type)

    publish_user_logged_in_event(normalized)

    response = redirect(next_path)
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, 
        samesite="None", domain=settings.COOKIES_DOMAIN, path="/gateway/refresh_token", secure=True
    )

    return response

def me(request):
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    token_type = request.GET.get("token_type", "Bearer")
    if not access_token:
        return JsonResponse({"error": "Missing token"}, status=401)

    adapter = resolve_idp_adapter(access_token)
    claims = adapater.decode_token(access_token)
    normalized = adapter.normalized_claims(claims, token_type=token_type)

    return JsonResponse(normalized)

def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return JsonResponse({"error": "Missing Refresh Token"}, status=401)

    token_response = requests.post(
        settings.IDP_TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": settings.IDP_CLIENT_ID,
            "client_secret": settings.IDP_CLIENT_SECRET
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if token_response.status_code != 200:
        return JsonResponse({"error": "Token refresh failed"}, status=401)

    token_data = response.json()
    token_type = token_data.get("token_type", "Bearer")
    new_access_token = token_data.get("access_token")
    new_refresh_token = token_data.get("refresh_token")

    if not new_access_token or not new_refresh_token:
        return JsonResponse({"error": "No access/refresh token in response"}, status=401)

    adapter = resolve_idp_adapter(new_access_token)
    claims = adapater.decode_token(new_access_token)
    normalized = adapter.normalized_claims(claims, token_type=token_type)

    response = JsonResponse({
        "access_token": new_access_token,
        "token_type": token_type
        "sub": normalized.get("sub")
    })

    # Decision: frontend to request via refresh_token & let frontend have the access token in mem or localStorage via post-login?

    response.set_cookie(
        key="refresh_token", value=new_refresh_token, httponly=True, 
        samesite="None", domain=settings.COOKIES_DOMAIN, path="/gateway/refresh", secure=True
    )

    return response

