import json
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

from parse import parse
from webob import Request, Response


class BaseResponse:
    def __init__(self, **kwargs):
        self.body: Any = ''
        self.text: str = kwargs['text']
        self.headers: dict = kwargs['headers'] if 'headers' in kwargs else {}
        self.status: int = kwargs['status'] if 'status' in kwargs else 200


class PlainResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers['headers'] = 'Content-Type: text/plain'
        self.body = kwargs['body'] if 'body' in kwargs else ''

class JsonResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers['headers'] = 'Content-Type: text/json'
        self.body = kwargs['body'] if 'body' in kwargs else ''


class AppRequest:
    def __init__(self, request: Request):
        self.body = request.body.decode()
        self.headers = request.headers
        self.text = request.text

class Methods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


@dataclass(repr=True)
class PathStruct:
    method: str
    path: str
    handler: Callable


def default_response() -> BaseResponse:
    return PlainResponse(status=404, text='Page doesnt exist')


class API:
    def __init__(self):
        self.routes: list[PathStruct] = []


    def __call__(self, environ, start_response) -> Response:
        request = Request(environ)
        response = self.__handle_request(request)
        return response(environ, start_response)


    def __handle_request(self, request: Request) -> Response:
        handler, kwargs = self.__searching_path(request)
        app_request = AppRequest(request)
        if handler is not None:
            response_obj: BaseResponse = handler(app_request)
            # handle raw response from funcs
            if not isinstance(response_obj, BaseResponse):
                response_obj = PlainResponse(text=response_obj)
        else:
            response_obj: BaseResponse = default_response()

        response = Response()
        response.status = response_obj.status
        response.text = response_obj.text
        response.headers = response_obj.headers
        response.body = json.dumps(response_obj.body).encode()
        return response


    def __searching_path(self, request: Request) -> (Callable, dict):
        for route in self.routes:
            print(route, request.method, request.path)
            if route.path == request.path and route.method == request.method:
                print('парсим', route.path, request.path)
                parse_result = parse(route.path, request.path)

                if parse_result is not None:
                    return route.handler, parse_result.named
        return None, None


    def get(self, path: str):
        def wrapper(handler):
            self.routes.append(PathStruct(path=path, method=Methods.GET.value, handler=handler))
            return handler
        return wrapper


    def post(self, path: str):
        def wrapper(handler):
            self.routes.append(PathStruct(path=path, method=Methods.POST.value, handler=handler))
            return handler
        return wrapper


    def put(self, path: str):
        def wrapper(handler):
            self.routes.append(PathStruct(path=path, method=Methods.PUT.value, handler=handler))
            return handler
        return wrapper


    def patch(self, path: str):
        def wrapper(handler):
            self.routes.append(PathStruct(path=path, method=Methods.PATCH.value, handler=handler))
            return handler
        return wrapper


    def delete(self, path: str):
        def wrapper(handler):
            self.routes.append(PathStruct(path=path, method=Methods.DELETE.value, handler=handler))
            return handler
        return wrapper
