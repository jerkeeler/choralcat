from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

default_fixtures = [
    "Program",
    "Composition",
    "User",
    "Tag",
    "Category",
    "Person",
    "Instrument",
    "Topic",
]


class CCTestCase(TestCase):
    fixtures = default_fixtures

    def setUp(self) -> None:
        self.client.login(username="test_user", password="testpassword")
        self.user = User.objects.get(pk=2)
        self.factory = RequestFactory()
