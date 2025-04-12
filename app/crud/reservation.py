from app.dependency import SessionDependency
from app.models.reservation import Reservation
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from sqlalchemy import select


async def add_reservation(session: SessionDependency, reservation: Reservation):
    session.add(reservation)
    try:
        await session.commit()
        await session.refresh(reservation)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Reservation already exists")


async def get_reservation(session: SessionDependency):
    tables = await session.execute(select(Reservation))
    results = tables.scalars().all()

    if not results:
        raise HTTPException(400, 'Reservation not found')

    return results


async def delete_reservation(session: SessionDependency, reservation: Reservation):

    if not reservation:
        raise HTTPException(400, 'reservation not found')

    await session.delete(reservation)
    await session.commit()


