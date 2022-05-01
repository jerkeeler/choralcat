import pytest
from assertpy import assert_that
from django.http import Http404

from ..models import Organization, Person
from ..query import get_object_or_404, org_filter
from ..types import CCHttpRequest

names = [
    "Jeremy",
    "Tim",
]


@pytest.fixture
def org_models(org: Organization) -> list[Person]:
    return [Person.objects.create(first_name=f"{name}-org", organization=org) for name in names]


@pytest.fixture
def non_org_models() -> list[Person]:
    return [Person.objects.create(first_name=f"{name}-not-org") for name in names]


@pytest.mark.django_db
def test_org_filter_includes(org_models: list[Person], non_org_models: list[Person], org: Organization) -> None:
    request = CCHttpRequest()
    request.org = org
    returned_objs = org_filter(Person, request)
    assert_that([o.first_name for o in returned_objs]).is_equal_to(["Jeremy-org", "Tim-org"])


@pytest.mark.django_db
def test_org_filter_excludes(org_models: list[Person], non_org_models: list[Person], org: Organization) -> None:
    request = CCHttpRequest()
    request.org = None
    returned_objs = org_filter(Person, request)
    assert_that([o.first_name for o in returned_objs]).is_equal_to(["Jeremy-not-org", "Tim-not-org"])


@pytest.mark.django_db
def test_get_object_or_404(org_models: list[Person], non_org_models: list[Person], org: Organization) -> None:
    request = CCHttpRequest()
    request.org = org
    returned_obj = get_object_or_404(Person, request, first_name="Jeremy-org")
    assert_that(returned_obj.first_name).is_equal_to("Jeremy-org")


@pytest.mark.django_db
def test_get_object_or_404_raises(org_models: list[Person], non_org_models: list[Person], org: Organization) -> None:
    request = CCHttpRequest()
    request.org = None
    assert_that(lambda: get_object_or_404(Person, request, first_name="Jeremy-not-org")).raises(Http404)
