from django.apps import AppConfig


class PartnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partners'
    verbose_name = 'Партнёры'

    def ready(self) -> None:
        import partners.signals