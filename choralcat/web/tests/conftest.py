import os

import pytest
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client

from choralcat.web.models import Composition, Organization, Person, Program, Tag

all_fixtures_glob = os.path.join(settings.BASE_DIR, "choralcat", "web", "fixtures", "[!User]*")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Organization.objects.create(name="Chanticleer")
        User.objects.create(username="test_user", password=make_password("testpassword"), id=1)


@pytest.fixture
@pytest.mark.django_db
def all_fixtures(org: Organization) -> None:
    Composition.objects.create(slug="fratres-ego-enim-accepi-RKAQ", organization=org)
    Program.objects.create(slug="live-from-london-S4xg", organization=org)
    Person.objects.create(slug="rachmaninoff-cXpe", organization=org)
    Tag.objects.create(pk=1, value="test tag", organization=org)
    Tag.objects.create(pk=2, value="we love", organization=org)


@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    return User.objects.get(username="test_user")


@pytest.fixture
@pytest.mark.django_db
def org() -> Organization:
    return Organization.objects.get(name="Chanticleer")


@pytest.fixture
@pytest.mark.django_db
def logged_in_client(client: Client) -> Client:
    client.login(username="test_user", password="testpassword")
    return client


@pytest.fixture
@pytest.mark.django_db
def logged_out_client(client: Client) -> Client:
    client.logout()
    return client
