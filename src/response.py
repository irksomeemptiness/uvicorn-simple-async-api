from http import HTTPStatus

DEFAULT_CODE = "utf-8"

class BaseResponse:
    def __init__(self, **kwargs):
        self.body = kwargs.get('body', '')
        self.text: str = kwargs.get('text', '')
        self.headers: list[dict] = [kwargs['headers'] if 'headers' in kwargs else {}]
        self.status: int = kwargs.get('status', HTTPStatus.OK)
        self.extra_headers: list[dict] = kwargs.get('extra_headers', [])

    def headers_to_byte(self):
        headers = []
        for header in self.headers:
            for key, value in header.items():
                headers.append([key.encode(DEFAULT_CODE), value.encode(DEFAULT_CODE)])
        return headers


class PlainResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = [{'Content-Type': 'text/plain'}] + self.extra_headers


class JsonResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = [{'Content-Type': 'text/json'}] + self.extra_headers


class ErrorResponse(BaseResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = [{'Content-Type': 'text/json'}]
        self.body = [{'error': True, 'message': 'Page doesnt exist. Check URL correctness.'}]
        self.status = HTTPStatus.NOT_FOUND
