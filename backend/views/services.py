from fastapi import APIRouter, Depends

from asyncpg.connection import Connection

from dependencies.db import get_db

from schemas import Service, ServiceLoad

from controllers.services_controller import ServicesController

services = APIRouter(
    prefix='/api/services',
    tags=['services']
)


@services.get('/branch/{branch_id}', response_model=list[ServiceLoad],
              description='Возвращает список услуг, предоставляемых банковским отделением с загруженностью этих услуг')
async def branch_services(branch_id: int,
                          db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_branch_services(branch_id)
    return resp


@services.get('/juridical', response_model=list[Service],
              description='Возвращает список услуг для юридических лиц')
async def juridical_services(db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_services_juridical()
    return resp


@services.get('/physical', response_model=list[Service],
              description='Возвращает список услуг для физических лиц')
async def physical_services(db_con: Connection = Depends(get_db)):
    resp = await ServicesController(db_con).get_services_physical()
    return resp
