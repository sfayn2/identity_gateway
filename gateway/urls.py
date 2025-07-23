from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.login_callback, name="login_callback"),
    path("refresh/", views.refresh_token, name="refresh_token"),
    path("me/", views.me, name="me")
]