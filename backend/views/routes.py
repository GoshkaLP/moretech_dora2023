from fastapi import APIRouter, Depends

from asyncpg.connection import Connection

from backend.dependencies.db import get_db

from backend.schemas import Branch

from backend.controllers.routes_controller import RoutesController


routes = APIRouter(
    prefix='/api/routes',
    tags=['routes']
)


@routes.get('/branches', response_model=list[Branch])
async def test(db_con: Connection = Depends(get_db)):
    resp = await RoutesController(db_con).get_branches()
    return resp

