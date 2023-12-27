from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


exc_dict = {
        400: {
                "message": "Некорректный запрос",
                "details": "Отсутствует обязательный параметр '{}'",
                },
        404: {
                "message": "Нет доступных данных",
                "details": "Запрошенный ресурс '{}' не существует",
                },
}


class CustomJSONException(HTTPException):
        pass


def my_json_exception_handle(request: Request, exc: HTTPException):
        '''
        Возвращает JSON ответ ошибки
        '''
        return JSONResponse(status_code=exc.status_code,
                                content={
                                        'error': {
                                                'code': exc.detail['code'],
                                                'message': exc.detail['message'],
                                                'details': exc.detail['details'],
                                        }
                                })


def http_exception_json(status_code: int, param: str):
        '''
        Поднимает HTTP ошибку по переданному коду ошибки
        '''

        raise CustomJSONException(
                status_code=status_code,
                detail={
                        'code': status_code,
                        'message': exc_dict[status_code]['message'],
                        'details': exc_dict[status_code]['details'].format(param),
                })