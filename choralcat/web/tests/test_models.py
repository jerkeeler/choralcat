import pytest
from assertpy import assert_that

from ..models import Composition, Organization, Program


@pytest.fixture
@pytest.mark.django_db
def composition1(org: Organization) -> Composition:
    return Composition.objects.create(title="Composition Example", organization=org, slug="comp-1")


@pytest.fixture
@pytest.mark.django_db
def composition2(org: Organization) -> Composition:
    return Composition.objects.create(title="Composition2 Example", organization=org, slug="comp-2")


@pytest.fixture
@pytest.mark.django_db
def program(org: Organization, composition1) -> Program:
    program = Program.objects.create(title="Program Example", organization=org)
    program.add(composition1)
    return program


@pytest.mark.django_db
def test_add_composition(program: Program, composition2: Composition) -> None:
    assert_that(program.compositions.count()).is_equal_to(1)
    program.add(composition2)
    assert_that(program.compositions.count()).is_equal_to(2)
    assert_that(program.ordering["compositions"]).is_equal_to(["comp-1", "comp-2"])


@pytest.mark.django_db
def test_remove_composition(program: Program, composition1: Composition) -> None:
    assert_that(program.compositions.count()).is_equal_to(1)
    program.remove(composition1)
    assert_that(program.compositions.count()).is_equal_to(0)
    assert_that(program.ordering["compositions"]).is_equal_to([])


@pytest.mark.django_db
def test_reorder_compositions(program: Program, composition2: Composition) -> None:
    program.add(composition2)
    assert_that(program.ordering["compositions"]).is_equal_to(["comp-1", "comp-2"])
    program.reorder(["comp-2", "comp-1"])
    assert_that(program.ordering["compositions"]).is_equal_to(["comp-2", "comp-1"])


@pytest.mark.django_db
def test_compositions_ordered_fail_gracefully(program: Program) -> None:
    program.ordering = {}
    assert_that(program.compositions_ordered).is_length(1)
    assert_that(program.ordering["compositions"]).is_equal_to(["comp-1"])


@pytest.mark.django_db
def test_compositions_ordered_fail_gracefully_missing_key(program: Program, composition2: Composition) -> None:
    program.add(composition2)
    program.ordering = {"compositions": ["comp-2"]}
    assert_that(program.compositions_ordered).is_length(2)
    assert_that(program.ordering["compositions"]).is_equal_to(["comp-1", "comp-2"])
