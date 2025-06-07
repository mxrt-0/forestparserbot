from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from bot.bot import router
from bot.settings import get_settings
from bot.keyboards.inline import menu_kb, admin_menu_kb

cfg = get_settings()


def start_caption(chat_id, balance):
    return (
        "<b>❗Меню @forestscrpaperbot\n\n</b>"
        "🕸️ <i>Данный сервис предназначен для легального сбора информации с разного рода сайтов и маркетплейсов.</i>\n\n"
        f"<b>💰: </b><code>{balance}$</code>\n"
        f"<b>🆔: </b><code>{chat_id}</code>"
    )


@router.message(CommandStart())
async def start(message: Message):
    caption = start_caption(chat_id=message.from_user.id, balance=0)
    reply_markup = admin_menu_kb() if message.from_user.id in cfg.ADMINS else menu_kb()
    await message.answer_photo(
        photo=cfg.BOT_PHOTO, caption=caption, reply_markup=reply_markup
    )


@router.callback_query(F.data == "menu")
async def menu(query: CallbackQuery):
    caption = start_caption(chat_id=query.from_user.id, balance=0)
    reply_markup = admin_menu_kb() if query.from_user.id in cfg.ADMINS else menu_kb()
    await query.message.edit_caption(caption=caption, reply_markup=reply_markup)
