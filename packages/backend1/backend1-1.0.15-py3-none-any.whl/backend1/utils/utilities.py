from fastapi import Request

def setupHeader(request:Request):
    headers = {
        "authorization": request.headers.get("authorization"),
    }
    for header, value in request.headers.items():
        if header.lower().startswith("x-"):
            headers[header] = value
    return headers