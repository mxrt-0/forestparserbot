from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton        

def channels_kb(CHANNELS_LIST):
    channels_keyboard=[]

    for channel_data in CHANNELS_LIST:
        label = channel_data.get("label")
        url = channel_data.get("url")

        if label and url:
            kb = [InlineKeyboardButton(text=label, url=url)]
            channels_keyboard.append(kb)

        
    channels_keyboard.append([InlineKeyboardButton(
        text="Проверить подписку", 
        callback_data="check_subscription"
    )])
    return InlineKeyboardMarkup(inline_keyboard=channels_keyboard)

def main_kb():
    main_keyboard = [
        [InlineKeyboardButton(text="♻️ Парсер", callback_data="parser section")],
        [InlineKeyboardButton(text="💸 Подписка", callback_data="subscription section")],
        [InlineKeyboardButton(text="🛠 Настройки", callback_data="settings section"),
        InlineKeyboardButton(text="🪬 Профиль ", callback_data="profile section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=main_keyboard)

def admin_main_kb():
    main_keyboard = [
        [InlineKeyboardButton(text="♻️ Парсер", callback_data="parser section")],
        [InlineKeyboardButton(text="💸 Подписка", callback_data="subscription section")],
        [InlineKeyboardButton(text="🛠 Настройки", callback_data="settings section"),
        InlineKeyboardButton(text="🪬 Профиль", callback_data="profile section")],
        [InlineKeyboardButton(text="📊 Админ панель", callback_data="admin panel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=main_keyboard)

def settings_section_kb(min_price, max_price, min_view_count, max_view_count):
    settings_keyboard = [        
        [InlineKeyboardButton(text=f"🔖 Диапазон цен:", callback_data="change price")],
        [InlineKeyboardButton(text=f"📉 от {min_price}", callback_data="change min price"),
        InlineKeyboardButton(text=f"📈 до {max_price}", callback_data="change max price")],
        [InlineKeyboardButton(text=f"👀 Диапазон просмотров за чаc:", callback_data="change view count")],
        [InlineKeyboardButton(text=f"📉 от {min_view_count}", callback_data="change min view count"),
        InlineKeyboardButton(text=f"📈 до {max_view_count}", callback_data="change max view count")],
        [InlineKeyboardButton(text="📁 Категории", callback_data="scrapper links"),
        InlineKeyboardButton(text="🚫 Банворды", callback_data="banwords")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=settings_keyboard)

def subscription_section_kb():
    subscription_keyboard = [
        [InlineKeyboardButton(text="💸 Пополнить баланс", callback_data="top up balance")],
        [InlineKeyboardButton(text="🎫 Купить подписку", callback_data="buy subscription")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")], 
    ]
    return InlineKeyboardMarkup(inline_keyboard=subscription_keyboard)


def profile_kb():
    profile_keyboard = [
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=profile_keyboard)

def profile_main_kb():
    profile_keyboard = [
        [InlineKeyboardButton(text="👥 Реферальная программа", callback_data="referral program")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=profile_keyboard)

def referral_program_kb():
    select_payment_method_keyboard= [
        [InlineKeyboardButton(text="💸 Вывести реферальный баланс", callback_data="withdraw referrer balance")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="profile section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=select_payment_method_keyboard)

def back_to_referrer_program():
    select_payment_method_keyboard= [
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="referral program")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=select_payment_method_keyboard)

def select_payment_method_kb():
    select_payment_method_keyboard= [
        [InlineKeyboardButton(text="💸 CryptoBot", callback_data="CryptoBot")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to subscription section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=select_payment_method_keyboard)

def select_cryptocurrency_kb():
    select_cryptocurrency_keyboard = [
        [InlineKeyboardButton(text="💸 USDT", callback_data="USDT")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to subscription section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=select_cryptocurrency_keyboard)

def select_payment_amount_kb():
    select_payment_amount_keyboard = [
        [InlineKeyboardButton(text="💸 5$ (1 день)", callback_data="amount_5"),
        InlineKeyboardButton(text="💸 12$ (3 дня)", callback_data="amount_12")],
        [InlineKeyboardButton(text="💸 25$ (7 дней)", callback_data="amount_25"), 
        InlineKeyboardButton(text="💸 83$ (30 дней)", callback_data="amount_83")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to subscription section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=select_payment_amount_keyboard)


async def payment_transaction_kb(amount, telegram_id, create_invoice): 
    invoice_id, invoice_url = await create_invoice(amount)
    invoice_identificator = invoice_url.replace("https://t.me/CryptoBot?start=", "")
    payment_transaction_keyboard = [
        [InlineKeyboardButton(text="💸 Оплатить счёт", url=invoice_url)],
        [InlineKeyboardButton(text="♻️ Проверить платёж", callback_data=f"inv_,{invoice_id},{invoice_identificator},{amount}, {telegram_id}")], 
    ]
    return InlineKeyboardMarkup(inline_keyboard=payment_transaction_keyboard)


def buy_subscription_kb():
    buy_subscription_keyboard = [
        [InlineKeyboardButton(text="⌛ 1 день (5$)", callback_data="d_1,price_5"),
        InlineKeyboardButton(text="⌛ 3 дня (12$)", callback_data="d_3,price_12")],
        [InlineKeyboardButton(text="⌛ 7 дней (25$)", callback_data="d_7,price_25"), 
        InlineKeyboardButton(text="⌛ 30 дней (83$)", callback_data="d_30,price_83")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buy_subscription_keyboard)


def top_up_balance_redirect_kb():
    top_up_balance_redirect_keyboard = [
        [InlineKeyboardButton(text="💸 Пополнить баланс", callback_data="top up balance")],
        [InlineKeyboardButton(text="⬅️Вернуться назад", callback_data="back to menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=top_up_balance_redirect_keyboard)


def scrapper_links_kb():
    scrapper_links_keyboard = [
        [InlineKeyboardButton(text="🚗🚲⛵ Auto, Rad & Boot", callback_data="Auto, Bike & Boat")],
        [InlineKeyboardButton(text="🎟️🎫 Eintrittskarten & Tickets", callback_data="Tickets & Admission")],
        [InlineKeyboardButton(text="📱💻 Elektronik", callback_data="Electronics")],
        [InlineKeyboardButton(text="👪👶 Familie, Kind & Baby", callback_data="Family, Children & Baby")],
        [InlineKeyboardButton(text="🎮🎨 Freizeit, Hobby & Nachbarschaft", callback_data="Leisure, Hobby & Neighborhood")],
        [InlineKeyboardButton(text="🏠🌱 Haus & Garten", callback_data="Home & Garden")],
        [InlineKeyboardButton(text="🐶🐱 Haustiere", callback_data="Pets")],
        [InlineKeyboardButton(text="👗💅 Mode & Beauty", callback_data="Fashion & Beauty")],
        [InlineKeyboardButton(text="🎶🎬📚 Musik, Filme & Bücher", callback_data="Music, Movies & Books")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=scrapper_links_keyboard)


def auto_bike_boat_kb(text_data):
    auto_rad_boot_kb = [
        [InlineKeyboardButton(text=f"Autoteile & Reifen {text_data[0]}", callback_data="Auto, Bike & Boat__auto_parts_tires")],
        [InlineKeyboardButton(text=f"Boote & Bootszubehör {text_data[1]}", callback_data="Auto, Bike & Boat__boats_boat_accessories")],
        [InlineKeyboardButton(text=f"Fahrräder & Zubehör {text_data[2]}", callback_data="Auto, Bike & Boat__bicycles_accessories")],
        [InlineKeyboardButton(text=f"Motorradteile & Zubehör {text_data[3]}", callback_data="Auto, Bike & Boat__motorcycle_parts_accessories")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=auto_rad_boot_kb)

def tickets_admission_kb(text_data):
    eintrittskarten_tickets_kb = [
        [InlineKeyboardButton(text=f"Bahn & ÖPNV {text_data[0]}", callback_data="Tickets & Admission__train_public_transport")],
        [InlineKeyboardButton(text=f"Comedy & Kabarett {text_data[1]}", callback_data="Tickets & Admission__comedy_cabaret")],
        [InlineKeyboardButton(text=f"Gutscheine {text_data[2]}", callback_data="Tickets & Admission__vouchers")],
        [InlineKeyboardButton(text=f"Kinder {text_data[3]}", callback_data="Tickets & Admission__kids")],
        [InlineKeyboardButton(text=f"Konzerte {text_data[4]}", callback_data="Tickets & Admission__concerts")],
        [InlineKeyboardButton(text=f"Sport {text_data[5]}", callback_data="Tickets & Admission__sports")],
        [InlineKeyboardButton(text=f"Theater & Musical {text_data[6]}", callback_data="Tickets & Admission__theater_musical")],
        [InlineKeyboardButton(text=f"Weitere Eintrittskarten & Tickets {text_data[7]}", callback_data="Tickets & Admission__other_tickets")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]

    ]
    return InlineKeyboardMarkup(inline_keyboard=eintrittskarten_tickets_kb)

def electronics_kb(text_data):
    elektronik_kb = [
        [InlineKeyboardButton(text=f"Audio & Hifi {text_data[0]}", callback_data="Electronics__audio_hifi")],
        [InlineKeyboardButton(text=f"Foto {text_data[1]}", callback_data="Electronics__photo")],
        [InlineKeyboardButton(text=f"Handy & Telefon {text_data[2]}", callback_data="Electronics__mobile_phones_telephones")],
        [InlineKeyboardButton(text=f"Haushaltsgeräte {text_data[3]}", callback_data="Electronics__household_appliances")],
        [InlineKeyboardButton(text=f"Konsolen {text_data[4]}", callback_data="Electronics__consoles")],
        [InlineKeyboardButton(text=f"Notebooks {text_data[5]}", callback_data="Electronics__laptops")],
        [InlineKeyboardButton(text=f"PCs {text_data[6]}", callback_data="Electronics__pcs")],
        [InlineKeyboardButton(text=f"Pc-Zubehör & Software {text_data[7]}", callback_data="Electronics__pc_accessories_software")],
        [InlineKeyboardButton(text=f"Tablets & Reader {text_data[8]}", callback_data="Electronics__tablets_ereaders")],
        [InlineKeyboardButton(text=f"Tv & Video {text_data[9]}", callback_data="Electronics__tv_video")],
        [InlineKeyboardButton(text=f"Videospiele {text_data[10]}", callback_data="Electronics__video_games")],
        [InlineKeyboardButton(text=f"Weitere Elektronik {text_data[11]}", callback_data="Electronics__other_electronics")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=elektronik_kb)

def family_children_baby_kb(text_data):
    familie_kind_baby_kb = [
        [InlineKeyboardButton(text=f"Altenpflege {text_data[0]}", callback_data="Family, Children & Baby__elder_care")],
        [InlineKeyboardButton(text=f"Baby- & Kinderkleidung {text_data[1]}", callback_data="Family, Children & Baby__baby_kids_clothing")],
        [InlineKeyboardButton(text=f"Baby- & Kinderschuhe {text_data[2]}", callback_data="Family, Children & Baby__baby_kids_shoes")],
        [InlineKeyboardButton(text=f"Baby-Ausstattung {text_data[3]}", callback_data="Family, Children & Baby__baby_equipment")],
        [InlineKeyboardButton(text=f"Babyschalen & Kindersitze {text_data[4]}", callback_data="Family, Children & Baby__baby_seats_child_seats")],
        [InlineKeyboardButton(text=f"Babysitter/-in & Kinderbetreuung {text_data[5]}", callback_data="Family, Children & Baby__babysitter_childcare")],
        [InlineKeyboardButton(text=f"Kinderwagen & Buggys {text_data[6]}", callback_data="Family, Children & Baby__strollers_buggy")],
        [InlineKeyboardButton(text=f"Kinderzimmermöbel {text_data[7]}", callback_data="Family, Children & Baby__children_room_furniture")],
        [InlineKeyboardButton(text=f"Spielzeug {text_data[8]}", callback_data="Family, Children & Baby__toys")],
        [InlineKeyboardButton(text=f"Weiteres Familie, Kind & Baby {text_data[9]}", callback_data="Family, Children & Baby__other_family_children_baby")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=familie_kind_baby_kb)


def leisure_hobby_neighborhood_kb(text_data):
    freizeit_hobby_nachbarschaft_kb = [
        [InlineKeyboardButton(text=f"Esoterik & Spirituelles {text_data[0]}", callback_data="Leisure, Hobby__esoteric_spiritual")],
        [InlineKeyboardButton(text=f"Essen & Trinken {text_data[1]}", callback_data="Leisure, Hobby__food_drink")],
        [InlineKeyboardButton(text=f"Freizeitaktivitäten {text_data[2]}", callback_data="Leisure, Hobby__leisure_activities")],
        [InlineKeyboardButton(text=f"Handarbeit, Basteln & Kunsthandwerk {text_data[3]}", callback_data="Leisure, Hobby__crafts_handmade")],
        [InlineKeyboardButton(text=f"Kunst & Antiquitäten {text_data[4]}", callback_data="Leisure, Hobby__art_antiques")],
        [InlineKeyboardButton(text=f"Künstler/-in & Musiker/-in {text_data[5]}", callback_data="Leisure, Hobby__artists_musicians")],
        [InlineKeyboardButton(text=f"Modellbau {text_data[6]}", callback_data="Leisure, Hobby__model_building")],
        [InlineKeyboardButton(text=f"Reise & Eventservices {text_data[7]}", callback_data="Leisure, Hobby__travel_event_services")],
        [InlineKeyboardButton(text=f"Sammeln {text_data[8]}", callback_data="Leisure, Hobby__collectibles")],
        [InlineKeyboardButton(text=f"Sport & Camping {text_data[9]}", callback_data="Leisure, Hobby__sports_camping")],
        [InlineKeyboardButton(text=f"Trödel {text_data[10]}", callback_data="Leisure, Hobby__flea_market")],
        [InlineKeyboardButton(text=f"Verloren & Gefunden {text_data[11]}", callback_data="Leisure, Hobby__lost_found")],
        [InlineKeyboardButton(text=f"Weiteres Freizeit, Hobby & Nachbarschaft {text_data[12]}", callback_data="Leisure, Hobby__other_leisure_hobby_neighborhood")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=freizeit_hobby_nachbarschaft_kb)

def home_garden_kb(text_data):
    haus_garten_kb = [
        [InlineKeyboardButton(text=f"Badezimmer {text_data[0]}", callback_data="Home & Garden__bathroom")],
        [InlineKeyboardButton(text=f"Büro {text_data[1]}", callback_data="Home & Garden__office")],
        [InlineKeyboardButton(text=f"Dekoration {text_data[2]}", callback_data="Home & Garden__decoration")],
        [InlineKeyboardButton(text=f"Dienstleistungen Haus & Garten {text_data[3]}", callback_data="Home & Garden__home_garden_services")],
        [InlineKeyboardButton(text=f"Gartenzubehör & Pflanzen {text_data[4]}", callback_data="Home & Garden__garden_accessories_plants")],
        [InlineKeyboardButton(text=f"Heimtextilien {text_data[5]}", callback_data="Home & Garden__home_textiles")],
        [InlineKeyboardButton(text=f"Heimwerken {text_data[6]}", callback_data="Home & Garden__diy")],
        [InlineKeyboardButton(text=f"Küche & Esszimmer {text_data[7]}", callback_data="Home & Garden__kitchen_dining_room")],
        [InlineKeyboardButton(text=f"Lampen & Licht {text_data[8]}", callback_data="Home & Garden__lighting")],
        [InlineKeyboardButton(text=f"Schlafzimmer {text_data[9]}", callback_data="Home & Garden__bedroom")],
        [InlineKeyboardButton(text=f"Wohnzimmer {text_data[10]}", callback_data="Home & Garden__living_room")],
        [InlineKeyboardButton(text=f"Weiteres Haus & Garten {text_data[11]}", callback_data="Home & Garden__other_home_garden")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=haus_garten_kb)

def pets_kb(text_data):
    haustiere_kb = [
        [InlineKeyboardButton(text=f"Fische {text_data[0]}", callback_data="Pets__fish")],
        [InlineKeyboardButton(text=f"Hunde {text_data[1]}", callback_data="Pets__dogs")],
        [InlineKeyboardButton(text=f"Katzen {text_data[2]}", callback_data="Pets__cats")],
        [InlineKeyboardButton(text=f"Kleintiere {text_data[3]}", callback_data="Pets__small_animals")],
        [InlineKeyboardButton(text=f"Nutztiere {text_data[4]}", callback_data="Pets__farm_animals")],
        [InlineKeyboardButton(text=f"Pferde {text_data[5]}", callback_data="Pets__horses")],
        [InlineKeyboardButton(text=f"Tierbetreuung & Training {text_data[6]}", callback_data="Pets__pet_care_training")],
        [InlineKeyboardButton(text=f"Vögel {text_data[7]}", callback_data="Pets__birds")],
        [InlineKeyboardButton(text=f"Zubehör {text_data[8]}", callback_data="Pets__pet_accessories")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=haustiere_kb)

def fashion_beauty_kb(text_data):
    mode_beauty_kb = [
        [InlineKeyboardButton(text=f"Beauty & Gesundheit {text_data[0]}", callback_data="Fashion & Beauty__beauty_health")],
        [InlineKeyboardButton(text=f"Damenbekleidung {text_data[1]}", callback_data="Fashion & Beauty__womens_clothing")],
        [InlineKeyboardButton(text=f"Damenschuhe {text_data[2]}", callback_data="Fashion & Beauty__womens_shoes")],
        [InlineKeyboardButton(text=f"Herrenbekleidung {text_data[3]}", callback_data="Fashion & Beauty__mens_clothing")],
        [InlineKeyboardButton(text=f"Herrenschuhe {text_data[4]}", callback_data="Fashion & Beauty__mens_shoes")],
        [InlineKeyboardButton(text=f"Taschen & Accessoires {text_data[5]}", callback_data="Fashion & Beauty__bags_accessories")],
        [InlineKeyboardButton(text=f"Uhren & Schmuck {text_data[6]}", callback_data="Fashion & Beauty__watches_jewelry")],
        [InlineKeyboardButton(text=f"Weiteres Mode & Beauty {text_data[7]}", callback_data="Fashion & Beauty__other_fashion_beauty")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=mode_beauty_kb)

def music_movies_books_kb(text_data):
    musik_filme_bucher_kb = [
        [InlineKeyboardButton(text=f"Bücher & Zeitschriften {text_data[0]}", callback_data="Music, Movies & Books__books_magazines")],
        [InlineKeyboardButton(text=f"Büro & Schreibwaren {text_data[1]}", callback_data="Music, Movies & Books__office_supplies")],
        [InlineKeyboardButton(text=f"Comics {text_data[2]}", callback_data="Music, Movies & Books__comics")],
        [InlineKeyboardButton(text=f"Fachbücher, Schule & Studium {text_data[3]}", callback_data="Music, Movies & Books__textbooks_school_study")],
        [InlineKeyboardButton(text=f"Film & DVD {text_data[4]}", callback_data="Music, Movies & Books__films_dvds")],
        [InlineKeyboardButton(text=f"Musik & CDs {text_data[5]}", callback_data="Music, Movies & Books__music_cds")],
        [InlineKeyboardButton(text=f"Musikinstrumente{text_data[6]}", callback_data="Music, Movies & Books__musical_instruments")],
        [InlineKeyboardButton(text=f"Weitere Musik, Filme & Bücher {text_data[7]}", callback_data="Music, Movies & Books__other_music_movies_books")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to categories section")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=musik_filme_bucher_kb)


def banwords_kb():
    banwords_kb = [
        [InlineKeyboardButton(text="❌ Удалить банворды", callback_data="delete banwords")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=banwords_kb)


def retry_banwords_kb():
    banwords_kb = [
        [InlineKeyboardButton(text="♻️ Изменить повторно", callback_data="change banwords again")],
        [InlineKeyboardButton(text="❌ Удалить банворды", callback_data="delete banwords")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=banwords_kb)


def retry_min_price_kb():
    price_kb = [
        [InlineKeyboardButton(text="♻️ Изменить повторно", callback_data="change min price")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def retry_max_price_kb():
    price_kb = [
        [InlineKeyboardButton(text="♻️ Изменить повторно", callback_data="change max price")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def choose_between_prices_kb():
    price_kb = [
        [InlineKeyboardButton(text="📉 Минимальную цену", callback_data="change min price")],
        [InlineKeyboardButton(text="📈 Максимальную цену", callback_data="change max price")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)


def choose_between_views_kb():
    price_kb = [
        [InlineKeyboardButton(text="📉 Минимальное кол-во просмотров", callback_data="change min view count")],
        [InlineKeyboardButton(text="📈 Максимальное кол-во просмотров", callback_data="change max view count")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)


def retry_view_count_kb():
    price_kb = [
        [InlineKeyboardButton(text="♻️ Изменить повторно", callback_data="change view count")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def back_to_settings_kb():
    price_kb = [
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to settings section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def parser_section_kb():
    price_kb = [
        [InlineKeyboardButton(text="♻️ Запустить парсер", callback_data="start monitoring database")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def admin_kb(): 
    price_kb = [ 
        [InlineKeyboardButton(text="♻️ Взаимодействие с пользователями", callback_data="interaction with users")],
        [InlineKeyboardButton(text="♻️ Взаимодействие с пользователем", callback_data="interaction with user")],
        [InlineKeyboardButton(text="♻️ Открыть статистику", callback_data="open bot statistics")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def back_to_admin_kb():
    price_kb = [
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to admin panel section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def admin_user_interaction_kb():
    price_kb = [
        [InlineKeyboardButton(text="💬 Изменить баланс", callback_data="change user current balance")],
        [InlineKeyboardButton(text="💬 Изменить время подписки", callback_data="change user subscription time end")],
        [InlineKeyboardButton(text="❌ Забанить", callback_data="restrict user permissions")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to admin panel section")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def admin_send_message_kb():
    price_kb = [
        [InlineKeyboardButton(text="💬 Cообщение", callback_data="message for all from admin"),
        InlineKeyboardButton(text="📸 Фото + текст", callback_data="message with photo for all from admin")],
        [InlineKeyboardButton(text="🎞️ GIF + текст", callback_data="message with animation for all from admin"),
        InlineKeyboardButton(text="🎥 Видео + текст", callback_data="message with animation for all from admin")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)

def balance_success_kb():
    price_kb = [
        [InlineKeyboardButton(text="🎫 Купить подписку", callback_data="buy subscription")],
        [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back to menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=price_kb)
