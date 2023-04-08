def uri_parser(request: dict):
    return request['PATH_INFO']



def uri_params(request: dict):
    return request['REQUEST_URI'].split('?')[1]
    #pass
