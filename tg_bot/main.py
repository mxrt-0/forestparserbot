import asyncio
from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand

import logging

from create_bot import bot, dp
from middlewares import middlewares_query_list , middlewares_message_list
from handlers import routers_list
from monitoring_database import monitoring_database

async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Перезапустить бота 🤖"),
    ]
    await bot(SetMyCommands(commands=commands))

for middleware in middlewares_message_list:
    dp.message.middleware(middleware)

for middleware in middlewares_query_list:
    dp.callback_query.middleware(middleware)

dp.include_routers(*routers_list)

async def on_startup():
    asyncio.create_task(monitoring_database(bot))  # Run background parsing task
    logging.info("🚀 Background task started!")

async def main():
    dp.startup.register(on_startup)
    
    await dp.start_polling(bot)
    await set_bot_commands()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    asyncio.run(main())


