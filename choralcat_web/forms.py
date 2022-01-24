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


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ["title", "season"]
        widgets = {
            "title": widgets.TextInput(
                attrs={
                    "placeholder": "Awesome Program",
                    "class": "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm "
                    "border-gray-300 rounded-md",
                }
            ),
            "season": widgets.TextInput(
                attrs={
                    "placeholder": "2021",
                    "class": "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm "
                    "border-gray-300 rounded-md",
                }
            ),
        }


text_input_classes = (
    "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border"
    "border-gray-300 rounded-md"
)
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
