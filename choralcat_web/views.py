from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index_view(request):
    return render(request, template_name="choralcat_web/index.html")


@login_required
def catalog_view(request):
    return render(request, template_name="choralcat_web/catalog.html")


@login_required
def composition_detail_view(request):
    return render(request, template_name="choralcat_web/composition_detail.html")


@login_required
def program_list_view(request):
    return render(request, template_name="choralcat_web/programs.html")


@login_required
def program_detail_view(request):
    return render(request, template_name="choralcat_web/program_detail.html")


@login_required
def person_list_view(request):
    return render(request, template_name="choralcat_web/persons.html")


@login_required
def person_detail_view(request):
    return render(request, template_name="choralcat_web/persons_detail.html")
