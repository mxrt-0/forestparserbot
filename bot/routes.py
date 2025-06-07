from typing import Annotated

from fastapi import APIRouter, Request, Header, HTTPException
from aiogram.types import Update
from loguru import logger

from bot.bot import bot, dp
from bot.settings import get_settings

cfg = get_settings()

root_router = APIRouter(
    prefix="", tags=["root"], responses={404: {"description": "Not found"}}
)


@root_router.post(cfg.WEBHOOK_BOT_PATH)
async def bot_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> None | dict:
    try:
        if x_telegram_bot_api_secret_token != cfg.BOT_SECRET_TOKEN:
            raise HTTPException(status_code=403, detail="Forbidden")

        payload = await request.json()
        update = Update(**payload)
        await dp.feed_update(bot, update)

        return {"status": "ok"}

    except Exception as e:
        logger.exception(e)
