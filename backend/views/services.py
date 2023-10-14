from fastapi import APIRouter, Depends

from asyncpg.connection import Connection

from backend.dependencies.db import get_db

from backend.schemas import Service

from backend.controllers.services_controller import ServicesController

services = APIRouter(
    prefix='/api/services',
    tags=['services']
)


@services.get('/branch/{branch_id}', response_model=list[Service])
async def test(branch_id: int,
               db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_branch_services(branch_id)
    return resp


@services.get('/juridical', response_model=list[Service])
async def test(db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_services_juridical()
    return resp


@services.get('/physical', response_model=list[Service])
async def test(db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_services_physical()
    return resp
