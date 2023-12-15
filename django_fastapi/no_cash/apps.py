from django.apps import AppConfig


class NoCashConfig(AppConfig):
    name = "no_cash"
    verbose_name = 'Безналичные'

    def ready(self) -> None:
        import no_cash.signals
