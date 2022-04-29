import os
from glob import glob

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client

all_fixtures_glob = os.path.join(settings.BASE_DIR, "choralcat", "web", "fixtures", "[!User]*")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "User.json")


@pytest.fixture
@pytest.mark.django_db
def all_fixtures():
    for fixture_name in glob(all_fixtures_glob):
        call_command("loaddata", os.path.basename(fixture_name))


@pytest.fixture
@pytest.mark.django_db
def user() -> User:
    return User.objects.get(username="test_user")


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
