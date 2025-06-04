from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import admin_kb, admin_main_kb, main_kb, banwords_kb, scrapper_links_kb, settings_section_kb, subscription_section_kb 
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from constants import ADMINS

router = Router()


@router.callback_query(F.data == "back to admin panel section")
async def back_to_admin_panel(query: CallbackQuery, state:FSMContext):
    await state.clear()
    await query.message.edit_caption(
        caption=" ",
        reply_markup=admin_kb()
    )

@router.callback_query(F.data == "back to menu")
async def back_to_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    telegram_id = query.from_user.id
    caption = '>>>💬 *Парсер запускается автоматически после:*\n\n>>>*1\)* _Пополнения баланса и приобретения подписки в разделе_ "*💸 Подписка*"\n\n>>>*2\)* _Изменения конфигурации парсера в разделе_ "*🛠 Настройки*"\n\n'
    await query.message.edit_caption(
        caption=caption,
        reply_markup=main_kb() if telegram_id not in ADMINS else admin_main_kb(),
        parse_mode="MarkdownV2"
    )

@router.callback_query(F.data == "back to categories section")
async def back_to_categories(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=scrapper_links_kb()
    )

@router.callback_query(F.data == "back to settings section")
async def back_to_settings_section(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await init_pool()
    telegram_id = query.from_user.id
    sql_query = """
        SELECT min_price, max_price, min_view_count, max_view_count
        FROM user_preferences
        WHERE telegram_id = $1
    """
    data = await fetch_db_data(sql_query, (telegram_id,))

    if data:
        min_price = int(data[0])
        max_price = int(data[1])
        min_view_count = int(data[2])
        max_view_count = int(data[3])

        await query.message.edit_caption(
            caption=" ",
            reply_markup=settings_section_kb(min_price, max_price, min_view_count, max_view_count)
        )
    await close_pool()

@router.callback_query(F.data == "back to banwords section")
async def back_to_settings(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=banwords_kb()
    )


@router.callback_query(F.data == "back to subscription section")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=subscription_section_kb()
        )


@router.callback_query(F.data == "step back(CryptoBot/USDT/)") 
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=main_kb()
        )


@router.callback_query(F.data == "step back(CryptoBot/USDT/ammounts/)")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=main_kb()()
        )


@router.callback_query(F.data == "step back(CryptoBot/USDT/ammounts/payment)")
async def subscription_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption=" ",
        reply_markup=main_kb()()
        )
