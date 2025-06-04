from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode
from aiogram.utils.deep_linking import decode_payload

from constants import GIF
from keyboards.inline import admin_main_kb, main_kb
from database.db import fetch_db_data, init_pool, close_pool, execute_db_query
from constants import ADMINS

router = Router()

@router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    await init_pool()
    telegram_id = message.from_user.id
    username = message.from_user.username
    if command.args:
        referrer_id = int(decode_payload(command.args))
        check_query = """
            SELECT EXISTS (
                SELECT telegram_id
                FROM users
                WHERE telegram_id = $1
            )
        """
        data = await fetch_db_data(check_query, (referrer_id,))

        if not data:
            referrer_id = 0
            await message.answer("Такой реферальной ссылки не существует")

    else:
        referrer_id = 0
    
    users_query = """
        INSERT INTO users (telegram_id, referrer_id, username)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id) DO UPDATE 
        SET username = CASE 
            WHEN users.username IS DISTINCT FROM EXCLUDED.username 
            THEN EXCLUDED.username
            ELSE users.username
        END;
    """
    user_preferences_query = """ 
        INSERT INTO user_preferences (telegram_id)
        VALUES ($1)
        ON CONFLICT (telegram_id)
        DO NOTHING; 
    """

    await execute_db_query(users_query, (telegram_id, referrer_id, username))
    await execute_db_query(user_preferences_query, (telegram_id,))

    caption = '>>>💬 *Парсер запускается автоматически после:*\n\n>>>*1\)* _Пополнения баланса и приобретения подписки в разделе_ "*💸 Подписка*"\n\n>>>*2\)* _Изменения конфигурации парсера в разделе_ "*🛠 Настройки*"\n\n'
    await message.answer_animation(
        animation=GIF, 
        caption=caption, 
        reply_markup=main_kb() if telegram_id not in ADMINS else admin_main_kb(),
        parse_mode="MarkdownV2"
    )


