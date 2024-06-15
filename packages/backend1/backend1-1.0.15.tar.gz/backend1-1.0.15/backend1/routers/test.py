from fastapi import APIRouter, Depends, Request
from backend1.auth.auth_bearer import JWTBearer
import requests
from decouple import config
from backend1.utils.utilities import setupHeader

BACKEND2_URL = config("BACKEND2_URL")

router = APIRouter(
    prefix="/backend1",
)

@router.get("/hello_world")
async def hello_world():
    return {"message": "Hello RDSS KS"}


@router.get("/test_authentication", dependencies=[Depends(JWTBearer())])
async def test_authentication():
    return {"message": "Authentication successfull"}


@router.get("/test_backend2")
async def test_backend2():
    url = f"{BACKEND2_URL}/backend2/hello_backend2"
    response = requests.get(url)
    print(response.json())
    return response.json()

@router.get("/test_authentication_backend2", dependencies=[Depends(JWTBearer())])
async def test_authentication_backend2(request: Request):
    headers = setupHeader(request)
    url = f"{BACKEND2_URL}/backend2/test_backend2_authenticaton"
    response = requests.get(url, headers=headers)
    return response.json()





