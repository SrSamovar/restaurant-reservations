from typing import Literal

from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    id: int


class CreateTableRequest(BaseModel):
    name: str
    seats: int
    location: str

    class Config:
        from_attributes = True


class CreateTableResponse(BaseResponseModel):
    pass


class GetTables(BaseResponseModel):
    name: str
    seats: int
    location: str


class GetTableResponse(BaseModel):
    tables: list[GetTables]


class DeleteTableResponse(BaseModel):
    status: Literal['deleted']
