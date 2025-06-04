from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import  scrapper_links_kb, settings_section_kb, select_cryptocurrency_kb, select_payment_method_kb, select_payment_amount_kb, payment_transaction_kb
from constants import GIF 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, execute_db_query, fetch_db_data

router = Router()

@router.callback_query(F.data == "settings section")
async def settings_section(query: CallbackQuery):
    await init_pool()
    telegram_id = query.from_user.id
    sql_query = """
        SELECT min_price, max_price, min_view_count, max_view_count
        FROM user_preferences
        WHERE telegram_id = $1;
    """
    data = await fetch_db_data(sql_query, (telegram_id,))

    if data:
        min_price = int(data[0])
        max_price = int(data[1])
        min_view_count = int(data[2])
        max_view_count = int(data[3])

        await query.message.edit_caption(
            caption = """
🔐 Неизменяемые настройки ⌵
   
┣ 📦 *Доставка:* 
┃   ┗╾ _только с доставкой_
┣ 💵 *Мин\. цена товара:* 
┃   ┗╾ _от 100_
┣ 👀 *Мин\. просмотров за час:* 
┃   ┗╾ _от 10_      
┗ 📜 *Страниц на категорию\/подкатегорию:*
     ┗╾ _50_
            """,
            reply_markup=settings_section_kb(min_price, max_price, min_view_count, max_view_count),
            parse_mode="MarkdownV2"

        )

    await close_pool()




