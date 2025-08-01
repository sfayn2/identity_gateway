from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("callback/", views.login_callback_view, name="login_callback"),
    path("refresh/", views.refresh_token_view, name="refresh_token"),
    path("me/", views.me_view, name="me")
]