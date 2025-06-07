from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.API.CryptobotAPI import create_invoice, invoice_status
from bot.settings import get_settings

cfg = get_settings()

NEWS = cfg.REQUIRED_CHANNELS["2"]["url"]
SUPPORT = cfg.SUPPORT


def channels_subscription_kb(channels):
    inline_keyboard=[]

    for i in range(len(channels)):
        label = channels[i][0]
        url = channels[i][1]

        button = [InlineKeyboardButton(text=label, url=url)]
        inline_keyboard.append(button)

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ Я подписался",
                callback_data="check_channels_subscription"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def menu_kb():
    inline_keyboard = [
        [InlineKeyboardButton(text="🕸️ Парсер", callback_data="parser")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="charge_balance")],
        [InlineKeyboardButton(text="📰 Новостник", url=NEWS)],
        [InlineKeyboardButton(text="🆘 Поддержка", url=SUPPORT)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def admin_menu_kb():
    inline_keyboard = [
        [InlineKeyboardButton(text="🕸️ Парсер", callback_data="parser")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="charge_balance")],
        [InlineKeyboardButton(text="📰 Новостник", url=NEWS)],
        [InlineKeyboardButton(text="🆘 Поддержка", url=SUPPORT)],
        [InlineKeyboardButton(text="📊 Панель управления", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def choose_direction_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="1.0",
                callback_data="first_direction"
            ),
            InlineKeyboardButton(
                text="2.0",
                callback_data="second_direction")
        ],
        [InlineKeyboardButton(text="🏠 Вернуться в меню",  callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def first_direction_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="kleinanzeigen.de",
                callback_data="kl1"
            )
        ],
        [InlineKeyboardButton(
            text="🔙 Вернуться назад", callback_data="choose_direction"
        )],
        [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def second_direction_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="kleinanzeigen.de",
                callback_data="kl1"
            )
        ],
        [InlineKeyboardButton(
            text="🔙 Вернуться назад", callback_data="choose_direction"
        )],
        [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



def charge_balance_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(text="5$", callback_data="charge_balance_amount_1"),
            InlineKeyboardButton(text="12$", callback_data="charge_balance_amount_2"),
            InlineKeyboardButton(text="25", callback_data="charge_balance_amount_3"),
        ],
        [
            InlineKeyboardButton(text="10$", callback_data="charge_balance_amount_10"),
            InlineKeyboardButton(text="20$", callback_data="charge_balance_amount_20"),
            InlineKeyboardButton(text="30$", callback_data="charge_balance_amount_30"),
        ],
        [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def kl1_menu_kb(data):
    from bot.states.kl1 import buttons
    builder = InlineKeyboardBuilder()
    for i in range(1, len(buttons) + 1):
        text, callback_data, key = buttons[i]
        value = data.get(key)
        builder.button(
            text=text,
            callback_data=callback_data
        )
    builder.button(text="🔙 Вернуться назад", callback_data="kl1")
    builder.button(text="🏠 Вернуться в меню", callback_data="menu")
    rows = ()
    builder.adjust(*rows, 1, 1, 1)

    return InlineKeyboardMarkup(inline_keyboard=builder.export())


def back_to_kl1_kb():
    inline_keyboard = [
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="kl1")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



def ad_menu_kb(data):
    from app.fsm.receipts.amazonde import buttons
    builder = InlineKeyboardBuilder()
    for i in range(1, len(buttons) + 1):
        text, callback_data, key = buttons[i]
        value = data.get(key)
        builder.button(
            text="🟢" + text if value else "🔴" + text,
            callback_data=callback_data
        )
    builder.button(text="🔙 Вернуться назад", callback_data="receipts")
    builder.button(text="🏠 Вернуться в меню", callback_data="menu")
    builder.button(text="✅ Оплатить и создать", callback_data="ad_payment_request")
    rows = (2, 2, 1, 1, 1, 2, 2, 2)
    builder.adjust(*rows, 1, 1, 1)

    return InlineKeyboardMarkup(inline_keyboard=builder.export())


def ad_shipping_price_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="3.99",
                callback_data="ad_shipping_price_id_3.99"),
            InlineKeyboardButton(
                text="4.99",
                callback_data="ad_shipping_price_id_4.99")
        ],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="amazonde")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def back_to_ad_kb():
    inline_keyboard = [
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="amazonde")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def gic_menu_kb(data):
    buttons = {
            1: ("Кол-во сторон", "gic_side_id", "side_id"),
            2: ("Пол", "gic_sex_id", "sex_id"),
            3: ("Номер документа", "gic_doc_number", "doc_number"),
            4: ("Имя", "gic_name", "name"),
            5: ("Фамилия", "gic_surname", "surname"),
            6: ("Подпись", "gic_sign", "sign"),
            7: ("Дата рождения", "gic_birthdate", "birthdate"),
            8: ("Место рождения", "gic_birthplace", "birthplace"),
            9: ("Фото", f"gic_photo_id", "photo_id"),
            10: ("Фон", "gic_bg_id", "bg_id"),
            11: ("Рост", "gic_height", "height"),
            12: ("PLZ + город", "gic_location_code", "location_code"),
            13: ("Улица + № дома", "gic_street", "street")
    }
    stop =  10 if data.get("side_id", "лицевая") == "лицевая" else 13
    builder = InlineKeyboardBuilder()
    for i in range(1, stop + 1):
        text, callback_data, key = buttons[i]
        value =  data.get(key)
        builder.button(
            text="🟢" + text if value else "🔴" + text,
            callback_data=callback_data
        )
    builder.button(text="🔙 Вернуться назад", callback_data="docs")
    builder.button(text="🏠 Вернуться в меню", callback_data="menu")
    builder.button(text="✅ Оплатить и создать", callback_data="gic_payment_request")
    rows = (
        (2, 1, 2, 1, 2, 2)
        if data.get("side_id") == "лицевая"
        or data.get("side_id") == None
        else (2, 1, 2, 1, 2, 2, 1, 2)
    )
    builder.adjust(*rows, 1, 1, 1)

    return InlineKeyboardMarkup(inline_keyboard=builder.export())


