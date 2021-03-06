from django.urls import path

from .forms import CustomLoginForm
from .views import (
    CatalogView,
    ChoralcatLoginView,
    ChoralcatLogoutView,
    CompositionCreateView,
    CompositionDetailView,
    CompositionUpdateView,
    PersonCreateView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
    ProgramCreateView,
    ProgramDetailView,
    ProgramListView,
    ProgramUpdateView,
    catalog_modal,
    catalog_score_remove,
    catalog_score_retrieve,
    catalog_score_upload,
    catalog_search,
    category_add,
    index_view,
    instrument_add,
    program_add,
    program_download,
    program_remove,
    program_reorder,
    tag_add,
    topic_add,
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
    path("catalog/<str:slug>/upload/score", catalog_score_upload, name="catalog_score_upload"),
    path("catalog/<str:slug>/score/retrieve", catalog_score_retrieve, name="catalog_score_retrieve"),
    path("catalog/<str:slug>/score/<str:name>", catalog_score_remove, name="catalog_score_remove"),
    path("programs/", ProgramListView.as_view(), name="programs"),
    path("programs/new/", ProgramCreateView.as_view(), name="program_new"),
    path("programs/<str:slug>/", ProgramDetailView.as_view(), name="program_detail"),
    path("programs/<str:slug>/edit/", ProgramUpdateView.as_view(), name="program_edit"),
    path("programs/<str:slug>/add/", program_add, name="program_add"),
    path("programs/<str:slug>/remove/", program_remove, name="program_remove"),
    path("programs/<str:slug>/reorder/", program_reorder, name="program_reorder"),
    path("programs/<str:slug>/download/", program_download, name="program_download"),
    path("people/", PersonListView.as_view(), name="persons"),
    path("people/new/", PersonCreateView.as_view(), name="person_new"),
    path("people/<str:slug>/", PersonDetailView.as_view(), name="person_detail"),
    path("people/<str:slug>/edit/", PersonUpdateView.as_view(), name="person_edit"),
    path("search/catalog/", catalog_search, name="catalog_search"),
    path("categories/", category_add, name="category_add"),
    path("instruments/", instrument_add, name="instrument_add"),
    path("topics/", topic_add, name="topic_add"),
    path("tags/", tag_add, name="tag_add"),
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
