import typing as t
from fastapi import APIRouter

routes = APIRouter()


@routes.get('/funds', response_model=t.List[dict], status_code=200)
async def get_funds():
    pass


@routes.post('/deals', response_model=t.List[dict], status_code=201)
async def create_deals():
    pass
