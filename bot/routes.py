from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from aiogram.types import Update
from loguru import logger

from bot import bot, dp
from settings import get_settings

cfg: Settings = get_settings()

root_router = APIRouter(
    prefix="", tags=["root"], responses={404: {"description": "Not found"}}
)


@root_router.post(cfg.WEBHOOK_BOT_PATH)
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> None | dict:
    try:
        if x_telegram_bot_api_secret_token != cfg.BOT_SECRET_TOKEN:
            raise HTTPException(status=403, detail="Forbidden")

        update = Update(**update)
        await dp.feed_update(bot, update)

        return {"status": "ok"}

    except Exception as e:
        logger.exception(e)
