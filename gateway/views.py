import jwt, json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
#from .services.event_publisher import publish_user_logged_in_event

from mycode.infrastructure import repositories, idp_services
from mycode.application import handlers, commands, queries


# Create your views here.
def login_view(request):
    try:
        tenant_id = request.GET.get("state")
        result = handlers.handle_login(
            cmd=commands.LoginCommand(tenant_id=tenant_id),
            tenant_repo=repositories.DjangoTenantRepository(),
            idp_service=idp_services
        )
        return redirect(result.login_url)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def logout_view(request):
    try:
        tenant_id = request.GET.get("state")
        result = handlers.handle_logout(
            cmd=commands.LogoutCommand(tenant_id=tenant_id),
            tenant_repo=repositories.DjangoTenantRepository(),
            idp_service=idp_services
        )

        response = redirect(result.frontend_post_logout_url)

        response.delete_cookie(
            key=result.cookie_name,
            domain=settings.COOKIES_DOMAIN,
            path=settings.COOKIES_PATH,
            samesite=None
        )

        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def login_callback_view(request):
    try:
        tenant_id = request.GET.get("state")
        code = request.GET.get("code")
        result = handlers.handle_login_callback(
            cmd=commands.LoginCallbackCommand(tenant_id=tenant_id, code=code),
            tenant_repo=repositories.DjangoTenantRepository(),
            idp_service=idp_services
        )
        response = redirect(result.frontend_post_login_url)
        response.set_cookie(
            key=result.cookie_name, value=result.refresh_token, httponly=True, 
            samesite=None, domain=settings.COOKIES_DOMAIN, path=settings.COOKIES_PATH, secure=True
        )

        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def me_view(request):
    try:
        tenant_id = request.GET.get("tenant_id")
        access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        result = handlers.handle_me(
            qry=queries.MeQuery(tenant_id=tenant_id, access_token=access_token),
            tenant_repo=repositories.DjangoTenantRepository(),
            idp_service=idp_services
        )
        return JsonResponse(result.__dict__)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def refresh_token_view(request):
    try:
        tenant_id = request.POST.get("tenant_id")
        refresh_token = request.COOKIES.get(f"refresh_token_{tenant_id}")
        result = handlers.handle_refresh_token(
            cmd=commands.RefreshTokenCommand(tenant_id=tenant_id, refresh_token=refresh_token),
            tenant_repo=repositories.DjangoTenantRepository(),
            idp_service=idp_services
        )

        response = JsonResponse({
            "access_token":result.access_token,
            "sub": result.sub,
            "name":result.name,
            "email":result.email
        })

        # Decision: frontend to request via refresh_token & let frontend have the access token in mem or localStorage via post-login?

        response.set_cookie(
            key=result.cookie_name, value=result.refresh_token, httponly=True, 
            samesite=None, domain=settings.COOKIES_DOMAIN, path=settings.COOKIES_PATH, secure=True
        )

        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

