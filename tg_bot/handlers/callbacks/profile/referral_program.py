
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.deep_linking import create_start_link
from constants import GIF 
from keyboards.inline import back_to_referrer_program, profile_kb, referral_program_kb
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from create_bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


@router.callback_query(F.data == "referral program")
async def referral_program(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await init_pool()
    telegram_id = query.from_user.id
    sql_query = """
        SELECT 
        u.referrer_balance,
            COUNT(u2.telegram_id) AS referral_count
        FROM users u
        LEFT JOIN users u2 on u.telegram_id = u2.referrer_id
        WHERE u.telegram_id = $1
        GROUP BY u.referrer_balance;
    """
    data = await fetch_db_data(sql_query, (telegram_id,))
    
    referrer_balance = data["referrer_balance"]
    referral_count = data["referral_count"]

    referrer_link = await create_start_link(bot, str(telegram_id), encode=True)

    caption = f"""
<b>🪬 Профиль ⌵
    👥 Реферальная программа

📩 Ваша реферальная ссылка
   ┗  [  <code>{referrer_link}</code>  ]

<blockquote>👬 Ваших рефералов: <em>{referral_count}</em>
🎁 Ваш реферальный баланс: <em>{referrer_balance}$</em></blockquote>

❓ Что я получу, если приведу реферала?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                         
❗ 10% от каждого пополнения баланса реферала с возможностью вывода из бота

✨ Минимальная сумма вывода: <em>3$</em></b>
"""
    await query.message.edit_caption(
        caption=caption,
        reply_markup=referral_program_kb(),
        parse_mode="HTML"
    )

    await close_pool()

@router.callback_query(F.data == "withdraw referrer balance")
async def withdraw_referrer_balance(query: CallbackQuery):
    await query.answer()
    await query.message.answer(
        "❗<b>Вывод баланса на CryptoBot временно через саппорта бота (указан в описании)</b>",
        parse_mode="HTML"
    )


