from sqlalchemy import select
from app.constants import STATUS_DELETED
from fastapi import APIRouter
from app.crud.table import add_tables, get_tables, table_delete
from app.dependency import SessionDependency
from app.models.table import Table
from app.schemas.table import CreateTableRequest, CreateTableResponse, GetTableResponse, DeleteTableResponse

table_router = APIRouter()

@table_router.post("/tables", response_model=CreateTableResponse)
async def create_table(session: SessionDependency, table_request: CreateTableRequest):
    # Преобразуем входящий запрос в словарь
    table_dict = table_request.model_dump()
    # Создаем новый объект Table с использованием данных из запроса
    table = Table(**table_dict)
    # Добавляем новый объект в базу данных
    await add_tables(session, table)
    # Возвращаем идентификатор созданной таблицы
    return table.id_dict


@table_router.get('/tables', response_model=GetTableResponse)
async def get_all_tables(session: SessionDependency):
    # Получаем все таблицы из базы данных
    tables = await get_tables(session)
    # Возвращаем ответ в формате GetTableResponse с преобразованными данными таблиц
    return GetTableResponse(tables=[table.dict_ for table in tables])


@table_router.delete('/tables/{table_id}', response_model=DeleteTableResponse)
async def delete_table(session: SessionDependency, table_id: int):
    # Создаем запрос для поиска таблицы по ее идентификатору
    chek = select(Table).where(Table.id == table_id)

    # Выполняем запрос и получаем результат
    table = await session.execute(chek)

    # Извлекаем первый найденный объект таблицы
    result = table.scalars().first()

    # Удаляем найденную таблицу из базы данных
    await table_delete(session, result)

    # Возвращаем статус удаления
    return STATUS_DELETED
