from django.conf import settings

from general_models.models import Valute


def try_generate_icon_url(valute: Valute) -> str | None:
    icon_url = None
    if valute.icon_url.name:
        icon_url = settings.PROTOCOL + settings.SITE_DOMAIN\
                                        + settings.DJANGO_PREFIX\
                                            + valute.icon_url.url
    return icon_url