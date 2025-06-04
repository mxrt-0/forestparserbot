from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery 
from keyboards.inline import scrapper_links_kb, auto_bike_boat_kb, tickets_admission_kb, electronics_kb, family_children_baby_kb, leisure_hobby_neighborhood_kb, home_garden_kb, pets_kb, fashion_beauty_kb, music_movies_books_kb 
from constants import GIF, AD_SECTIONS 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from payment_systems.CryptoBotAPI import create_invoice, invoice_status, delete_invoice 
from database.db import init_pool, close_pool, fetch_db_data, execute_db_query

router = Router()

@router.callback_query(F.data == "scrapper links")
async def settings_section(query: CallbackQuery):
    await query.message.edit_caption(
        caption="🎯 *Выберите категорию в которой хотите добавить\/удалить подкатегорию\/\(ии\):*",
        reply_markup=scrapper_links_kb(),
        parse_mode="MarkdownV2"
    )

@router.callback_query(F.data.in_(
    [
        "Auto, Bike & Boat",
        "Tickets & Admission",
        "Electronics",
        "Family, Children & Baby",
        "Leisure, Hobby & Neighborhood",
        "Home & Garden",
        "Pets",
        "Fashion & Beauty",
        "Music, Movies & Books"
    ]
))
async def choose_category(query: CallbackQuery):
    await init_pool()
    section_name = query.data


    columns_in_section = ", ".join(AD_SECTIONS.get(section_name))
    
    sql_query = f"""
        SELECT {columns_in_section}
        FROM user_preferences 
        WHERE telegram_id = $1
    """
    telegram_id = query.from_user.id
    data = await fetch_db_data(sql_query, (telegram_id,))


    values = []
    for value in data:
        if value:
            values.append("✅") 
        else:
            values.append("❌")


    current_kb = None
    if section_name == "Auto, Bike & Boat":
        current_kb = auto_bike_boat_kb(values)
    elif section_name == "Tickets & Admission":
        current_kb = tickets_admission_kb(values)
    elif section_name == "Electronics":
        current_kb = electronics_kb(values)
    elif section_name == "Family, Children & Baby":
        current_kb = family_children_baby_kb(values)
    elif section_name == "Leisure, Hobby & Neighborhood":
        current_kb = leisure_hobby_neighborhood_kb(values)
    elif section_name == "Home & Garden":
        current_kb = home_garden_kb(values)
    elif section_name == "Pets":
        current_kb = pets_kb(values)
    elif section_name == "Fashion & Beauty":
        current_kb = fashion_beauty_kb(values)
    elif section_name == "Music, Movies & Books":
        current_kb = music_movies_books_kb(values)

    await query.message.edit_caption(
        caption="🎯 *Добавьте\/удалите подкатегорию\/\(ии\):*",
        reply_markup=current_kb,
        parse_mode="MarkdownV2"
    )
    await close_pool()

