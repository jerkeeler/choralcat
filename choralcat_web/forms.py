from django.contrib.auth.forms import AuthenticationForm


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
