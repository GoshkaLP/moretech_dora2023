from pydantic import BaseModel


class Branch(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float


class Service(BaseModel):
    id: int
    name: str
    service_type: str
