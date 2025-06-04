from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import balance_success_kb, subscription_section_kb, select_cryptocurrency_kb, select_payment_method_kb, select_payment_amount_kb, payment_transaction_kb, profile_kb
from payment_systems.CryptoBotAPI import create_invoice, invoice_status 
from database.db import init_pool, close_pool, execute_db_query

router = Router()

@router.callback_query(F.data == "subscription section")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=subscription_section_kb(),
        parse_mode="MarkdownV2"
        )


@router.callback_query(F.data == "top up balance")
async def top_up_balance(query: CallbackQuery):
    await query.message.edit_caption(
        caption="💸 *Выберите споособ пополнения:*",
        reply_markup=select_payment_method_kb(),
        parse_mode="MarkdownV2"
        )



@router.callback_query(F.data == "CryptoBot")
async def select_cryptocurrency(query: CallbackQuery):
    await query.message.edit_caption(
        caption="💸 *Выберите валюту:*",
        reply_markup=select_cryptocurrency_kb(),
        parse_mode="MarkdownV2"
        )


@router.callback_query(F.data == "USDT") 
async def select_payment_amount(query: CallbackQuery): 
    await query.message.edit_caption(
        caption="💸 *Выберите сумму пополнения:*",
        reply_markup=select_payment_amount_kb(),
        parse_mode="MarkdownV2"
        )


@router.callback_query(F.data.startswith("amount_")) 
async def payment_confirmation(query: CallbackQuery): 
    amount_str = query.data.replace("amount_", "").replace("$", "")
    amount_float = float(amount_str)
    telegram_id = query.from_user.id
    await query.message.edit_caption(
        caption=f'🎯 *Вы выбрали сумму:* {amount_str}*$*\n\n*Для оплаты счёта нажмите на*\n*"💸 Оплатить счёт"*\n\n*После оплаты нажмите на*\n*"♻️Проверить платеж"*',
        reply_markup= await payment_transaction_kb(amount_float, telegram_id, create_invoice),
        parse_mode="MarkdownV2"
        )

    

@router.callback_query(F.data.startswith("inv_")) 
async def handle_subscription_query(query: CallbackQuery): 
    payment_info = query.data.split(",")
    invoice_id = int(payment_info[1])
    print(payment_info, invoice_id)
    status = await invoice_status(invoice_id)
    if status == "paid":
        amount = float(payment_info[3])
        telegram_id = int(payment_info[4].strip())
        await init_pool()
        sql_query = """
            WITH user_referrer AS (
                SELECT referrer_id 
                FROM users 
                WHERE telegram_id = $2  
            )
            UPDATE users
            SET 
                balance = CASE
                    WHEN telegram_id = $2 THEN balance + $1 
                    ELSE balance  
                END,
                overall_balance = CASE
                    WHEN telegram_id = $2 THEN overall_balance + $1 
                    ELSE overall_balance 
                END,
                referrer_balance = CASE
                    WHEN telegram_id = (SELECT referrer_id FROM user_referrer) 
                    AND (SELECT referrer_id FROM user_referrer) != 0 
                    THEN referrer_balance + ($1 * 0.1)  
                    ELSE referrer_balance 
                END
            WHERE telegram_id IN ($2, (SELECT referrer_id FROM user_referrer));  
        """

        await execute_db_query(sql_query, (amount, telegram_id))
        await close_pool()
        await query.message.edit_caption(
            caption="🎉 *Счет успешно пополнен\!*",
            reply_markup=balance_success_kb(),
            parse_mode="MarkdownV2"
        )
