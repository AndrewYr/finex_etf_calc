import typing as t
from fastapi import APIRouter

admin_routes = APIRouter()


@admin_routes.post('/funds', response_model=t.List[dict], status_code=201)
async def create_funds():
    pass
