import typing_extensions
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.bot import bot, router
from bot.keyboards.inline import kl1_menu_kb

class KleinanzeigenOne(StatesGroup):
    chat_id = State()
    message_id = State()
    banwords = State()
    min_view_count = State()
    max_view_count = State()
    min_price = State()
    max_price = State()


buttons = {
    1: ("Банворды", "kl1_banwords", "side_id"),
    2: ("Кол-во проверок", "kl1_check_count", "check_count"),
    3: ("Проверять каждые", "kl1_checks_every_n", "check_every_n"),
    4: ("Минимальное кол-во просмотров", "kl1_min_views", "min_views"),
    5: ("Максимальное кол-во просмотров", "kl1_max_views", "max_views"),
    6: ("Минимальная цена товара", "kl1_max_price", "max_price"),
    7: ("Максимальная цена товара", "kl1_min_price", "min_price"),
    8: ("Только с доставкой", "kl1_shipping", "shipping")
}


def kl1_main_caption(data):
    caption = [
        "<b>🕸️ Парсер ⌄\n"
        "🧭 Направление — 1.0 ⌄\n"
        "🌐 Площадка — "
        "<a href='https://www.kleinanzeigen.de'>kleinanzeigen.de</a> ⌄\n\n"
        "⚙️ Настройки ⌄</b>\n",
    ]
    for i in  range(1, len(buttons) + 1):
        text, _, key = buttons[i]
        value = data.get(key) or ""
        caption.append(
            f"<i>• {text}:</i> <code>{escape(value)}</code>\n"
        )
    return "".join(caption)


async def back_to_kl1_menu(data):
    await bot.edit_message_caption(
        chat_id=data.get("chat_id"),
        message_id=data.get("message_id"),
        caption=kl1_main_caption(data),
        reply_markup=kl1_menu_kb(data)
    )


async def update_fsm(message: Message, state: FSMContext, key, value):
    await state.update_data({ key: value })

    data = await state.get_data()
    await back_to_kl1_menu(data)
    await message.delete()



@router.message(KleinanzeigenOne.banwords)
async def choose_banwords(message: Message, state: FSMContext):
    pass


@router.message(KleinanzeigenOne.min_view_count)
async def choose_min_view_count(message: Message, state: FSMContext):
    value = message.text
    data = state.get_data()
    max_view_count = data.get("max_view_count", 0)
    if value.isdigit() and int(max_view_count) > int(value):
        await update_fsm(message, state, "min_view_count", value)

@router.message(KleinanzeigenOne.max_view_count)
async def choose_max_view_count(message: Message, state: FSMContext):
    pass

@router.message(KleinanzeigenOne.min_price)
async def choose_min_price(message: Message, state: FSMContext):
    pass


@router.message(KleinanzeigenOne.max_price)
async def choose_max_price(message: Message, state: FSMContext):
    pass
