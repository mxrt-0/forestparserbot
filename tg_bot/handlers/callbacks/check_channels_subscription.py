from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.inline import main_kb
from constants import REQUIRED_CHANNELS, GIF 
from create_bot import bot
from aiogram.enums import ParseMode
from aiogram.enums import ContentType, ChatMemberStatus

router = Router()

@router.callback_query(F.data == "check_subscription")
async def handle_parser_query(query: CallbackQuery):
    user_id = query.from_user.id
    try:
        missing_channels = []
        for channel_data in REQUIRED_CHANNELS: 
            channel_label = channel_data.get("label") 
            channel_url =channel_data.get("url")
            channel_id = channel_data.get("id")
                    
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                missing_channels.append({"label": channel_label, "url": channel_url, "id": channel_id})
        
        if missing_channels:
            await query.answer()
            await query.answer(chat_id=user_id, text="Вы не подписаны")
        else:
            caption = '>>>💬 *Парсер запускается автоматически после:*\n\n>>>*1\)* _Пополнения баланса и приобретения подписки в разделе_ "*💸 Подписка*"\n\n>>>*2\)* _Изменения конфигурации парсера в разделе_ "*🛠 Настройки*"\n\n'
            await query.answer()
            await query.message.edit_caption(
                #chat_id=user_id, 
                #animation=GIF, 
                caption=caption, 
                reply_markup=main_kb(),
                parse_mode="MarkdownV2"
            )
    except Exception as e:
        print(f"Exception: {e}")
