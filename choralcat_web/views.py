import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from choralcat_core.views import UserCreateView, UserUpdateView
from .consts import DEFAULT_NUM_PER_PAGE
from .forms import CompositionForm, PersonForm, ProgramForm
from .models import Composition, Person, Program, Tag, Category, Topic, Instrument

logger = logging.getLogger(__name__)


def index_view(request):
    return render(request, template_name="choralcat_web/index.html")


class ChoralcatLoginView(LoginView):
    def get_success_url(self):
        logger.info(f"User {self.request.POST['username']} has logged in")
        return super().get_success_url()


class ChoralcatLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user and self.request.user.is_authenticated:
            logger.info(f"User {self.request.user} has logged out")
        return super().dispatch(request, *args, **kwargs)


@login_required
@require_POST
def catalog_search(request):
    term = request.POST.get("search")
    page = request.POST.get("page", 1)
    per_page = request.POST.get("per_page", DEFAULT_NUM_PER_PAGE)
    logger.debug(f"Querying database for compositions related to: {term}")
    if term:
        compositions = Composition.objects.filter(
            Q(title__icontains=term)
            | Q(composers__first_name__icontains=term)
            | Q(composers__last_name__icontains=term)
            | Q(arrangers__first_name__icontains=term)
            | Q(arrangers__last_name__icontains=term)
        ).distinct()
    else:
        compositions = Composition.objects.all()
    paginator = Paginator(compositions, per_page, allow_empty_first_page=True)
    page = paginator.get_page(page)
    context = {"compositions": page.object_list, "page_obj": page}
    return render(
        request,
        template_name="partials/catalog/table_with_pagination.html",
        context=context,
    )


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
    paginate_by = DEFAULT_NUM_PER_PAGE

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


class CompositionCreateView(LoginRequiredMixin, UserCreateView):
    model = Composition
    form_class = CompositionForm
    template_name = "choralcat_web/catalog/composition_create.html"


class CompositionUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Composition
    form_class = CompositionForm
    template_name = "choralcat_web/catalog/composition_edit.html"


@login_required
@require_POST
def category_add(request):
    return _simple_add_view(
        request, Category, "categories", reverse_lazy("category_add")
    )


@login_required
@require_POST
def instrument_add(request):
    return _simple_add_view(
        request, Instrument, "accompaniment", reverse_lazy("instrument_add")
    )


@login_required
@require_POST
def topic_add(request):
    return _simple_add_view(request, Topic, "topics", reverse_lazy("topic_add"))


@login_required
@require_POST
def tag_add(request):
    return _simple_add_view(request, Tag, "tags", reverse_lazy("tag_add"))


@transaction.atomic
def _simple_add_view(request, model, relationship_name, tag_url):
    selected_values = request.POST.getlist(relationship_name)
    new_value = request.POST.get(f"new_{relationship_name}")
    removed_value = request.POST.get("remove")
    logger.debug(f"selected values: {selected_values}")

    current_values = []
    if selected_values:
        pks = [int(c) for c in selected_values]
        current_values = {c.pk: c for c in model.objects.filter(pk__in=pks)}
        current_values = [current_values[pk] for pk in pks]

    if new_value:
        try:
            new_object = model.objects.get(value=new_value)
            logger.debug(f"Found value {new_value}")
        except model.DoesNotExist:
            new_object = model.objects.create(value=new_value, user=request.user)
            logger.info(f"{request.user} created new {model.__name__} {new_value}")
        if new_object not in current_values:
            current_values.append(new_object)

    if removed_value:
        logger.debug(f"Removing {removed_value}")
        removed_value = get_object_or_404(model, value=removed_value)
        current_values = [c for c in current_values if c != removed_value]

    context = {
        "widget_name": relationship_name,
        "selected": [{"label": c.value, "value": c.id} for c in current_values],
        "tag_url": tag_url,
    }
    return render(
        request,
        "choralcat_web/widgets/tag_widget_response.html",
        context=context,
    )


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
    form_class = ProgramForm
    template_name = "choralcat_web/program/program_create.html"

    def form_valid(self, form):
        form.instance.ordering = {"compositions": []}
        return super().form_valid(form)


class ProgramUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "choralcat_web/program/program_edit.html"


@login_required
@require_POST
def program_add(request, slug):
    composition_slug = request.POST["composition_slug"]
    composition = get_object_or_404(Composition, slug=composition_slug)
    program = get_object_or_404(Program, slug=slug)
    logger.debug(f"Adding {composition} to program {program}")
    program.add(composition)
    program.save()
    return _render_catalog_modal(request, composition_slug)


@login_required
@require_POST
def program_remove(request, slug):
    composition_slug = request.POST["composition_slug"]
    composition = get_object_or_404(Composition, slug=composition_slug)
    program = get_object_or_404(Program, slug=slug)
    program.remove(composition)
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
    logger.debug(f"Reordering program {program} to {new_ordering}")
    program.reorder(new_ordering)
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
    form_class = PersonForm
    template_name = "choralcat_web/people/person_create.html"


class PersonUpdateView(LoginRequiredMixin, UserUpdateView):
    model = Person
    form_class = PersonForm
    template_name = "choralcat_web/people/person_edit.html"
