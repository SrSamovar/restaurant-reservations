from app.dependency import SessionDependency
from app.models.table import Table
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from sqlalchemy import select


async def add_tables(session: SessionDependency, table: Table) -> Table:
    # Добавляем новый объект 'table' в сессию
    session.add(table)
    try:
        # Пытаемся зафиксировать изменения в базе данных
        await session.commit()
        # Возвращаем добавленный объект 'table'
        return table
    except IntegrityError:
        # Если возникает ошибка целостности (например, дублирование), откатываем изменения
        await session.rollback()
        # Генерируем HTTP-исключение с сообщением об ошибке
        raise HTTPException(status_code=400, detail="Table already exists")


async def get_tables(session: SessionDependency) -> list[Table]:
    # Выполняем запрос для получения всех объектов 'Table' из базы данных
    results = await session.execute(select(Table))
    tables = results.scalars().all()

    # Проверяем, есть ли полученные результаты
    if not tables:
        # Если таблицы не найдены, генерируем исключение с соответствующим сообщением
        raise HTTPException(400, 'Tables not found')

    # Возвращаем список найденных таблиц
    return tables


async def table_delete(session: SessionDependency, table: Table):
    # Проверяем, передан ли объект 'table' для удаления
    if not table:
        # Если объект не найден, генерируем исключение
        raise HTTPException(400, 'Table not found')

    # Удаляем объект 'table' из сессии
    await session.delete(table)
    # Фиксируем изменения в базе данных
    await session.commit()


