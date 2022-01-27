from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from django.forms import ModelForm

from .models import Program, Composition, Person


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
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
    "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm "
    "border-gray-300 rounded-md"
)


class ProgramForm(ModelForm):
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


checkbox_input_classes = (
    "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
)


class PersonForm(ModelForm):
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
        ]
        widgets = {
            "first_name": widgets.TextInput(attrs={"class": text_input_classes}),
            "last_name": widgets.TextInput(attrs={"class": text_input_classes}),
            "birth": widgets.DateInput(attrs={"class": text_input_classes}),
            "death": widgets.DateInput(attrs={"class": text_input_classes}),
            "poc": widgets.CheckboxInput(attrs={"class": checkbox_input_classes}),
            "non_male_identifying": widgets.CheckboxInput(
                attrs={"class": checkbox_input_classes}
            ),
            "bio": widgets.Textarea(attrs={"class": text_input_classes}),
        }


class CompositionForm(ModelForm):
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
            "title": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "Title"}
            ),
            "starting_key": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "C"}
            ),
            "ending_key": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "Cm"}
            ),
            "voicing": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "satb"}
            ),
            "duration": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "03:00"}
            ),
            "number_of_voices": widgets.NumberInput(
                attrs={"class": text_input_classes, "placeholder": 4}
            ),
            "time_period": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "Modern"}
            ),
            "language": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "Klingon"}
            ),
            "rating": widgets.NumberInput(
                attrs={"class": text_input_classes, "placeholder": "1-5"}
            ),
            "score_link": widgets.TextInput(
                attrs={"class": text_input_classes, "placeholder": "keeler.dev"}
            ),
            "notes": widgets.Textarea(
                attrs={
                    "class": text_input_classes,
                    "placeholder": "Jeremy could've written this one better, tbh",
                }
            ),
            "edition_notes": widgets.Textarea(
                attrs={"class": text_input_classes, "placeholder": "Arabian Nights"}
            ),
            "arrangers": widgets.SelectMultiple(attrs={"class": text_input_classes}),
            "composers": widgets.SelectMultiple(attrs={"class": text_input_classes}),
            "categories": widgets.SelectMultiple(attrs={"class": text_input_classes}),
            "tags": widgets.SelectMultiple(attrs={"class": text_input_classes}),
            "topics": widgets.SelectMultiple(attrs={"class": text_input_classes}),
            "accompaniment": widgets.SelectMultiple(
                attrs={"class": text_input_classes}
            ),
        }
