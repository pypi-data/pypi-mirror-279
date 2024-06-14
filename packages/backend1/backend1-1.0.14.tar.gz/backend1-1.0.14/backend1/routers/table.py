from fastapi import APIRouter, Depends, Request
from backend1.auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from typing import Annotated
from decouple import config
from backend1.utils.utilities import setupHeader
import requests

BACKEND2_URL = config("BACKEND2_URL")

router = APIRouter(
    prefix="/backend1",
)


class Item(BaseModel):
    name: str
    description: str
    class Config:
        from_attributes = True

class ItemId(BaseModel):
    id: int
    class Config:
        from_attributes = True

@router.post("/items", tags=["table"], dependencies=[Depends(JWTBearer())])
async def create_item(item: Annotated[Item, {"description": "Items to be added"}], request: Request):
    headers = setupHeader(request)
    url = f"{BACKEND2_URL}/backend2/items"
    response = requests.post(url, headers=headers, data=item.model_dump_json())
    return response.json()



@router.delete("/items/{item_index}", tags=["table"], dependencies=[Depends(JWTBearer())])
async def remove_item(item_index: Annotated[int, {'description": "Item index to be deleted'}], request: Request):
    headers = setupHeader(request)
    url = f"{BACKEND2_URL}/backend2/items/{item_index}"
    response = requests.delete(url, headers=headers)
    return response.json()

@router.get("/items/all", tags=["table"])
async def read_all_items(request: Request):
    headers = setupHeader(request)
    url = f"{BACKEND2_URL}/backend2/items/all"
    response = requests.get(url, headers=headers)
    return response.json()

@router.get("/items/{item_id}", tags=["table"])
async def read_item_index(item_id: int, request: Request):
    headers = setupHeader(request)
    url = f"{BACKEND2_URL}/backend2/items/{item_id}"
    response = requests.get(url, headers=headers)
    return response.json()