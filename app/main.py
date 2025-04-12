from fastapi import FastAPI
from app.lifespan import lifespan
from routers.table import table_router
from routers.reservation import reservation_router

app = FastAPI(
    title="Restaurant API",
    description="API for managing restaurant tables",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(table_router, prefix='/api/v1', tags=['table'])
app.include_router(reservation_router, prefix='/api/v1', tags=['reservation'])
