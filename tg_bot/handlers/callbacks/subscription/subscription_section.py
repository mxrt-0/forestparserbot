from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.inline import subscription_section_kb, select_cryptocurrency_kb, select_payment_method_kb, select_payment_amount_kb, payment_transaction_kb
from constants import GIF 

from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, execute_db_query

router = Router()

@router.callback_query(F.data == "subscription section")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=subscription_section_kb()
        )
