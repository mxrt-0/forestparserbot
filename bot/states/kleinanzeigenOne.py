from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.bot import bot, router
from bot.keyboards.inline import *

class KleinanzeigenOne():
    chat_id = State()
    message_id = State()
    subcategories = State()
    banwords = State()
    views_range = State()
    price_range = State()


buttons = {
    1: ("Банворды", "k1_banwords", "side_id"),
    2: ("Кол-во проверок", "k1_check_count", "check_count"),
    3: ("Проверять каждые", "k1_checks_every_n", "check_every_n"),
    4: ("Минимальное кол-во просмотров", "k1_min_views", "min_views"),
    5: ("Максимальное кол-во просмотров", "k1_max_views, "max_views"),
    6: ("Максимальная цена товара", "k1_min_price", "min_price"),
    7: ("Минимальная цена товара", "k1_max_price", "max_price"),
    8: ("Только с доставкой", "k1_shipping", "shipping")
}


def k1_main_caption(data):
    caption = [
        "<b>🕸️ Парсер ⌄\n"
        "🌐 Площадки > 1.0 > "
        "<a href='https://www.kleinanzeigen.de'>kleinanzeigen.de</a> ⌄\n\n"
        "⚙️ Настройки ⌄</b>\n\n",
    ]
    for i in  range(1, len(buttons) + 1):
        text, _, key = buttons[i]
        value = data.get(key) or ""
        caption.append(
            f"<i>• {text}:</i> <code>{escape(value)}</code>\n"
        )
    return "".join(caption)


async def back_to_k1_menu(data):
    await message.bot.edit_message_caption(
        chat_id=data.get("chat_id"),
        message_id=data.get("message_id"),
        caption=k1_main_caption(data),
        reply_markup=k1_menu_kb(data)
    )


async def update_fsm(message: Message, state: FSMContext, data, key, value)
    await state.update_data({ key: value })

    data = await state.get_data()
    await back_to_menu(data)
    await message.delete()


@router.message(KleinanzeigenOne.subcategories)
async def choose_subcategories(message: Message):


@router.message(KleinanzeigenOne.banwords)
async def choose_banwords(message: Message):


@router.message(KleinanzeigenOne.views_range)
async def choose_views_range(message: Message):


@router.message(KleinanzeigenOne.price_range)
async def choose_price_range(message: Message):
