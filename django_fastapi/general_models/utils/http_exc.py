from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


exc_dict = {
        400: 'Некорректный запрос',
        404: 'Нет доступных данных',
}


class CustomJSONException(HTTPException):
        pass


def my_json_exception_handle(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code,
                            content={
                                    'error': {
                                            'message': exc.detail
                                    }
                            })


def http_exception_json(status_code: int):
        raise CustomJSONException(status_code=status_code,
                                  detail=f'{exc_dict[status_code]}')