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
    """Создает новую резервуцию."""

    # Получаем время резервирования из запроса
    reservation_time = reservation_request.reservation_time

    # Устанавливаем время начала резервирования
    start_time = reservation_time

    # Вычисляем время окончания резервирования на основе продолжительности
    end_time = start_time + datetime.timedelta(minutes=reservation_request.duration_minutes)

    # Создаем запрос для поиска существующих резервирований для данной таблицы
    search = select(Reservation).filter(
        Reservation.table_id == reservation_request.table_id,
        Reservation.reservation_time < end_time,
        Reservation.end_time > start_time
    )

    # Выполняем запрос и получаем результаты
    result = await session.execute(search)
    existing_reservation = result.scalars().all()

    # Если существует конфликтующее резервирование, выбрасываем исключение
    if existing_reservation:
        raise HTTPException(400, 'This table is reserved for this time.')

    # Создаем новый объект Reservation с данными из запроса
    new_reservation = Reservation(
        customer_name=reservation_request.customer_name,
        table_id=reservation_request.table_id,
        reservation_time=start_time,
        duration_minutes=reservation_request.duration_minutes,
        end_time=end_time
    )

    # Добавляем новое резервирование в базу данных
    await add_reservation(session, new_reservation)

    # Возвращаем идентификатор новой резервировки
    return new_reservation.id_dict


@reservation_router.get('/reservations', response_model=GetReservationResponse)
async def get_reservations(session: SessionDependency):
    """Получает все резервирования."""

    # Получаем список всех резервирований из базы данных
    reservations = await get_reservation(session)

    # Возвращаем ответ с преобразованными данными резервирований
    return GetReservationResponse(tables=[reservation.dict_ for reservation in reservations])


@reservation_router.delete('/reservations/{reservation_id}', response_model=DeleteReservationResponse)
async def delete_reservations(session: SessionDependency, reservation_id: int):
    """Удаляет резервирование по идентификатору."""

    # Создаем запрос для поиска резервирования по его идентификатору
    check = select(Reservation).where(Reservation.id == reservation_id)

    # Выполняем запрос и получаем результат
    result = await session.execute(check)

    # Извлекаем найденное резервирование
    existing_reservation = result.scalars().first()

    # Удаляем найденное резервирование из базы данных
    await delete_reservation(session, existing_reservation)

    # Возвращаем статус удаления
    return STATUS_DELETED

