
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import back_to_settings_kb, choose_between_views_kb, retry_view_count_kb, banwords_kb, retry_banwords_kb, scrapper_links_kb, auto_bike_boat_kb, settings_section_kb, tickets_admission_kb, electronics_kb, family_children_baby_kb, leisure_hobby_neighborhood_kb, home_garden_kb, pets_kb, fashion_beauty_kb, music_movies_books_kb
from constants import GIF, AD_SECTIONS 
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import bot

router = Router()

class ViewCount(StatesGroup):
    view_count = State()
    view_count_type = State()
    chat_id = State()
    message_id = State()

@router.callback_query(F.data == "change view count")
async def change_view_count(query: CallbackQuery):
    caption = f"🎯 *Выберите, что желаете изменить:*"
    await query.message.edit_caption(
        caption=caption,
        reply_markup=choose_between_views_kb(),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data.in_(
    [
        "change min view count",
        "change max view count",
    ]
))
async def view_count(query: CallbackQuery, state: FSMContext):
    data = query.data 
    if data == "change min view count": 
        await state.update_data(view_count_type="min")
        caption=f"✏️ *Введите минимальное количество просмотров за час:*\n\n📋 *Пример: 30*"
    elif data == "change max view count":
        await state.update_data(view_count_type="max")
        caption=f"✏️ *Введите максимальное количество просмотров за час:*\n\n📋 *Пример: 100*"

    await state.set_state(ViewCount.view_count)
    await state.update_data(message_id=query.message.message_id)
    await state.update_data(chat_id=query.message.chat.id)

    await query.message.edit_caption(
        caption=caption,
        reply_markup=back_to_settings_kb(),
        parse_mode="MarkdownV2",
    )

@router.message(ViewCount.view_count)
async def handle_view_count(message: Message, state: FSMContext):
    
    await init_pool()

    user_data = await state.get_data()
    view_count_type = user_data.get("view_count_type")
    message_id = user_data.get("message_id")
    chat_id = user_data.get("chat_id")   

    if view_count_type == "min":
        min_view_count = message.text
    elif view_count_type == "max":
        max_view_count = message.text
    
    if view_count_type == "min":

        if 32767 >= int(min_view_count) >= 10:
            sql_query = """
                SELECT max_view_count
                FROM user_preferences
                WHERE telegram_id = $1
            """
            data = await fetch_db_data(sql_query, (chat_id,))
            
            if data:
                
                if data["max_view_count"] >= int(min_view_count):
                    update_query = """
                        UPDATE user_preferences
                        SET min_view_count = $1
                        WHERE telegram_id = $2
                    """
                    await execute_db_query(update_query, (int(min_view_count), chat_id))

                    caption = "✅ *Минимальное количество просмотров за час обновлено*\n\n🎯 *Выберите действие:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_view_count_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()
                else:
                    caption = "❌ *Введите значение минимального количества просмотров меньшее или равное максимальному\!*\n\n🎯 *Выберите действиe:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_view_count_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()

        else:
            caption = "❌ *Минимальная количество просмотров не может быть ниже 10*\!\n\n🎯 *Выберите действиe:*" 
            await bot.edit_message_caption(
                message_id=message_id,
                chat_id=chat_id,
                caption=caption,
                reply_markup=retry_view_count_kb(),
                parse_mode="MarkdownV2"
            )
            await state.clear()
    


    elif view_count_type == "max":

        if 32767 >= int(max_view_count):
            sql_query = """
                SELECT min_view_count
                FROM user_preferences
                WHERE telegram_id = $1
            """
            data = await fetch_db_data(sql_query, (chat_id,))
            
            if data:
                
                if int(max_view_count) >= data["min_view_count"]:
                    update_query = """
                        UPDATE user_preferences
                        SET max_view_count = $1
                        WHERE telegram_id = $2
                    """
                    await execute_db_query(update_query, (int(max_view_count), chat_id))

                    caption = "✅ *Максимальное количество просмотров за час обновлено*\n\n🎯 *Выберите действие:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_view_count_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()

                
                else:
                    caption = "❌ *Введите значение максимального количества просмотров большее или равное максимальному\!*\n\n🎯 *Выберите действиe:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_view_count_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()
        else:
            caption = "❌ *Введите максимальное количество просмотров меньше 32767\!*\n\n🎯 *Выберите действиe:*" 
            await bot.edit_message_caption(
                message_id=message_id,
                chat_id=chat_id,
                caption=caption,
                reply_markup=retry_view_count_kb(),
                parse_mode="MarkdownV2"
            )
            await state.clear()

    await message.delete()
    await state.clear()
    await close_pool()

