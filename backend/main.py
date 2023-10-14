from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.views import status, routes, services


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status)
app.include_router(routes)
app.include_router(services)
