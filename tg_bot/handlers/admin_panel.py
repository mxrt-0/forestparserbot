from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from keyboards.inline import admin_kb, admin_send_message_kb, admin_user_interaction_kb, back_to_admin_kb, profile_kb
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime 
import logging
logging.basicConfig(level=logging.DEBUG)


router = Router()

class AdminMessage(StatesGroup):
    send_message = State()
    send_message_caption = State()
    message_type = State()
    data_type = State()

class UserInteraction(StatesGroup):
    user_id = State()
    user_id_type = State()
    telegram_id = State()
    message_id = State()
    caption = State()
    action_type = State()
    action = State()

@router.callback_query(F.data == "admin panel")
async def admin_panel(query: CallbackQuery):
        caption = f"⚙️ *Админ панель открыта*\n\n🎯 *Выберите действие:*" 
        await query.message.edit_caption(
            caption=caption,
            reply_markup=admin_kb(),
            parse_mode="MarkdownV2"
        )
    

@router.callback_query(F.data == "open bot statistics")
async def bot_statistics(query: CallbackQuery):
    await init_pool()

    sql_query = """
        SELECT
            (SELECT COUNT(telegram_id) FROM users) AS users_count,
            (SELECT COUNT(subscription_time_end) FROM users 
            WHERE subscription_time_end >= NOW()) AS active_subscriptions,
            (SELECT SUM(overall_balance) FROM users) AS total_balance;
        """
    bot_stats = await fetch_db_data(sql_query)
    if bot_stats:
        users_count = bot_stats["users_count"]
        active_subscriptions = bot_stats["active_subscriptions"]
        total_balance = bot_stats["total_balance"]

        caption = f"⚙️ *Статистика:*\n\n*Всего пользователей:* {users_count}\n*Активных подписок:* {active_subscriptions}\n*Пополнений за все время:* {total_balance}$\n\n🎯 *Выберите действие:*" 
        await query.message.edit_caption(
            caption=caption,
            reply_markup=back_to_admin_kb(),
            parse_mode="MarkdownV2"
        )
    await close_pool()

@router.callback_query(F.data == "interaction with user")
async def user_panel(query: CallbackQuery, state: FSMContext):
    chat_id = query.from_user.id
    message_id = query.message.message_id

    await state.set_state(UserInteraction.user_id)
    await state.update_data(chat_id=chat_id)
    await state.update_data(message_id=message_id)

    caption = f"⚙️ *Панель взаимодействия с юзером открыта*\n\n🎯 *Введите id/username пользователя:*" 
    await query.message.edit_caption(
        caption=caption,
        reply_markup=back_to_admin_kb(),
        parse_mode="MarkdownV2"
    )

@router.message(UserInteraction.user_id)
async def user_interaction(message: Message, state: FSMContext):
    user_id = message.text

    user_data = await state.get_data()
    chat_id = user_data.get("chat_id")
    message_id = user_data.get("message_id")

    if user_id[0] == "@":
        user_id = user_id[1:]
        user_id_type = "username"

        await state.update_data(user_id=user_id)
        await state.update_data(user_id_type=user_id_type)

    elif not user_id.isdigit():
        user_id = user_id 
        user_id_type = "username"

        await state.update_data(user_id=user_id)
        await state.update_data(user_id_type=user_id_type)

    elif user_id.isdigit():
        user_id = int(user_id)
        user_id_type = "telegram_id"

        await state.update_data(user_id=user_id)
        await state.update_data(user_id_type=user_id_type)

    else:
        await state.clear()
        caption = "❌ *Некорректный формат идентификатора пользователя*"
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=caption,
            parse_mode="MarkdownV2"
        )
    await init_pool()

    sql_query = f"""
        SELECT telegram_id, username, balance, overall_balance, subscription_time_end, registration_data, banned
        FROM users
        WHERE {user_id_type} = $1
    """
    user_info = await fetch_db_data(sql_query, (user_id,) )

    if user_info:
        telegram_id = user_info["telegram_id"]
        username = user_info["username"]
        balance = user_info["balance"]
        overall_balance = user_info["overall_balance"]

        subscription_time_end = user_info["subscription_time_end"]

        if subscription_time_end:
            subscription_time_end = datetime.strptime(subscription_time_end.split(".")[0], "%Y-%m-%d %H:%M:%S")
            if datetime.now() >= subscription_time_end:
                subscription_time_end = "expired"   
            else:
                subscription_time_end = subscription_time_end.strftime("%Y-%m-%d %H:%M:%S")
        else:
            subscription_time_end = "wasn't subscribed yet"

        registration_data = user_info["registration_data"]
        registration_data = registration_data.strftime("%Y-%m-%d %H:%M:%S.%f").split(".")[0]

        banned = user_info["banned"]

        caption = (
        f"<b>Данные пользователя:</b>\n\n"
        f"<b>telegram_id:</b> <code>{telegram_id}</code>\n"
        f"<b>username:</b> <code>{username}</code>\n\n"
        f"<b>Текущий баланс:</b> <code>{balance}</code>$\n"
        f"<b>Пополнений за все время:</b> <code>{overall_balance}</code>$\n\n"
        f"<b>Время подписки:</b> <code>{subscription_time_end}</code>\n\n"
        f"<b>Дата регистрации:</b> <code>{registration_data}</code>\n"
        f"<b>Забанен: {banned}</b>"
        )
        await state.update_data(caption=caption)
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=caption,
            reply_markup=admin_user_interaction_kb(),
            parse_mode="HTML"
        )
    else:
        caption = "❌ *Пользователя не существует*"
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=caption,
            reply_markup=back_to_admin_kb(),
            parse_mode="MarkdownV2"
        )
        await state.clear()

    await message.delete()
    await close_pool()
    
