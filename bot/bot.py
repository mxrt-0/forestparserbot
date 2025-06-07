from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

from loguru import logger

from bot.settings import get_settings

cfg = get_settings()

redis = Redis.from_url(cfg.REDIS_URL)
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

bot = Bot(token=cfg.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

COUNTRY_CODES = {"ru": "Запустить бота ♻️", "en": "Start the bot ♻️"}


async def get_commands(cc: str) -> list[BotCommand]:
    desc = COUNTRY_CODES.get(cc, COUNTRY_CODES["ru"])
    return [BotCommand(command="/start", description=desc)]


async def set_bot_commands() -> None:
    await bot.set_my_commands(await get_commands(cc="ru"), language_code="ru")
    await bot.set_my_commands(await get_commands(cc="en"), language_code="en")


async def set_webhook() -> None:
    await bot.set_webhook(
        url=f"{cfg.BASE_URL}{cfg.WEBHOOK_BOT_PATH}",
        secret_token=cfg.BOT_SECRET_TOKEN,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


async def on_startup_notify() -> None:
    """Notify about successful start"""
    text = "🚀 Starting application"
    try:
        logger.info(text)
    except Exception as e:
        logger.exception(e)
    for admin in cfg.ADMINS:
        try:
            logger.info(text)
            await bot.send_message(chat_id=admin, text=text)
        except Exception as e:
            logger.exception(e)


async def start_bot() -> None:
    await on_startup_notify()
    await set_webhook()
    await set_bot_commands()


async def on_shutdown_notify() -> None:
    """Notify about successful stop"""
    text = "⛔ Stopping application"
    try:
        logger.info(text)
    except Exception as e:
        logger.exception(e)
    for admin in cfg.ADMINS:
        try:
            await bot.send_message(chat_id=admin, text=text)
        except Exception as e:
            logger.exception(e)
