from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from constants import GIF 
from keyboards.inline import profile_kb, profile_main_kb
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from create_bot import dp
import re
router = Router()


@router.callback_query(F.data == "profile section")
async def subscription_section(query: CallbackQuery):
    telegram_id = query.from_user.id

    await init_pool() 
    balance_query = """ 
        SELECT balance
        FROM users
        WHERE telegram_id = $1
    """
    balance_data = await fetch_db_data(balance_query, (telegram_id,))
    balance = re.escape(str(balance_data["balance"]))

    time_diff_query = """
        SELECT 
            FLOOR(EXTRACT(EPOCH FROM subscription_time_end - CURRENT_TIMESTAMP) / 86400) || ',' ||
            FLOOR((EXTRACT(EPOCH FROM subscription_time_end - CURRENT_TIMESTAMP) % 86400) / 3600) || ',' ||
            FLOOR((EXTRACT(EPOCH FROM subscription_time_end - CURRENT_TIMESTAMP) % 3600) / 60) 
        AS remaining_time
        FROM users
        WHERE telegram_id = $1;
    """
    time_diff = await fetch_db_data(time_diff_query, (telegram_id,))
    if time_diff[0] is None or not time_diff[0]:
        remaining_subscription_time = "У Вас нет подписки"
    elif time_diff: 
        time_diff_data = time_diff[0].split(",")
        remaining_days = int(time_diff_data[0])
        remaining_hours = int(time_diff_data[1])
        remaining_minutes = int(time_diff_data[2])
        if remaining_days == 0 and remaining_hours == 0 and remaining_minutes == 0:
            remaining_subscription_time = "У Вас нет подписки"
        remaining_subscription_time = f"{remaining_days}д\.{remaining_hours}ч\.{remaining_minutes}м\."
    await close_pool()

    if remaining_subscription_time == "У Вас нет подписки":
        await query.message.edit_caption(
            caption=f"""
🪬 Профиль ⌵
   
┏ 🆔 `{telegram_id}`
┃ 
┣ 🌸 *{remaining_subscription_time}*
┃
┗ 💸 *Ваш текущий баланс*
   ┗╾ _{balance}_*$*
        """,
            reply_markup=profile_main_kb(),
            parse_mode="MarkdownV2"
        )
    else:
        await query.message.edit_caption(
            caption=f"""
🪬 Профиль ⌵
   
┏🆔 `{telegram_id}`
┃ 
┣ 🌸 *Ваше время подписки*
┃  ┗╾ _{remaining_subscription_time}_
┃
┗ 💸 *Ваш текущий баланс*
   ┗╾ _{balance}_*$*
        """,
            reply_markup=profile_main_kb(),
            parse_mode="MarkdownV2"
        )

