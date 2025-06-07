from contextlib import asynccontextmanager
from fastapi import FastAPI

from bot.routes import root_router
from bot.bot import start_bot, on_shutdown_notify

import bot.handlers  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_bot()
    yield
    await on_shutdown_notify()


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
