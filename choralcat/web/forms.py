from typing import Any, Type

from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Model
from django.forms import FileField, Form, ModelForm, widgets
from django.urls import reverse_lazy

from .models import Category, Composition, Instrument, Person, Program, Tag, Topic
from .widgets import AutocompleteStringWidget, MtMStringWidget, TagWidget


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "focus:ring-accent500 focus:border-accent500 block w-full pl-4 pr-4 sm:text-sm "
                "border-gray-300 rounded-md"
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "focus:ring-accent500 focus:border-accent500 block w-full pl-4 pr-4 sm:text-sm "
                "border-gray-300 rounded-md"
            }
        )


text_input_classes = (
    "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm " "border-gray-300 rounded-md"
)


class OrgForm(ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.org = kwargs.pop("org")
        super().__init__(*args, **kwargs)


class ProgramForm(OrgForm):
    template_name = "web/program/program_form.html"

    class Meta:
        model = Program
        fields = ["title", "season"]
        widgets = {
            "title": widgets.TextInput(
                attrs={
                    "placeholder": "Awesome Program",
                    "class": text_input_classes,
                }
            ),
            "season": widgets.TextInput(
                attrs={
                    "placeholder": "2021",
                    "class": text_input_classes,
                }
            ),
        }


checkbox_input_classes = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"


class PersonForm(OrgForm):
    template_name = "web/people/person_form.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["nationality"].widget.queryset = Person.objects.filter(organization=self.org)

    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "birth",
            "death",
            "poc",
            "non_male_identifying",
            "bio",
            "nationality",
        ]
        widgets = {
            "first_name": widgets.TextInput(attrs={"class": text_input_classes}),
            "last_name": widgets.TextInput(attrs={"class": text_input_classes}),
            "birth": widgets.DateInput(attrs={"class": text_input_classes}),
            "death": widgets.DateInput(attrs={"class": text_input_classes}),
            "poc": widgets.CheckboxInput(attrs={"class": checkbox_input_classes}),
            "non_male_identifying": widgets.CheckboxInput(attrs={"class": checkbox_input_classes}),
            "nationality": AutocompleteStringWidget(field="nationality", attrs={"placeholder": "georgian"}),
            "bio": widgets.Textarea(attrs={"class": text_input_classes}),
        }


class CompositionForm(OrgForm):
    template_name = "web/catalog/catalog_form.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        comp_filter = Composition.objects.filter(organization=self.org)
        self.fields["time_period"].widget.queryset = comp_filter
        self.fields["language"].widget.queryset = comp_filter
        self.fields["voicing"].widget.queryset = comp_filter

        def simple_choices(model: Type[Model]) -> Any:
            return model.objects.filter(organization=self.org).values_list("pk", "value")

        self.fields["categories"].widget.choices = simple_choices(Category)
        self.fields["tags"].widget.choices = simple_choices(Tag)
        self.fields["topics"].widget.choices = simple_choices(Topic)
        self.fields["accompaniment"].widget.choices = simple_choices(Instrument)

        composer_choices = [(c.pk, c.name) for c in Person.objects.filter(organization=self.org)]
        self.fields["composers"].widget.choices = composer_choices
        self.fields["arrangers"].widget.choices = composer_choices

    class Meta:
        model = Composition
        fields = [
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

        widgets = {
            "title": widgets.TextInput(attrs={"class": text_input_classes, "placeholder": "Title"}),
            "starting_key": widgets.TextInput(attrs={"class": text_input_classes, "placeholder": "C"}),
            "ending_key": widgets.TextInput(attrs={"class": text_input_classes, "placeholder": "Cm"}),
            "voicing": AutocompleteStringWidget(field="voicing", attrs={"placeholder": "satb"}),
            "duration": widgets.TextInput(attrs={"class": text_input_classes, "placeholder": "03:00"}),
            "number_of_voices": widgets.NumberInput(attrs={"class": text_input_classes, "placeholder": 4}),
            "time_period": AutocompleteStringWidget(field="time_period", attrs={"placeholder": "Modern"}),
            "language": AutocompleteStringWidget(field="language", attrs={"placeholder": "Klingon"}),
            "rating": widgets.NumberInput(attrs={"class": text_input_classes, "placeholder": "1-5"}),
            "score_link": widgets.TextInput(attrs={"class": text_input_classes, "placeholder": "keeler.dev"}),
            "notes": widgets.Textarea(
                attrs={
                    "class": text_input_classes,
                    "placeholder": "Jeremy could've written this one better, tbh",
                }
            ),
            "edition_notes": widgets.Textarea(attrs={"class": text_input_classes, "placeholder": "Arabian Nights"}),
            "composers": MtMStringWidget(attrs={"placeholder": "Search artists..."}),
            "arrangers": MtMStringWidget(attrs={"placeholder": "Search artists..."}),
            "categories": TagWidget(
                attrs={
                    "placeholder": "Search for a category...",
                    "tag_url": reverse_lazy("category_add"),
                }
            ),
            "tags": TagWidget(
                attrs={
                    "placeholder": "Search for a tag...",
                    "tag_url": reverse_lazy("tag_add"),
                }
            ),
            "topics": TagWidget(
                attrs={
                    "placeholder": "Search for a topic...",
                    "tag_url": reverse_lazy("topic_add"),
                }
            ),
            "accompaniment": TagWidget(
                attrs={
                    "placeholder": "Search for an instrument...",
                    "tag_url": reverse_lazy("instrument_add"),
                }
            ),
        }


class CompositionScoreForm(Form):
    file = FileField()
