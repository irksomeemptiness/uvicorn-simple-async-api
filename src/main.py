from webob import Response

from api import API, JsonResponse

app = API()


@app.get("/home")
def get(request):
    #response.text = f'hello get {request}'
    return JsonResponse(text=f'hello get {request}')

@app.post("/home")
def post(request):
    #response.text = f'hello post {request}'
    body_data = request.body
    print(body_data)
    return JsonResponse(text=f'hello post {request}', body={'test': 'test', 'test1': 1})


@app.get("/")
def get1(request):
    return f'hello get1'


@app.post("/")
def post1(request):
    return f'hello post1'


@app.put("/")
def put1(request):
    return f'hello put1'


@app.patch("/")
def patch1(request):
    return f'hello patch1'


@app.delete("/")
def delete1(request):
    return f'hello delete1'