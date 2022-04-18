from assertpy import assert_that, soft_assertions
from django.test import TestCase

from .. import models as m
from .test_base import CCTestCase


class TestAuthViews(TestCase):
    fixtures = ["User"]

    def test_login(self):
        res = self.client.post("/login/", {"name": "test_user", "password": "testpassword"})
        assert_that(res.status_code).is_equal_to(200)

    def test_logout(self):
        self.client.post("/login/", {"name": "test_user", "password": "testpassword"})
        res = self.client.get("/logout/", follow=True)
        assert_that(res.status_code).is_equal_to(200)
        assert_that(res.redirect_chain[-1][0]).is_equal_to("/")


class TestAllGetViews(CCTestCase):
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

    def test_all_get_views_render(self):
        with soft_assertions():
            for url in self.urls:
                res = self.client.get(url)
                assert_that(res.status_code).is_equal_to(200)

    def test_views_require_authentication(self):
        self.client.logout()
        with soft_assertions():
            for url in self.urls[1:]:
                res = self.client.get(url, follow=True)
                assert_that(res.status_code).is_equal_to(200)
                assert_that(res.redirect_chain[0][1]).is_equal_to(302)
                assert_that(res.redirect_chain[-1][0]).starts_with("/login/")


class TestSimpleAddViews(CCTestCase):
    urls = [
        ("/categories/", "categories", m.Category),
        ("/instruments/", "accompaniment", m.Instrument),
        ("/topics/", "topics", m.Topic),
        ("/tags/", "tags", m.Tag),
    ]

    def test_add_new_value(self):
        with soft_assertions():
            for url, name, model in self.urls:
                assert_that(model.objects.filter(value="new_value").count()).is_equal_to(0)
                res = self.client.post(url, {f"new_{name}": "new_value"})
                assert_that(res.status_code).is_equal_to(200)
                assert_that(model.objects.filter(value="new_value").count()).is_equal_to(1)

    def test_add_current_value(self):
        with soft_assertions():
            for url, name, model in self.urls:
                model.objects.create(value="an oldie but a goodie", user=self.user)
                assert_that(model.objects.filter(value="an oldie but a goodie").count()).is_equal_to(1)
                res = self.client.post(url, {f"new_{name}": "an oldie but a goodie"})
                assert_that(res.status_code).is_equal_to(200)
                assert_that(model.objects.filter(value="an oldie but a goodie").count()).is_equal_to(1)

    def test_append_value(self):
        response = self.client.post("/tags/", {"new_tags": "to tag things", "tags": ["1", "2"]})
        assert_that(response.status_code).is_equal_to(200)
        expected = [
            {"label": "test tag", "value": 1},
            {"label": "we love", "value": 2},
            {"label": "to tag things", "value": 3},
        ]
        with soft_assertions():
            for expect, actual in zip(expected, response.context["selected"]):
                assert_that(expect).is_equal_to(actual)

    def test_remove_value(self):
        response = self.client.post("/tags/", {"remove": "test tag", "tags": ["1", "2"]})
        assert_that(response.status_code).is_equal_to(200)
        expected = [
            {"label": "we love", "value": 2},
        ]
        with soft_assertions():
            for expect, actual in zip(expected, response.context["selected"]):
                assert_that(expect).is_equal_to(actual)
