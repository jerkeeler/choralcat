from django.test import TestCase


class BadTest(TestCase):
    def test_fail(self):
        self.assertTrue(False)