@router.callback_query(F.data.in_(
    [
        # Auto, Rad & Boot
        "Auto, Bike & Boat__auto_parts_tires",                          
        "Auto, Bike & Boat__boats_boat_accessories",
        "Auto, Bike & Boat__bicycles_accessories",
        "Auto, Bike & Boat__motorcycle_parts_accessories",
        
        # Eintrittskarten & Tickets
        "Tickets & Admission__train_public_transport",
        "Tickets & Admission__comedy_cabaret",
        "Tickets & Admission__vouchers",
        "Tickets & Admission__kids",
        "Tickets & Admission__concerts",
        "Tickets & Admission__sports",
        "Tickets & Admission__theater_musical",
        "Tickets & Admission__other_tickets",
        
        # Elektronik
        "Electronics__audio_hifi",
        "Electronics__photo",
        "Electronics__mobile_phones_telephones",
        "Electronics__household_appliances",
        "Electronics__consoles",
        "Electronics__laptops",
        "Electronics__pcs",
        "Electronics__pc_accessories_software",
        "Electronics__tablets_ereaders",
        "Electronics__tv_video",
        "Electronics__video_games",
        "Electronics__other_electronics",
        
        # Family, Children & Baby
        "Family, Children & Baby__elder_care",
        "Family, Children & Baby__baby_kids_clothing",
        "Family, Children & Baby__baby_kids_shoes",
        "Family, Children & Baby__baby_equipment",
        "Family, Children & Baby__baby_seats_child_seats",
        "Family, Children & Baby__babysitter_childcare",
        "Family, Children & Baby__strollers_buggy",
        "Family, Children & Baby__children_room_furniture",
        "Family, Children & Baby__toys",
        "Family, Children & Baby__other_family_children_baby",
        
        # Leisure, Hobby & Neighborhood
        "Leisure, Hobby__esoteric_spiritual",
        "Leisure, Hobby__food_drink",
        "Leisure, Hobby__leisure_activities",
        "Leisure, Hobby__crafts_handmade",
        "Leisure, Hobby__art_antiques",
        "Leisure, Hobby__artists_musicians",
        "Leisure, Hobby__model_building",
        "Leisure, Hobby__travel_event_services",
        "Leisure, Hobby__collectibles",
        "Leisure, Hobby__sports_camping",
        "Leisure, Hobby__flea_market",
        "Leisure, Hobby__lost_found",
        "Leisure, Hobby__other_leisure_hobby_neighborhood",

        # Home & Garden
        "Home & Garden__bathroom",
        "Home & Garden__office",
        "Home & Garden__decoration",
        "Home & Garden__home_garden_services",
        "Home & Garden__garden_accessories_plants",
        "Home & Garden__home_textiles",
        "Home & Garden__diy",
        "Home & Garden__kitchen_dining_room",
        "Home & Garden__lighting",
        "Home & Garden__bedroom",
        "Home & Garden__living_room",
        "Home & Garden__other_home_garden",
        
        # Pets
        "Pets__fish",
        "Pets__dogs",
        "Pets__cats",
        "Pets__small_animals",
        "Pets__farm_animals",
        "Pets__horses",
        "Pets__pet_care_training",
        "Pets__birds",
        "Pets__pet_accessories",
        
        # Fashion & Beauty
        "Fashion & Beauty__beauty_health",
        "Fashion & Beauty__womens_clothing",
        "Fashion & Beauty__womens_shoes",
        "Fashion & Beauty__mens_clothing",
        "Fashion & Beauty__mens_shoes",
        "Fashion & Beauty__bags_accessories",
        "Fashion & Beauty__watches_jewelry",
        "Fashion & Beauty__other_fashion_beauty",
        
        # Music, Movies & Books
        "Music, Movies & Books__books_magazines",
        "Music, Movies & Books__office_supplies",
        "Music, Movies & Books__comics",
        "Music, Movies & Books__textbooks_school_study",
        "Music, Movies & Books__films_dvds",
        "Music, Movies & Books__music_cds",
        "Music, Movies & Books__musical_instruments",
        "Music, Movies & Books__other_music_movies_books"
    ]
))
async def change_undercategories(query: CallbackQuery):
    await init_pool()

    telegram_id = query.from_user.id

    section_name = query.data.split("__")[0].strip()
    if section_name == "Leisure, Hobby":
        section_name += " & Neighborhood"
    column_name = query.data.split("__")[1].strip()
    undercategories = ",".join(AD_SECTIONS.get(section_name))

    sql_query = f"""
        UPDATE user_preferences
        SET {column_name} = CASE 
            WHEN {column_name} = TRUE THEN FALSE
            ELSE TRUE
        END
        WHERE telegram_id = $1
        RETURNING {undercategories};
    """
    data = await fetch_db_data(sql_query, (telegram_id,))

    values = []
    for value in data:
        if value:
            values.append("✅") 
        else:
            values.append("❌")


    current_kb = None
    if section_name == "Auto, Bike & Boat":
        current_kb = auto_bike_boat_kb(values)
    elif section_name == "Tickets & Admission":
        current_kb = tickets_admission_kb(values)
    elif section_name == "Electronics":
        current_kb = electronics_kb(values)
    elif section_name == "Family, Children & Baby":
        current_kb = family_children_baby_kb(values)
    elif section_name == "Leisure, Hobby & Neighborhood":
        current_kb = leisure_hobby_neighborhood_kb(values)
    elif section_name == "Home & Garden":
        current_kb = home_garden_kb(values)
    elif section_name == "Pets":
        current_kb = pets_kb(values)
    elif section_name == "Fashion & Beauty":
        current_kb = fashion_beauty_kb(values)
    elif section_name == "Music, Movies & Books":
        current_kb = music_movies_books_kb(values)
    await query.message.edit_caption(
        caption="🎯 *Добавьте\/удалите подкатегорию\/\(ии\):*",
        reply_markup=current_kb,
        parse_mode="MarkdownV2"
    )
    await close_pool()

