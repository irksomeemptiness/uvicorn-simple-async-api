from api import API

app = API()


@app.get("/home")
def get(request, response):
    #response.text = f'hello get {request}'
    return f'hello get {request}'

@app.post("/home")
def post(request, response):
    #response.text = f'hello post {request}'
    return f'hello post {request}'


@app.get("/")
def get1(request, response):
    response.text = f'hello get1'
    return f'hello get1'


@app.post("/")
def post1(request, response):
    response.text = f'hello post1'
    return f'hello post1'


@app.put("/")
def put1(request, response):
    response.text = f'hello put1'
    return f'hello put1'


@app.patch("/")
def patch1(request, response):
    response.text = f'hello patch1 '
    return f'hello patch1'


@app.delete("/")
def delete1(request, response):
    response.text = f'hello delete1'
    return f'hello delete1'