def back_to_gic_kb():
    inline_keyboard = [
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="gic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def gic_choose_side_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Лицевая",
                callback_data="gic_side_number_front"
            ),
            InlineKeyboardButton(
                text="Лицевая + задняя",
                callback_data="gic_side_number_both"
            )
        ],
        [InlineKeyboardButton(text=" 🔙 Вернуться назад", callback_data="gic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def gic_choose_sex_kb():
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Мужской ♂️", callback_data=f"gic_sex_number_M"),
            InlineKeyboardButton(text="Женский ♀️", callback_data=f"gic_sex_number_F")
        ],
        [InlineKeyboardButton(text=" 🔙 Вернуться назад", callback_data="gic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def gic_generate_doc_number():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Сгенерировать номер документа",
                callback_data=f"gic_generate_doc_number"
            )
        ],
        [InlineKeyboardButton(text=" 🔙 Вернуться назад", callback_data="gic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def gic_choose_photo_kb(sex):
    end = 24 if sex == "M" else 22
    builder = InlineKeyboardBuilder()
    for i in range(1, end + 1):
        builder.button(
            text=f"• {i}",
            callback_data=f"gic_photo_number_{i}"
        )
    rows = (3, 3, 3, 3, 3, 3, 3, 3) if sex == "M" else (3, 3, 3, 3, 3, 3, 3, 1)
    builder.button(text=" 🔙 Вернуться назад", callback_data="gic")
    builder.adjust(*rows, 1)

    return InlineKeyboardMarkup(inline_keyboard=builder.export())


def gic_choose_bg_kb():
    bg_count = 6
    bgs = ["_", "black", "cardboard", "folder", "paper", "stone", "table"]
    builder = InlineKeyboardBuilder()
    for i in range(1, bg_count + 1):
        builder.button(
            text=f"• {i}",
            callback_data=f"gic_bg_number_{i}_{bgs[i]}"
        )
    builder.button(text=" 🔙 Вернуться назад", callback_data="gic")
    builder.adjust(3, 3, 1)

    return InlineKeyboardMarkup(inline_keyboard=builder.export())


async def payment_request_kb(amount, chat_id, prefix=None, side=None):
    inv_id, inv_url = await create_invoice(amount)
    inline_keyboard = [
        [InlineKeyboardButton(text="💸 Оплатить счёт", url=inv_url)],
        [
            InlineKeyboardButton(
                text="♻️ Проверить оплату",
                callback_data=(
                    f"inv_{inv_id}_{amount}_{chat_id}"
                    if not side and not prefix
                    else f"{prefix}_inv_{inv_id}_{chat_id}" if not side
                    else f"{prefix}_inv_{inv_id}_{chat_id}_{side}"
                )
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
