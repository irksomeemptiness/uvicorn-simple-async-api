from typing import Any

from . import uri_parser


def request_handler(request: dict, start_response) -> (str, Any):
    response_body = b"Hello, World!"

    headers = [
       ("Content-Type", "text/plain"),
       ("Content-Length", str(len(response_body)))
    ]
    if request_validator(request):

        uri_obj = uri_parser.uri_parser(request)
        match request['REQUEST_METHOD']:
            case 'GET':
                print('get', uri_obj)
            case 'POST':
                print('post', uri_obj)
            case 'PUT':
                print('put', uri_obj)
            case 'DELETE':
                print('delete', uri_obj)

    status = "200 OK"
    start_response(status, headers=headers)
    return response_body


def request_validator(request: dict):
    if request['REQUEST_URI'] == '/favicon.ico':
        return False
    return True
