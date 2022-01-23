from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from choralcat_core.views import UserCreateView, UserUpdateView
from .models import Composition, Person, Program, Tag, Category, Topic


def index_view(request):
    return render(request, template_name="choralcat_web/index.html")


@login_required
@require_POST
def catalog_search(request):
    term = request.POST["search"]
    context = {
        "compositions": Composition.objects.filter(
            Q(title__icontains=term)
            | Q(composers__first_name__icontains=term)
            | Q(composers__last_name__icontains=term)
            | Q(arrangers__first_name__icontains=term)
            | Q(arrangers__last_name__icontains=term)
        )
    }
    return render(request, template_name="partials/catalog/table.html", context=context)


@login_required
@require_GET
def catalog_modal(request, slug):
    return _render_catalog_modal(request, slug)


def _render_catalog_modal(request, slug):
    composition = get_object_or_404(Composition, slug=slug)
    in_programs = composition.program_set.values_list("slug", flat=True)
    context = {
        "programs": Program.objects.all(),
        "composition": composition,
        "in_programs": in_programs,
    }
    return render(
        request,
        template_name="partials/program_modal/modal_content.html",
        context=context,
    )


class CatalogView(LoginRequiredMixin, ListView):
    model = Composition
    context_object_name = "compositions"
    template_name = "choralcat_web/catalog/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = sorted([str(t) for t in Topic.objects.distinct()])
        context["tags"] = sorted([str(t) for t in Tag.objects.distinct()])
        context["categories"] = sorted([str(c) for c in Category.objects.distinct()])
        context["voicings"] = sorted(
            [
                str(v)
                for v in Composition.objects.order_by("voicing")
                .values_list("voicing", flat=True)
                .distinct()
            ]
        )
        return context


class CompositionDetailView(LoginRequiredMixin, DetailView):
    model = Composition
    context_object_name = "composition"
    template_name = "choralcat_web/catalog/composition_detail.html"


composition_editable_fields = [
    "title",
    "composers",
    "arrangers",
    "duration",
    "starting_key",
    "ending_key",
    "time_period",
    "language",
    "number_of_voices",
    "voicing",
    "categories",
    "accompaniment",
    "tags",
    "topics",
    "rating",
    "score_link",
    "notes",
    "edition_notes",
]


class CompositionCreateView(LoginRequiredMixin, UserCreateView):
    model = Composition
    fields = composition_editable_fields
    template_name = "choralcat_web/catalog/composition_create.html"


class CompositionUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Composition
    fields = composition_editable_fields
    template_name = "choralcat_web/catalog/composition_edit.html"


class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = "choralcat_web/program/programs.html"
    context_object_name = "programs"


class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    template_name = "choralcat_web/program/program_detail.html"
    context_object_name = "program"


class ProgramCreateView(LoginRequiredMixin, UserCreateView):
    model = Program
    fields = ["title", "season"]
    template_name = "choralcat_web/program/program_create.html"

    def form_valid(self, form):
        form.instance.ordering = {"compositions": []}
        return super().form_valid(form)


class ProgramUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Program
    fields = ["title", "season"]
    template_name = "choralcat_web/program/program_edit.html"


@login_required
@require_POST
def program_add(request, slug):
    composition_slug = request.POST["composition_slug"]
    composition = get_object_or_404(Composition, slug=composition_slug)
    program = get_object_or_404(Program, slug=slug)
    program.compositions.add(composition)
    if "compositions" not in program.ordering:
        program.ordering["compositions"] = [composition.slug]
    else:
        program.ordering["compositions"].append(composition.slug)
    program.save()
    return _render_catalog_modal(request, composition_slug)


@login_required
@require_POST
def program_remove(request, slug):
    composition_slug = request.POST["composition_slug"]
    composition = get_object_or_404(Composition, slug=composition_slug)
    program = get_object_or_404(Program, slug=slug)
    program.compositions.remove(composition)
    program.ordering["compositions"] = [
        c for c in program.ordering["compositions"] if c != composition.slug
    ]
    program.save()
    return _render_program(request, program)


def _render_program(request, program):
    context = {"program": program}
    return render(
        request,
        template_name="partials/program/program_detail_partial.html",
        context=context,
    )


@login_required
@require_POST
def program_reorder(request, slug):
    new_ordering = request.POST.getlist("slug")
    program = get_object_or_404(Program, slug=slug)
    program.ordering["compositions"] = new_ordering
    program.save()
    return _render_program_catalog(request, program)


def _render_program_catalog(request, program):
    context = {"program": program}
    return render(
        request,
        template_name="partials/program/program_catalog.html",
        context=context,
    )


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = "choralcat_web/people/persons.html"
    context_object_name = "persons"


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = "choralcat_web/people/person_detail.html"
    context_object_name = "person"


class PersonCreateView(LoginRequiredMixin, UserCreateView):
    model = Person
    fields = [
        "first_name",
        "last_name",
        "birth",
        "death",
        "poc",
        "non_male_identifying",
        "bio",
    ]
    template_name = "choralcat_web/people/person_create.html"


class PersonUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Person
    fields = [
        "first_name",
        "last_name",
        "birth",
        "death",
        "poc",
        "non_male_identifying",
        "bio",
    ]
    template_name = "choralcat_web/people/person_edit.html"
