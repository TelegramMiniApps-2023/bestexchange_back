import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
apps.populate(settings.INSTALLED_APPS)


from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

from no_cash.endpoints import api_router, no_cash_router


def get_application() -> FastAPI:
    app = FastAPI(title='BestChangeTgBot API', debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api_router.include_router(no_cash_router)
    app.include_router(api_router, prefix=settings.FASTAPI_PREFIX)
    app.mount(settings.DJANGO_PREFIX, WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()