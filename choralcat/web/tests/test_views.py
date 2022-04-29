import pytest
from assertpy import assert_that, soft_assertions
from django.contrib.auth.models import User
from django.test import Client

from .. import models as m


@pytest.mark.django_db
def test_logout(client: Client) -> None:
    client.post("/login/", {"name": "test_user", "password": "testpassword"})
    res = client.get("/logout/", follow=True)
    assert_that(res.status_code).is_equal_to(200)
    assert_that(res.redirect_chain[-1][0]).is_equal_to("/")


urls = [
    "/",
    "/catalog/",
    "/catalog/new/",
    "/catalog/fratres-ego-enim-accepi-RKAQ/",
    "/catalog/fratres-ego-enim-accepi-RKAQ/edit/",
    "/catalog/fratres-ego-enim-accepi-RKAQ/programs/",
    "/programs/",
    "/programs/new/",
    "/programs/live-from-london-S4xg/",
    "/programs/live-from-london-S4xg/edit/",
    "/people/",
    "/people/new/",
    "/people/rachmaninoff-cXpe/",
    "/people/rachmaninoff-cXpe/edit/",
]


@pytest.mark.django_db
def test_all_get_views_render(all_fixtures, logged_in_client: Client):
    with soft_assertions():
        for url in urls:
            res = logged_in_client.get(url)
            assert_that(res.status_code).is_equal_to(200)


@pytest.mark.django_db
def test_views_require_authentication(client: Client):
    with soft_assertions():
        for url in urls[1:]:
            res = client.get(url, follow=True)
            assert_that(res.status_code).is_equal_to(200)
            assert_that(res.redirect_chain[0][1]).is_equal_to(302)
            assert_that(res.redirect_chain[-1][0]).starts_with("/login/")


simple_add_urls = [
    ("/categories/", "categories", m.Category),
    ("/instruments/", "accompaniment", m.Instrument),
    ("/topics/", "topics", m.Topic),
    ("/tags/", "tags", m.Tag),
]


@pytest.mark.django_db
@soft_assertions()
def test_add_new_value(logged_in_client: Client) -> None:
    for url, name, model in simple_add_urls:
        assert_that(model.objects.filter(value="new_value").count()).is_equal_to(0)
        res = logged_in_client.post(url, {f"new_{name}": "new_value"})
        assert_that(res.status_code).is_equal_to(200)
        assert_that(model.objects.filter(value="new_value").count()).is_equal_to(1)


@pytest.mark.django_db
@soft_assertions()
def test_add_current_value(logged_in_client: Client, user: User) -> None:
    for url, name, model in simple_add_urls:
        model.objects.create(value="an oldie but a goodie", user=user)
        assert_that(model.objects.filter(value="an oldie but a goodie").count()).is_equal_to(1)
        res = logged_in_client.post(url, {f"new_{name}": "an oldie but a goodie"})
        assert_that(res.status_code).is_equal_to(200)
        assert_that(model.objects.filter(value="an oldie but a goodie").count()).is_equal_to(1)


@pytest.mark.django_db
def test_append_value(all_fixtures, logged_in_client: Client) -> None:
    response = logged_in_client.post("/tags/", {"new_tags": "to tag things", "tags": ["1", "2"]})
    assert_that(response.status_code).is_equal_to(200)
    expected = [
        {"label": "test tag", "value": 1},
        {"label": "we love", "value": 2},
        {"label": "to tag things", "value": 3},
    ]
    with soft_assertions():
        for expect, actual in zip(expected, response.context["selected"]):
            assert_that(expect).is_equal_to(actual)


@pytest.mark.django_db
def test_remove_value(all_fixtures, logged_in_client: Client) -> None:
    response = logged_in_client.post("/tags/", {"remove": "test tag", "tags": ["1", "2"]})
    assert_that(response.status_code).is_equal_to(200)
    expected = [
        {"label": "we love", "value": 2},
    ]
    with soft_assertions():
        for expect, actual in zip(expected, response.context["selected"]):
            assert_that(expect).is_equal_to(actual)
