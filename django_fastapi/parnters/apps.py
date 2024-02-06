from django.apps import AppConfig


class ParntersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parnters'
    verbose_name = 'Партнёры'

    def ready(self) -> None:
        import parnters.signals