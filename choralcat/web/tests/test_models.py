from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Composition, Program


class ProgramTestCase(TestCase):
    fixtures = ["User"]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.get(pk=2)
        cls.composition1 = Composition.objects.create(title="Composition Example", user=cls.user, slug="comp-1")
        cls.composition2 = Composition.objects.create(title="Composition2 Example", user=cls.user, slug="comp-2")
        cls.program = Program.objects.create(title="Program Example", user=cls.user)
        cls.program.add(cls.composition1)

    def test_add_composition(self):
        self.assertEqual(1, self.program.compositions.count())
        self.program.add(self.composition2)
        self.assertEqual(2, self.program.compositions.count())
        self.assertEqual(["comp-1", "comp-2"], self.program.ordering["compositions"])

    def test_remove_composition(self):
        self.assertEqual(1, self.program.compositions.count())
        self.program.remove(self.composition1)
        self.assertEqual(0, self.program.compositions.count())
        self.assertEqual([], self.program.ordering["compositions"])

    def test_reorder_compositions(self):
        self.program.add(self.composition2)
        self.assertEqual(["comp-1", "comp-2"], self.program.ordering["compositions"])
        self.program.reorder(["comp-2", "comp-1"])
        self.assertEqual(["comp-2", "comp-1"], self.program.ordering["compositions"])

    def test_compositions_ordered_fail_gracefully(self):
        self.program.ordering = {}
        self.assertEqual(1, len(self.program.compositions_ordered))
        self.assertEqual(["comp-1"], self.program.ordering["compositions"])

    def test_compositions_ordered_fail_gracefully_missing_key(self):
        self.program.add(self.composition2)
        self.program.ordering = {"compositions": ["comp-2"]}
        self.assertEqual(2, len(self.program.compositions_ordered))
        self.assertEqual(["comp-1", "comp-2"], self.program.ordering["compositions"])
