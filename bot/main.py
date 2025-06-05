from aiogram.types import Update

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from loguru import logger

import bot.handlers
from bot.bot import bot, dp
from routes import root_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    from bot.bot import start_bot
    await start_bot()
    yield
    from bot.bot import on_shutdown_notify
    await on_shutdown_notify()

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)


