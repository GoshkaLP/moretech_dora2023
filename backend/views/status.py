from fastapi import APIRouter


status = APIRouter(
    prefix='/api/server',
    tags=['server']
)


@status.get('/debug')
async def server_version():
    return {'version': '1.0.0', 'status': 'working'}
