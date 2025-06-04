from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from create_bot import bot
from aiogram.enums import ContentType, ChatMemberStatus
from typing import Callable, Awaitable, Dict, Any
from keyboards.inline import channels_kb
from constants import GIF
from database.db import init_pool, close_pool, execute_db_query


class CheckSubscription(BaseMiddleware):
    def __init__(self, REQUIRED_CHANNELS) -> None: 
        self.required_channels = REQUIRED_CHANNELS
        
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            telegram_id = event.from_user.id
            
            missing_channels = []
            for channel_data in self.required_channels:
                channel_label = channel_data.get("label")
                channel_url =channel_data.get("url")
                channel_id = channel_data.get("id")
                    
                member = await event.bot.get_chat_member(chat_id=channel_id, user_id=telegram_id)
                if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                    missing_channels.append({"label": channel_label, "url": channel_url, "id": channel_id})
            
            
            if missing_channels:
                if len(missing_channels) == 1:
                    await bot.send_animation(
                        chat_id=telegram_id,
                        animation=GIF,
                        caption="🔐 *Подпишитесь на канал, чтобы получить доступ к  функционалу бота:*",
                        reply_markup=channels_kb(missing_channels),
                        parse_mode="MarkdownV2"
                    )
                else:
                    await bot.send_animation(
                        chat_id=telegram_id,
                        animation=GIF,
                        caption="🔐 *Подпишитесь на каналы, чтобы получить доступ к функционалу бота*",
                        reply_markup=channels_kb(missing_channels),
                        parse_mode="MarkdownV2"
                    )
                result = None
            else:
                result = await handler(event, data)
            await close_pool()
            return result 
        except Exception as e:
            print(f"Exception: {e}")


class CheckUsername(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            username = event.from_user.username
            if username:
                result = await handler(event, data)
            else:
                await event.answer(
                    "❗ <b>Установите @username для продолжения взаимодействия с ботом</b>",
                    parse_mode="HTML")
                result = None

            return result 
        except Exception as e:
            print(f"Exception: {e}")


class CheckUsernameQuery(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            username = event.from_user.username
            if username:
                result = await handler(event, data)
            else:
                await event.answer()
                await event.message.answer(
                    "❗ <b>Установите @username для продолжения взаимодействия с ботом</b>",
                    parse_mode="HTML")
            await close_pool()
            return result 
        except Exception as e:
            print(f"Exception: {e}")

class CheckSubscriptionQuery(BaseMiddleware):
    def __init__(self, REQUIRED_CHANNELS) -> None: 
        self.required_channels = REQUIRED_CHANNELS
        
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        telegram_id = event.from_user.id
        try:
            missing_channels = []
            for channel_data in self.required_channels:
                channel_label = channel_data.get("label")
                channel_url =channel_data.get("url")
                channel_id = channel_data.get("id")
                    
                member = await event.bot.get_chat_member(chat_id=channel_id, user_id=telegram_id)
                if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                    missing_channels.append({"label": channel_label, "url": channel_url, "id": channel_id})
            
            
            if missing_channels:
                if len(missing_channels) == 1:
                    await bot.send_animation(
                        chat_id=telegram_id,
                        animation=GIF,
                        caption="🔐 *Подпишитесь на канал, чтобы получить доступ к  функционалу бота:*",
                        reply_markup=channels_kb(missing_channels),
                        parse_mode="MarkdownV2"
                    )
                else:
                    await bot.send_animation(
                        chat_id=telegram_id,
                        animation=GIF,
                        caption="🔐 *Подпишитесь на каналы, чтобы получить доступ к функционалу бота*",
                        reply_markup=channels_kb(missing_channels),
                        parse_mode="MarkdownV2"
                    )
                result = None
            else:
                result = await handler(event, data)
            return result 
        except Exception as e:
            print(f"Exception: {e}")
#
class UpdateUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            telegram_id = event.from_user.id
            username = event.from_user.username
            sql_query = """
                INSERT INTO users (telegram_id, username)
                VALUES ($1, $2)
                ON CONFLICT (telegram_id)
                DO UPDATE SET
                    username = CASE 
                        WHEN users.username IS DISTINCT FROM EXCLUDED.username
                        THEN EXCLUDED.username
                        ELSE users.username
                    END,
                    registration_data = CASE
                        WHEN users.registration_data IS NULL
                        THEN NOW()
                        ELSE users.registration_data
                    END;
            """
            await init_pool()
            await execute_db_query(sql_query, (telegram_id, username))
            await close_pool()

            return await handler(event, data)

        except Exception as e:
            print(f"Exception: {e}")

