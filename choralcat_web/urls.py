from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.shortcuts import redirect, reverse

from .forms import CustomLoginForm
from .views import index_view, catalog_view, program_list_view, person_list_view

urlpatterns = [
    path("", index_view, name="home"),
    path("catalog/", catalog_view, name="catalog"),
    path("programs/", program_list_view, name="programs"),
    path("persons/", person_list_view, name="persons"),
    path(
        "login/",
        LoginView.as_view(authentication_form=CustomLoginForm),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
