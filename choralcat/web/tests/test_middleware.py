import pytest
from assertpy import assert_that
from django.contrib.auth.models import User

from ..middleware import OrganizationMiddleware
from ..models import Organization, UserProfile
from ..types import CCHttpRequest


@pytest.fixture
def org() -> Organization:
    return Organization(name="Chanticleer")


@pytest.fixture
def profile(org: Organization) -> UserProfile:
    return UserProfile(organization=org)


@pytest.fixture
def user(profile: UserProfile) -> User:
    return User(username="test_user", profile=profile)


def test_organization_middleware(user: User, org: Organization, mocker) -> None:
    get_response = mocker.Mock()
    get_response.side_effect = lambda r: r
    request = CCHttpRequest()
    request.user = user
    middleware = OrganizationMiddleware(get_response)
    response = middleware(request)
    assert_that(response.org).is_equal_to(org)
