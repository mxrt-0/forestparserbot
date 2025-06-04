from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import banwords_kb, back_to_settings_kb, retry_banwords_kb, scrapper_links_kb, auto_bike_boat_kb, settings_section_kb, tickets_admission_kb, electronics_kb, family_children_baby_kb, leisure_hobby_neighborhood_kb, home_garden_kb, pets_kb, fashion_beauty_kb, music_movies_books_kb
from constants import GIF, AD_SECTIONS 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import bot

router = Router()

class Banwords(StatesGroup):
    banwords = State()
    chat_id = State()
    message_id = State()

@router.callback_query(F.data.in_(
    [ 
        "banwords",
        "change banwords again",
        "delete banwords"
    ]
    
)) 
async def banwords(query: CallbackQuery, state: FSMContext):
    await state.set_state(Banwords.banwords)
    await state.update_data(message_id=query.message.message_id)
    await state.update_data(chat_id=query.message.chat.id)
    await init_pool()

    telegram_id = query.from_user.id
    
    if query.data == "delete banwords":
        sql_query = """
            UPDATE user_preferences
            SET banwords = NULL 
            WHERE telegram_id = $1
            RETURNING banwords;
        """  
    else:
        sql_query = """
            SELECT banwords
            FROM user_preferences
            WHERE telegram_id = $1
        """  

    data = await fetch_db_data(sql_query, (telegram_id,))

    if data["banwords"]:
        banwords = data["banwords"]
        banwords_list = banwords.split(",")
        banwords_in_column = "\n".join([banword.strip() for banword in banwords_list])

        caption = f"✏️ *Введите новые банворды построчно:*\n\n📝 *Текущие банворды:*\n\n```\n{banwords_in_column}\n```"
        await query.message.edit_caption(
            caption=caption,
            reply_markup=banwords_kb(),
            parse_mode="MarkdownV2"
        ) 

        await close_pool()
    else:
        caption = f"✏️ *Введите новые банворды построчно:*\n\n📝 *Текущие банворды:* ❌"
        await query.message.edit_caption(
            caption=caption,
            reply_markup=back_to_settings_kb(),
            parse_mode="MarkdownV2"
        )

@router.message(Banwords.banwords)
async def handle_banwords(message: Message, state: FSMContext):
    telegram_id = message.from_user.id

    user_data = await state.get_data()
    message_id = user_data.get("message_id")
    chat_id = user_data.get("chat_id")

    await init_pool()
    new_banwords = message.text

    if new_banwords:
        new_banwords_list = [word.strip() for word in (new_banwords or "").split('\n') if word.strip()]
        await state.update_data(banwords=new_banwords_list)
        await state.set_state(Banwords.banwords)
        update_query = """
            UPDATE user_preferences
            SET banwords = $1
            WHERE telegram_id = $2
            RETURNING banwords;
        """
        data = await fetch_db_data(update_query, (" ,".join(new_banwords_list), telegram_id))

        banwords = data["banwords"]
        banwords_list = banwords.split(",")
        banwords_in_column = "\n".join([banword.strip() for banword in banwords_list])

        caption = f"✅ *Банворды изменены*\n\n📝 *Текущие банворды:*\n\n```\n{banwords_in_column}\n```"
        await bot.edit_message_caption(
            message_id=message_id,
            chat_id=chat_id,
            caption=caption,
            reply_markup=retry_banwords_kb(),
            parse_mode="MarkdownV2"
        )
        await message.delete()
        await state.clear()
        await close_pool()

    
