from http import HTTPStatus

import uvicorn

from src.api import API
from src.response import JsonResponse
from src.input_request import InputRequest

app = API()


@app.get("/home")
async def get(request: InputRequest):
    return JsonResponse(body=f'hello get {request}',
                        extra_headers=[{'Test': 'test1'}, {'hehe': 'hehe1'}])


@app.post("/home")
async def post(request: InputRequest):
    body_data = request.body
    print(body_data)
    return JsonResponse(text=f'hello post {request}',
                        body={'test': 'test', 'test1': 1}, status=HTTPStatus.OK)


@app.get("/")
async def get1(request: InputRequest):
    print(request.params)
    return f'hello get1 params'


@app.get("/test1/{test}/mda/{hehe}")
async def get3(request: InputRequest, test: int, hehe: str):
    print(test, hehe, request.params)
    return """hello get /test1/{test}/mda/{hehe}"""


@app.get("/test/{test}")
async def get2(request: InputRequest, test: int):
    print(test, request.params)
    return f'hello get location'


@app.post("/")
async def post1(request: InputRequest):
    return f'hello post1'


@app.put("/")
async def put1(request: InputRequest):
    return f'hello put1'


@app.patch("/")
async def patch1(request: InputRequest):
    return f'hello patch1'


@app.delete("/")
def delete1(request: InputRequest):
    return f'hello delete1'


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()