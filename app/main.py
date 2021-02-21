from fastapi import FastAPI

from app.config.settings import get_settings
from app.routes.router import router
from app.database.database import database
settings = get_settings()


app = FastAPI(
    title=settings.APP_NAME,
    prefix=settings.API_PREFIX,
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router, prefix=settings.API_PREFIX)
