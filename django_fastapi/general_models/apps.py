from django.apps import AppConfig


class ValutesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'general_models'
    verbose_name = 'Общее'

    def ready(self) -> None:
        import general_models.signals
