import datetime
from typing import Literal

from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    id: int

class CreateReservationRequest(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime.datetime
    duration_minutes: int

    class Config:
        from_attributes = True


class CreateReservationResponse(BaseResponseModel):
    pass


class GetReservation(BaseResponseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime.datetime
    duration_minutes: int
    end_time: datetime.datetime


class GetReservationResponse(BaseModel):
    tables: list[GetReservation]


class DeleteReservationResponse(BaseModel):
    status: Literal['deleted']
