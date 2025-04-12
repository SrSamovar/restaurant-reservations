from app.dependency import SessionDependency
from app.models.table import Table
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from sqlalchemy import select


async def add_tables(session: SessionDependency, table: Table) -> Table:
    session.add(table)
    try:
        await session.commit()
        return table
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Table already exists")


async def get_tables(session: SessionDependency) -> list[Table]:
    results = await session.execute(select(Table))
    tables = results.scalars().all()

    if not tables:
        raise HTTPException(400, 'Tables not found')

    return tables


async def table_delete(session: SessionDependency, table: Table):

    if not table:
        raise HTTPException(400, 'Table not found')

    await session.delete(table)
    await session.commit()

