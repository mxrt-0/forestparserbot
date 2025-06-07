from aiogram import F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from bot.settings import get_settings
from bot.bot import router, bot
from bot.keyboards.inline import kl1_menu_kb
from bot.states.kl1 import kl1_main_caption

cfg = get_settings()


@router.callback_query(F.data == "kl1")
async def choose_kl1(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await query.message.edit_caption(
        caption=kl1_main_caption(data),
        reply_markup=kl1_menu_kb(data)
    )


