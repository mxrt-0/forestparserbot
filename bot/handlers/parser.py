from aiogram import F
from aiogram.types import CallbackQuery

from bot.bot import router
from bot.keyboards.inline import choose_direction_kb, first_direction_kb, second_direction_kb


@router.callback_query(F.data == "parser")
async def choose_kl1(query: CallbackQuery):
    await query.message.edit_caption(
        caption=(
            "<b>🕸️ Парсер ⌄\n\n"
            "Выберите направление:</b>"
        ),
        reply_markup=choose_direction_kb()
    )


@router.callback_query(F.data == "first_direction")
async def choose_first_direction(query: CallbackQuery):
    await query.message.edit_caption(
        caption =(
            "<b>🕸️ Парсер  ⌄\n"
            "🧭 Направление — 1.0 ⌄\n\n"
            "Выберите площадку:</b>"
        ),
        reply_markup=first_direction_kb()
    )


@router.callback_query(F.data == "second_direction")
async def choose_second_direction(query: CallbackQuery):
    await query.message.edit_caption(
        caption =(
            "<b>🕸️ Парсер  ⌄\n"
            "🧭 Направление — 2.0 ⌄\n\n"
            "Выберите площадку:</b>"
        ),
        reply_markup=second_direction_kb()
    )
