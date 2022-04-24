from django.apps import AppConfig


class ChoralcatWebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "choralcat.web"

    def ready(self) -> None:
        pass
