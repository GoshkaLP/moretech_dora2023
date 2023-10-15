from typing import Annotated

from fastapi import APIRouter, Depends, Query

from asyncpg.connection import Connection

from dependencies.db import get_db

from schemas import Branch, BranchScore, BranchLoad

from controllers.routes_controller import RoutesController

routes = APIRouter(
    prefix='/api/routes',
    tags=['routes']
)


@routes.get('/branches', response_model=list[BranchLoad],
            description='Возвращает все банковские отделения ВТБ с их координатами и загруженностью')
async def branches(db_con: Connection = Depends(get_db)):
    resp = await RoutesController(db_con).get_branches()
    return resp


@routes.get('/shortest', response_model=list[BranchScore],
            description='Возвращает результаты алгоритма поиска оптимального отделения с учетом его загруженности')
async def shortest_branches(
        services_ids: Annotated[list[str], Query(description='Массив с id необходимых клиенту сервисов')],
        latitude: Annotated[float, Query(description='Широта местоположения клиента')],
        longitude: Annotated[float, Query(description='Долгота местоположения клиента')],
        db_con: Connection = Depends(get_db)):
    resp = await RoutesController(db_con).search_nearest(services_ids, latitude, longitude)
    return resp
