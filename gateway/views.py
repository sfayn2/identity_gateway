from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .adapters.resolver import  resolve_idp_adapter
from .services.event_publisher import publish_user_logged_in_event

# Create your views here.
@csrf_exempt
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
    token_type = token_data.get("token_type")

    if not access_token:
        return JsonResponse({"error": "Missing Access Token"}, status=401)

    adapter = resolved_idp_adapter(refresh_token)
    claims = adapter.decode_token(refresh_token)
    normalized = adapter.normalized_claims(claims, token_type=token_type)

    publish_user_logged_in_event(normalized)

    response = HttpResponseRedirect(next_path)
    response.set_cookie(
            key="access_token", value=result.access_token, httponly=True, 
            samesite="Lax", domain=".mystore.com", path="/", secure=True
        )
    response.set_cookie(
        key="refresh_token", value=result.refresh_token, httponly=True, 
        samesite="Strict", domain=".mystore.com", path="/gateway/refresh_token", secure=True
    )

    return response

def me(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return JsonResponse({"error": "Missing token"}, status=400)

    adapter = resolved_idp_adapter(token)
    claims = adapater.decode_token(token)
    normalized = adapter.normalized_claims(claims, token_type="Bearer")

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
    new_access_token = token_data.get("access_token")

    if not new_access_token:
        return JsonResponse({"error": "No access token in response"}, status=401)

    response = JsonResponse({"success": True })
    response.set_cookie(
            key="access_token", value=new_access_token, httponly=True, 
            samesite="Lax", domain=".mystore.com", path="/", secure=True
        )

    return response

