from django.urls import path

from .forms import CustomLoginForm
from .views import (
    index_view,
    ChoralcatLoginView,
    ChoralcatLogoutView,
    CatalogView,
    catalog_search,
    catalog_modal,
    CompositionDetailView,
    CompositionCreateView,
    CompositionUpdateView,
    ProgramListView,
    ProgramDetailView,
    ProgramCreateView,
    ProgramUpdateView,
    program_add,
    program_remove,
    program_reorder,
    PersonListView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView,
)

urlpatterns = [
    path("", index_view, name="home"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog/new/", CompositionCreateView.as_view(), name="composition_new"),
    path(
        "catalog/<str:slug>/",
        CompositionDetailView.as_view(),
        name="composition_detail",
    ),
    path(
        "catalog/<str:slug>/edit/",
        CompositionUpdateView.as_view(),
        name="composition_edit",
    ),
    path("catalog/<str:slug>/programs/", catalog_modal, name="catalog_modal"),
    path("programs/", ProgramListView.as_view(), name="programs"),
    path("programs/new/", ProgramCreateView.as_view(), name="program_new"),
    path("programs/<str:slug>/", ProgramDetailView.as_view(), name="program_detail"),
    path("programs/<str:slug>/edit/", ProgramUpdateView.as_view(), name="program_edit"),
    path("programs/<str:slug>/add/", program_add, name="program_add"),
    path("programs/<str:slug>/remove/", program_remove, name="program_remove"),
    path("programs/<str:slug>/reorder/", program_reorder, name="program_reorder"),
    path("people/", PersonListView.as_view(), name="persons"),
    path("people/new/", PersonCreateView.as_view(), name="person_new"),
    path("people/<str:slug>/", PersonDetailView.as_view(), name="person_detail"),
    path("people/<str:slug>/edit/", PersonUpdateView.as_view(), name="person_edit"),
    path("search/catalog/", catalog_search, name="catalog_search"),
    # ==========
    # Auth
    # ==========
    path(
        "login/",
        ChoralcatLoginView.as_view(authentication_form=CustomLoginForm),
        name="login",
    ),
    path("logout/", ChoralcatLogoutView.as_view(), name="logout"),
]