@router.callback_query(F.data.in_(
    [
        "change user current balance",
        "change user subscription time end",
        "restrict user permissions"
    ]
))
async def handle_user_interaction(query: CallbackQuery, state: FSMContext):

    await state.set_state(UserInteraction.action)
    await state.update_data(action_type=query.data)
    
    user_data = await state.get_data()
    caption = user_data.get("caption")
    action_type = user_data.get("action_type")
    
    if action_type == "change user current balance":
        caption = f"{caption}\n\n<b>Введите новый баланс пользователя:</b>"
    elif action_type == "change user subscription time end":
        caption = f"{caption}\n\n<b>Введите новое время подписки пользователя:</b>"
    elif action_type == "restrict user permissions":
        caption = f"{caption}\n\n<b>Введите новый статус доступа пользователя к боту (TRUE - бан/FALSE - разбан):</b>"
    await query.message.edit_caption(
        caption=caption,
        reply_markup=back_to_admin_kb(),
        parse_mode="HTML"
    )


@router.message(UserInteraction.action)
async def user_interaction(message: Message, state: FSMContext):
    action = message.text

    await init_pool()
    
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    user_id_type = user_data.get("user_id_type")
    chat_id = user_data.get("chat_id")
    message_id = user_data.get("message_id")
    action_type = user_data.get("action_type")

    if action_type == "change user current balance" and action.isdigit():
    
        action = int(action)
        await state.update_data(action=action)
        user_data = await state.get_data()
        action = user_data.get("action")

        caption = "*Баланс пользователя изменен*"
        sql_query = f"""
            UPDATE users
            SET balance = $1
            WHERE {user_id_type} = $2
            RETURNING telegram_id, username, balance, overall_balance, subscription_time_end, registration_data, banned; 
        """
           
    else:
        caption = "❌ <b>Неккоретное значение</b>\n\n<b>Введите реальное либо целочисленное число</b>"
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=caption,
            reply_markup=back_to_admin_kb(),
            parse_mode="HTML"
        )
            

                       

    if action_type == "change user subscription time end":
        if "days" or "hours" or "minutes" in action:
            await state.update_data(action=action)
            user_data = await state.get_data()
            action = user_data.get("action")

            caption = "*Время подписки пользователя изменено*"
            sql_query = f"""
                UPDATE users
                SET subscription_time_end = CASE
                    WHEN subscription_time_end < NOW() 
                    THEN NOW() + $1::INTERVAL
                    ELSE subscription_time_end + $1::INTERVAL
                END 
                WHERE {user_id_type} = $2;
                RETURNING telegram_id, username, balance, overall_balance, subscription_time_end, registration_data, banned; 
            """
            user_info = await fetch_db_data(sql_query, (action, user_id_type))

        else:
            caption = "❌ <b>Неккоретное значение</b>\n\n<b>Должно как минимум содержать одно из трех: 'days', 'hours', 'minutes'</b>"
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=caption,
                reply_markup=back_to_admin_kb(),
                parse_mode="HTML"
            )

    if action_type == "restrict user permissions":
        action = message.text

        if action == "TRUE" or "FALSE":
            await state.update_data(action=action)
            user_data = await state.get_data()
            action = user_data.get("action")

            caption = "*Статус доступа пользователя к боту изменен*"
            sql_query = f"""
                UPDATE users
                SET banned = CASE 
                    WHEN banned = TRUE THEN FALSE 
                    ELSE TRUE
                END
                WHERE {user_id_type} = $1
                RETURNING telegram_id, username, balance, overall_balance, subscription_time_end, registration_data, banned; 
            """    
            user_info = await fetch_db_data(sql_query, (user_id_type,))

        else:
            caption = "❌ <b>Неккоретное значение<b>\n\n<b>TRUE = забанить<b>\n<b>FALSE = разбанить<b>"
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=caption,
                reply_markup=back_to_admin_kb(),
                parse_mode="HTML"
            )

    telegram_id = user_info["telegram_id"]
    username = user_info["username"]
    balance = user_info["balance"]
    overall_balance = user_info["overall_balance"]

    subscription_time_end = user_info["subscription_time_end"]
    if subscription_time_end:
        subscription_time_end = datetime.strptime(subscription_time_end.split(".")[0], "%Y-%m-%d %H:%M:%S")
        if datetime.now() >= subscription_time_end:
            subscription_time_end = "expired"   
        else:
            subscription_time_end = subscription_time_end.strftime("%Y-%m-%d %H:%M:%S")
    else:
        subscription_time_end = "wasn't subscribed yet"

    registration_data = user_info["registration_data"]
    registration_data = registration_data.strftime("%Y-%m-%d %H:%M:%S.%f").split(".")[0]

    banned = user_info["banned"]

    caption_part = (
        f"<b>Данные пользователя:</b>\n\n"
        f"<b>telegram_id:</b> <code>{telegram_id}</code>\n"
        f"<b>username:</b> <code>{username}</code>\n\n"
        f"<b>Текущий баланс:</b> <code>{balance}</code>$\n"
        f"<b>Пополнений за все время на:</b> <code>{overall_balance}</code>$\n\n"
        f"<b>Время подписки:</b> <code>{subscription_time_end}</code>\n\n"
        f"<b>Дата регистрации:</b> <code>{registration_data}</code>"
        f"<b>Забанен: {banned}</b>"
    )
    
    await bot.edit_message_caption(
        chat_id=chat_id,
        message_id=message_id,
        caption=f"{caption}\n\n{caption_part}",
        reply_markup=back_to_admin_kb(),
        parse_mode="HTML"
    )

    await state.clear()
    await close_pool()

