import inspect
import json
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any, Coroutine, AsyncIterable

from parse import parse
from uvicorn.protocols.http.h11_impl import RequestResponseCycle

from src.response import BaseResponse, PlainResponse, ErrorResponse, JsonResponse, DEFAULT_CODE
from src.input_request import InputRequest


class HttpMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


@dataclass(repr=True)
class PathStruct:
    method: str
    path: str
    handler: Coroutine


def default_response() -> BaseResponse:
    return ErrorResponse()


class API:
    def __init__(self) -> None:
        self.routes: list[PathStruct] = []


    async def __call__(
            self, scope: dict, receive: RequestResponseCycle, send: Any) -> None:
        if scope['type'] in ('http', 'https'):
            request = InputRequest(**scope)
            response_obj = await self.__handle_request(request, receive)
            await self.response(response_obj, send)


    async def __handle_request(self, request: InputRequest, receive: RequestResponseCycle) -> BaseResponse:
        request._body = await read_body(receive)
        handler, kwargs = await self.__searching_path(request)
        if handler is not None:
            if inspect.iscoroutinefunction(handler):
                response_obj: BaseResponse = await handler(request, **kwargs)
            else:
                response_obj: BaseResponse = handler(request, **kwargs)

            if not isinstance(response_obj, JsonResponse):
                response_obj = PlainResponse(body=response_obj)
        else:
            response_obj: BaseResponse = default_response()
        return response_obj


    async def __path_genarator(self) -> AsyncIterable:
        for route in self.routes:
            yield route


    async def __searching_path(self, request: InputRequest) -> (Callable, dict):
        async for route in self.__path_genarator():
            parse_result = parse(route.path, request.path)
            if parse_result and route.method == request.method:
                if parse_result is not None:
                    return route.handler, parse_result.named
        return None, None


    @staticmethod
    async def response(response: BaseResponse, send) -> None:
        await send({
            'type': 'http.response.start',
            'status': response.status,
            'headers': response.headers_to_byte()
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(response.body).encode(DEFAULT_CODE)
                if isinstance(response.body, dict)
                else str(response.body).encode(DEFAULT_CODE)
        })


    def get(self, path: str) -> Callable:
        def wrapper(handler: Coroutine):
            self.routes.append(PathStruct(path=path, method=HttpMethods.GET.value, handler=handler))
            return handler
        return wrapper


    def post(self, path: str) -> Callable:
        def wrapper(handler: Coroutine):
            self.routes.append(PathStruct(path=path, method=HttpMethods.POST.value, handler=handler))
            return handler
        return wrapper


    def put(self, path: str) -> Callable:
        def wrapper(handler: Coroutine):
            self.routes.append(PathStruct(path=path, method=HttpMethods.PUT.value, handler=handler))
            return handler
        return wrapper


    def patch(self, path: str) -> Callable:
        def wrapper(handler: Coroutine):
            self.routes.append(PathStruct(path=path, method=HttpMethods.PATCH.value, handler=handler))
            return handler
        return wrapper


    def delete(self, path: str) -> Callable:
        def wrapper(handler: Coroutine):
            self.routes.append(PathStruct(path=path, method=HttpMethods.DELETE.value, handler=handler))
            return handler
        return wrapper


async def read_body(receive: RequestResponseCycle) -> bytes:
    body = b''
    more_body = True

    while more_body:
        message = await receive()   # which type ?????????
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body