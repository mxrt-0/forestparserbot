from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import  balance_success_kb
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query

router = Router()

@router.callback_query(F.data == "parser section")
async def parser_section(query: CallbackQuery):
    await init_pool()
    telegram_id = query.from_user.id
    sql_query = """
        SELECT subscription_time_end
        FROM users
        WHERE telegram_id = $1
        AND subscription_time_end > NOW();
    """
    data = await fetch_db_data(sql_query, (telegram_id,))
    if data:
        text = "♻️ *Парсер запущен\.\.\. Ожидайте выдачу обьявлений*\n\n❗ *Перезапуск после измения настроек не нужен*"
    else:
        text  = "❌ *Подписка не куплена*"
    await query.answer()
    await query.message.answer(
        text=text,
        parse_mode="MarkdownV2",
    )
    await close_pool()
