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
    table_dict = table_request.model_dump()
    table = Table(**table_dict)
    await add_tables(session, table)
    return table.id_dict


@table_router.get('tables', response_model=GetTableResponse)
async def get_all_tables(session: SessionDependency):
    tables = await get_tables(session)
    return GetTableResponse(tables=[table.dict_ for table in tables])


@table_router.delete('/tables/{table_id}', response_model=DeleteTableResponse)
async def delete_table(session: SessionDependency, table_id: int):
    chek = select(Table).where(Table.id == table_id)

    table = await session.execute(chek)

    result = table.scalars().first()

    await table_delete(session, result)

    return STATUS_DELETED
