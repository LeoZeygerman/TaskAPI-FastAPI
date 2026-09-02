from contextlib import asynccontextmanager
from app.database import engine
from fastapi import FastAPI
from app.models import Base
from app.router.tasks import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)