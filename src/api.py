from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

from parse import parse
from webob import Request, Response


class BaseResponse:
    def __init__(self, **kwargs):
        self.body: Any = kwargs['body']
        self.headers: dict = kwargs['headers']


class JsonResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers['headers'] = 'Content-Type: text/html'


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


def default_response(response: Response) -> None:
    response.status_code = 404
    response.text = 'Page doesnt exist'


class API:
    def __init__(self):
        self.routes: list[PathStruct] = []


    def __call__(self, environ, start_response) -> Response:
        request = Request(environ)
        response = self.__handle_request(request)
        return response(environ, start_response)


    def __handle_request(self, request: Request) -> Response:
        response = Response()
        handler, kwargs = self.__searching_path(request)
        print(handler, kwargs)
        if handler is not None:
            request_response = handler(request, response)
        else:
            request_response = default_response(response)
        return response


    def __searching_path(self, request: Request) -> (Callable, dict):
        for route in self.routes:
            print(route, request.method, request.path)
            if route.path == request.path and route.method == request.method:
                print('парсим', route.path, request.path)
                parse_result = parse(route.path, request.path)
                print(parse_result)

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
