from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import back_to_settings_kb, banwords_kb, choose_between_prices_kb, retry_banwords_kb, retry_max_price_kb, retry_min_price_kb, scrapper_links_kb, auto_bike_boat_kb, settings_section_kb, tickets_admission_kb, electronics_kb, family_children_baby_kb, leisure_hobby_neighborhood_kb, home_garden_kb, pets_kb, fashion_beauty_kb, music_movies_books_kb
from constants import GIF, AD_SECTIONS 
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import bot

router = Router()

class Price(StatesGroup):
    price = State()
    price_type = State()
    chat_id = State()
    message_id = State()


@router.callback_query(F.data == "change price")
async def price_choose(query: CallbackQuery, state: FSMContext):
    caption = f"🎯 *Выберите, что желаете изменить:*"
    await query.message.edit_caption(
        caption=caption,
        reply_markup=choose_between_prices_kb(),
        parse_mode="MarkdownV2",
    )

@router.callback_query(F.data.in_(
    [
        "change min price",
        "change max price",
    ]
))
async def change_price(query: CallbackQuery, state: FSMContext):
    await state.set_state(Price.price)
    await state.update_data(message_id=query.message.message_id)
    await state.update_data(chat_id=query.message.chat.id)

    data = query.data 
    if data == "change min price": 
        await state.update_data(price_type="min")
        caption=f"✏️ *Введите минимальную цену:*\n\n📋 *Пример: 200*"
    elif data == "change max price":
        await state.update_data(price_type="max")
        caption=f"✏️ *Введите максимальную цeну:*\n\n📋 *Пример: 5000*"


    await query.message.edit_caption(
        caption=caption,
        reply_markup=back_to_settings_kb(),
        parse_mode="MarkdownV2",
    )

@router.message(Price.price)
async def handle_price_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    price_type = user_data.get("price_type")
    chat_id = user_data.get("chat_id")   
    message_id = user_data.get("message_id")

    await init_pool()

    if price_type == "min":
        min_price = message.text
    elif price_type == "max":
        max_price = message.text
    
    if price_type == "min":

        if 32767 >= int(min_price) >= 100:
            sql_query = """
                SELECT max_price
                FROM user_preferences
                WHERE telegram_id = $1
            """
            data = await fetch_db_data(sql_query, (chat_id,))
            
            if data:
                
                if data["max_price"] >= int(min_price):
                    update_query = """
                        UPDATE user_preferences
                        SET min_price = $1
                        WHERE telegram_id = $2
                    """
                    await execute_db_query(update_query, (int(min_price), chat_id))

                    caption = "✅ *Минимальная цена обновлена*\n\n🎯 *Выберите действие:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_min_price_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()
                else:
                    caption = "❌ *Введите значение минимальной цены меньшее или равное максимальной\!*\n\n🎯 *Выберите действиe:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_min_price_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()

        else:
            caption = "❌ *Минимальная ценa не может быть ниже 100 и больше 32767*\!\n\n🎯 *Выберите действиe:*" 
            await bot.edit_message_caption(
                message_id=message_id,
                chat_id=chat_id,
                caption=caption,
                reply_markup=retry_min_price_kb(),
                parse_mode="MarkdownV2"
            )
            await state.clear()
    


    elif price_type == "max":

        if 32767 >= int(max_price):
            sql_query = """
                SELECT min_price
                FROM user_preferences
                WHERE telegram_id = $1
            """
            data = await fetch_db_data(sql_query, (chat_id,))
            
            if data:
                
                if int(max_price) >= data["min_price"]:
                    update_query = """
                        UPDATE user_preferences
                        SET max_price = $1
                        WHERE telegram_id = $2
                    """
                    await execute_db_query(update_query, (int(max_price), chat_id))

                    caption = "✅ *Максимальная цена обновленa*\n\n🎯 *Выберите действие:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_max_price_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()

                
                else:
                    caption = "❌ *Введите значение максимальной цены большее или равное минимальной\!*\n\n🎯 *Выберите действиe:*" 
                    await bot.edit_message_caption(
                        message_id=message_id,
                        chat_id=chat_id,
                        caption=caption,
                        reply_markup=retry_max_price_kb(),
                        parse_mode="MarkdownV2"
                    )
                    await state.clear()
        else:
            caption = "❌ *Введите максимальную цену меньше 32767\!*\n\n🎯 *Выберите действиe:*" 
            await bot.edit_message_caption(
                message_id=message_id,
                chat_id=chat_id,
                caption=caption,
                reply_markup=retry_max_price_kb(),
                parse_mode="MarkdownV2"
            )
            await state.clear()

    await message.delete()
    await state.clear()
    await close_pool()

