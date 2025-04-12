import datetime
from app.constants import STATUS_DELETED
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.crud.reservation import add_reservation, get_reservation, delete_reservation
from app.models.reservation import Reservation
from app.dependency import SessionDependency
from app.schemas.reservation import CreateReservationResponse, CreateReservationRequest, GetReservationResponse, \
    DeleteReservationResponse


reservation_router = APIRouter()

@reservation_router.post('/reservations', response_model=CreateReservationResponse)
async def create_reservations(session: SessionDependency, reservation_request: CreateReservationRequest):
    """Creates a reservation."""

    reservation_time = reservation_request.reservation_time


    start_time = reservation_time

    end_time = start_time + datetime.timedelta(minutes=reservation_request.duration_minutes)


    search = select(Reservation).filter(
        Reservation.table_id == reservation_request.table_id,
        Reservation.reservation_time < end_time,
        Reservation.end_time > start_time
    )

    result = await session.execute(search)
    existing_reservation = result.scalars().all()

    if existing_reservation:
        raise HTTPException(400, 'This table is reserved for this time.')

    new_reservation = Reservation(
        customer_name=reservation_request.customer_name,
        table_id=reservation_request.table_id,
        reservation_time=start_time,
        duration_minutes=reservation_request.duration_minutes,
        end_time=end_time
    )

    await add_reservation(session, new_reservation)

    return new_reservation.id_dict


@reservation_router.get('/reservations', response_model=GetReservationResponse)
async def get_reservations(session: SessionDependency):
    reservations = await get_reservation(session)

    return GetReservationResponse(tables=[reservation.dict_ for reservation in reservations])


@reservation_router.delete('/reservations/{reservation_id}', response_model=DeleteReservationResponse)
async def delete_reservations(session: SessionDependency, reservation_id: int):
    check = select(Reservation).where(Reservation.id == reservation_id)

    result = await session.execute(check)

    existing_reservation = result.scalars().first()

    await delete_reservation(session, existing_reservation)

    return STATUS_DELETED