@router.callback_query(F.data == "interaction with users")
async def users_interaction(query: CallbackQuery):
    caption = "*Выберите действие*"
    await query.message.edit_caption(
        caption=caption,
        reply_markup=admin_send_message_kb(),
        parse_mode="MarkdownV2"
    )


@router.callback_query(F.data.in_(
    [
        "message for all from admin",
        "message with photo for all from admin",
        "message with animation for all from admin"
    ]
))
async def handle_admin_messages(query: CallbackQuery, state: FSMContext):
    await init_pool()
    sql_query = """
        SELECT telegram_id
        FROM users
    """
    telegram_ids =  await fetch_db_data(sql_query, target="all")
    telegram_ids = [telegram_id["telegram_id"] for telegram_id in telegram_ids]

    if telegram_ids:
        data = query.data 
        await state.update_data(data_type=data)
        if data == "message for all from admin":
            caption = "🎯 *Отправьте сообщение для рассылки:*"
        elif data == "message with photo for all from admin":
            caption = "🎯 *Отправьте фото c описанием для рассылки:*"
        elif data == "message with animation for all from admin":
            caption = "🎯 *Отправьте анимацию c описанием для рассылки:*"
        elif data == "message with video for all from admin":
            caption = "🎯 *Отправьте видео с описанием для рассылки:*"

        await state.set_state(AdminMessage.send_message)
        await query.message.edit_caption(
            caption=caption,
            reply_markup=profile_kb(),
            parse_mode="MarkdownV2",
        )
        await close_pool()

@router.message(AdminMessage.send_message)
async def admin_send_message(message: Message, state: FSMContext):
    await init_pool()

    admin_data = await state.get_data()
    data_type = admin_data.get("data_type")
    
    sql_query = """
        SELECT telegram_id
        FROM users
    """
    telegram_ids = await fetch_db_data(sql_query, target="all")
    telegram_ids = [telegram_id["telegram_id"] for telegram_id in telegram_ids]

    if telegram_ids:

        if data_type == "message for all from admin":
            await state.update_data(send_message=message.text)
            admin_data = await state.get_data()
            text = admin_data.get("send_message")

            for telegram_id in telegram_ids:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=text,
                    parse_mode="MarkdownV2"
                )

        elif data_type == "message with photo for all from admin":
            photo = message.photo[-1]  
            photo_id = photo.file_id
            await state.update_data(send_message=photo_id)
            await state.update_data(message_caption=message.caption)

            admin_data =  await state.get_data()
            photo = admin_data.get("send_message")
            caption = admin_data.get("message_caption")

            for telegram_id in telegram_ids:
                await bot.send_photo(
                    chat_id=telegram_id,
                    photo=photo,
                    caption=caption,
                    parse_mode="MarkdownV2"
                )

        elif data_type == "message with animation for all from admin":
            animation = message.animation 
            animation_id = animation.file_id
            await state.update_data(send_message=animation_id)
            await state.update_data(message_caption=message.caption)

            admin_data =  await state.get_data()
            animation = admin_data.get("send_message")
            caption = admin_data.get("message_caption")

            for telegram_id in telegram_ids:
                await bot.send_animation(
                    chat_id=telegram_id,
                    animation=animation,
                    caption=caption,
                    parse_mode="MarkdownV2"
                )

        elif data_type == "message with video for all from admin":
            video = message.video 
            video_id = video.file_id
            await state.update_data(send_message=video_id)
            await state.update_data(message_caption=message.caption)
            
            admin_data =  await state.get_data()
            video = admin_data.get("send_message")
            caption = admin_data.get("message_caption")

            for telegram_id in telegram_ids:
                await bot.send_video(
                    chat_id=telegram_id,
                    video=video,
                    caption=caption,
                    parse_mode="MarkdownV2"
                )

    await state.clear()
    await close_pool()
        

