import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
apps.populate(settings.INSTALLED_APPS)


from fastapi import FastAPI, APIRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

from general_models.endpoints import common_router
from no_cash.endpoints import no_cash_router
from cash.endpoints import cash_router

from general_models.utils.http_exc import (CustomJSONException,
                                           my_json_exception_handle)


#Связывает Django и FastAPI
def get_application() -> FastAPI:
    app = FastAPI(title='BestChangeTgBot API', debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api_router = APIRouter(prefix=settings.FASTAPI_PREFIX)
    api_router.include_router(common_router)
    api_router.include_router(no_cash_router)
    api_router.include_router(cash_router)

    app.add_exception_handler(CustomJSONException,
                              my_json_exception_handle)

    app.include_router(api_router)
    app.mount(settings.DJANGO_PREFIX, WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()