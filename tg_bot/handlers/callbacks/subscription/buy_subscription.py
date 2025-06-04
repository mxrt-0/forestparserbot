from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from constants import GIF 
from keyboards.inline import buy_subscription_kb, profile_kb, top_up_balance_redirect_kb, main_kb
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query

router = Router()


@router.callback_query(F.data == "buy subscription")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption="*✏️ Выберите опцию:*",
        reply_markup=buy_subscription_kb(),
        parse_mode="MarkdownV2"
    )


@router.callback_query(F.data.startswith("d_"))
async def subscription_section(query: CallbackQuery):
    subscription_details = query.data.replace("d_", "").replace("price_", "").split(",")
    rent_time = int(subscription_details[0])
    price = int(subscription_details[1])
    telegram_id = query.from_user.id
    check_balance_query = """
        SELECT balance
        FROM users
        WHERE telegram_id = $1
    """
    await init_pool()
    balance = await fetch_db_data(check_balance_query, (telegram_id,), target="row")


    if not balance[0] or balance[0] < price:
        await query.message.edit_caption(
            caption="❌ *Недостаточно средств на балансе, пополните баланс\!*",
            reply_markup=top_up_balance_redirect_kb(),
            parse_mode="MarkdownV2"
        )
        return None


    update_subscription_query = """
        UPDATE users
        SET balance = balance - $1, 
            subscription_time_end = CASE 
                WHEN subscription_time_end >= NOW() 
                THEN subscription_time_end + INTERVAL '1 day' * $2 
                ELSE NOW() + INTERVAL '1 day' * $2 
            END
        WHERE telegram_id = $3 AND balance >= $1 AND balance > 0
        RETURNING balance, subscription_time_end;
    """
    updated_data = await fetch_db_data(update_subscription_query, (price, rent_time, telegram_id))

    
    if updated_data:
        updated_balance = updated_data['balance']
        updated_subscription_time_end = updated_data['subscription_time_end']
        await query.message.edit_caption(
            caption=f"🎉 *Подписка приобретена\!*",
            reply_markup=profile_kb(),
            parse_mode="MarkdownV2"
        )
    else:
        await query.message.edit_caption(
            caption="❌ *Что\-то пошло не так, попробуйте снова\!*",
            reply_markup=profile_kb(),
            parse_mode="MarkdownV2"
        )

    await close_pool()
