from app.dependency import SessionDependency
from app.models.reservation import Reservation
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from sqlalchemy import select


async def add_reservation(session: SessionDependency, reservation: Reservation):
    # Добавляем новую резервуцию в сессию
    session.add(reservation)
    try:
        # Пытаемся зафиксировать изменения в базе данных
        await session.commit()
        # Обновляем объект резервирования, чтобы получить его сгенерированные поля (например, ID)
        await session.refresh(reservation)
    except IntegrityError:
        # Если возникает ошибка целостности (например, дублирование), откатываем изменения
        await session.rollback()
        raise HTTPException(status_code=400, detail="Reservation already exists")


async def get_reservation(session: SessionDependency):
    # Выполняем запрос для получения всех резервирований
    tables = await session.execute(select(Reservation))
    results = tables.scalars().all()

    # Проверяем, есть ли результаты
    if not results:
        raise HTTPException(400, 'Reservation not found')

    return results


async def delete_reservation(session: SessionDependency, reservation: Reservation):
    # Проверяем, передано ли резервация для удаления
    if not reservation:
        raise HTTPException(400, 'Reservation not found')

    # Удаляем резервирование из сессии
    await session.delete(reservation)

    # Фиксируем изменения в базе данных
    await session.commit()



