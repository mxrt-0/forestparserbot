import asyncio 
from aiolimiter import AsyncLimiter
import logging
import re
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest, TelegramNetworkError, TelegramNotFound, TelegramServerError

from database.db import init_pool, close_pool, fetch_db_data, execute_db_query


vintedde = 6580390966
me = 7854485563

kl_1_price_100_300 = -1002433875093
kl_2_price_300_800 = -1002479422564
kl_3_price_800_4500 = -1002423348880


async def monitoring_database(bot):
    print("MONITORING IS STARTED")
    while True:
        #try:
            await init_pool()
            sql_query = """
                SELECT *
                FROM telegram_bot;
            """
            data = await fetch_db_data(sql_query, target="all")

            if data: 
                sql_query = """
                    SELECT user_preferences.*
                    FROM user_preferences
                    JOIN users ON users.telegram_id = user_preferences.telegram_id
                    WHERE users.subscription_time_end > NOW();
                """
                users = await fetch_db_data(sql_query, target="all")
                
                if users:

                    for user in users:
                        try:
                            telegram_id = user["telegram_id"]
                            min_price = user["min_price"]
                            max_price = user["max_price"]
                            min_view_count = user["min_view_count"]
                            max_view_count = user["max_view_count"]
                            banwords = user["banwords"]
                            if banwords:
                                if isinstance(banwords, str):
                                    banwords = banwords.split(",")
                                banwords = [word.strip().lower() for word in banwords]  

                            undercategories_list = [
                                
                                # Auto, Rad & Boot (Auto, Bike & Boat)
                                [user["auto_parts_tires"], "Autoteile & Reifen"],
                                [user["boats_boat_accessories"], "Boote & Bootszubehör"],
                                [user["bicycles_accessories"], "Fahrräder & Zubehör"],
                                [user["motorcycle_parts_accessories"], "Motorradteile & Zubehör"],
                                
                                # Tickets & Admission (Eintrittskarten & Tickets)
                                [user["train_public_transport"], "Bahn & ÖPNV"],
                                [user["comedy_cabaret"], "Comedy & Kabarett"],
                                [user["vouchers"], "Gutscheine"],
                                [user["kids"], "Kinder"],
                                [user["concerts"], "Konzerte"],
                                [user["sports"], "Sport"],
                                [user["theater_musical"], "Theater & Musical"],
                                [user["other_tickets"], "Weitere Eintrittskarten & Tickets"],

                                # Electronics (Elektronik) 
                                [user["audio_hifi"], "Audio & Hifi"], 
                                [user["photo"], "Foto"], 
                                [user["mobile_phones_telephones"], "Handy & Telefon"],
                                [user["household_appliances"], "Haushaltsgeräte"],
                                [user["consoles"], "Konsolen"],
                                [user["laptops"], "Notebooks"],
                                [user["pcs"], "PCs"],
                                [user["pc_accessories_software"], "PC-Zubehör & Software"],
                                [user["tablets_ereaders"], "Tablets & Reader"],
                                [user["tv_video"], "TV & Video"],
                                [user["video_games"], "Videospiele"],
                                [user["other_electronics"], "Weitere Elektronik"],
                                
                                # Family, Children & Baby (Familie, Kind & Baby)
                                [user["elder_care"], "Altenpflege"],
                                [user["baby_kids_clothing"], "Baby- & Kinderkleidung"],
                                [user["baby_kids_shoes"], "Baby- & Kinderschuhe"],
                                [user["baby_equipment"], "Baby-Ausstattung"],
                                [user["baby_seats_child_seats"], "Babyschalen & Kindersitze"],
                                [user["babysitter_childcare"], "Babysitter/-in & Kinderbetreuung"],
                                [user["strollers_buggy"], "Kinderwagen & Buggys"],
                                [user["children_room_furniture"], "Kinderzimmermöbel"],
                                [user["toys"], "Spielzeug"],
                                [user["other_family_children_baby"], "Weiteres Familie, Kind & Baby"],

                                # Leisure, Hobby & Neighborhood (Freizeit, Hobby & Nachbarschaft)
                                [user["esoteric_spiritual"], "Esoterik & Spirituelles"],
                                [user["food_drink"], "Essen & Trinken"],
                                [user["leisure_activities"], "Freizeitaktivitäten"],
                                [user["crafts_handmade"], "Handarbeit, Basteln & Kunsthandwerk"],
                                [user["art_antiques"], "Kunst & Antiquitäten"],
                                [user["artists_musicians"], "Künstler/-in & Musiker/-in"],
                                [user["model_building"], "Modellbau"],
                                [user["travel_event_services"], "Reise & Eventservices"],
                                [user["collectibles"], "Sammeln"],
                                [user["sports_camping"], "Sport & Camping"],
                                [user["flea_market"], "Trödel"],
                                [user["lost_found"], "Verloren & Gefunden"],
                                [user["other_leisure_hobby_neighborhood"], "Weiteres Freizeit, Hobby & Nachbarschaft"],                       
                                # Home & Garden (Haus & Garten)
                                [user["bathroom"], "Badezimmer"],
                                [user["office"], "Büro"],
                                [user["decoration"], "Dekoration"],
                                [user["home_garden_services"], "Dienstleistungen Haus & Garten"],
                                [user["garden_accessories_plants"], "Gartenzubehör & Pflanzen"],
                                [user["home_textiles"], "Heimtextilien"],
                                [user["diy"], "Heimwerken"], 
                                [user["kitchen_dining_room"], "Küche & Esszimmer"],
                                [user["lighting"], "Lampen & Licht"],
                                [user["bedroom"], "Schlafzimmer"],
                                [user["living_room"], "Wohnzimmer"],
                                [user["other_home_garden"], "Weiteres Haus & Garten"],

                                # Pets (Haustiere)
                                [user["fish"], "Fische"],
                                [user["dogs"], "Hunde"],
                                [user["cats"], "Katzen"],
                                [user["small_animals"], "Kleintiere"],
                                [user["farm_animals"], "Nutztiere"],
                                [user["horses"], "Pferde"],
                                [user["pet_care_training"], "Tierbetreuung & Training"],
                                [user["birds"], "Vögel"],
                                [user["pet_accessories"], "Zubehör"],

                                # Fashion & Beauty (Mode & Beauty)       
                                [user["beauty_health"], "Beauty & Gesundheit"],
                                [user["womens_clothing"], "Damenbekleidung"],
                                [user["womens_shoes"], "Damenschuhe"],
                                [user["mens_clothing"], "Herrenbekleidung"],
                                [user["mens_shoes"], "Herrenschuhe"],
                                [user["bags_accessories"], "Taschen & Accessoires"],
                                [user["watches_jewelry"], "Uhren & Schmuck"],
                                [user["other_fashion_beauty"], "Weiteres Mode & Beauty"],

                                # Music, Movies & Books (Musik, Filme & Bücher)
                                [user["books_magazines"], "Bücher & Zeitschriften"],
                                [user["office_supplies"], "Büro & Schreibwaren"],
                                [user["comics"], "Comics"],
                                [user["textbooks_school_study"], "Fachbücher, Schule & Studium"],
                                [user["films_dvds"], "Film & DVD"],
                                [user["music_cds"], "Musik & CDs"],
                                [user["musical_instruments"], "Musikinstrumente"],
                                [user["other_music_movies_books"], "Weitere Musik, Filme & Bücher"],
                            ]
                            #[user[""], ],
                        

                            for item in data:
                                url = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[1])
                                view_count = item[3]
                                parsed_at = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[4])
                                view_count_after_hour = item[5]
                                parsed_at_after_hour = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[6])
                                view_count_after_two = item[7]
                                parsed_at_after_two = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[8])
                                title = item[9]
                                formatted_title = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[9])
                                price = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[10])
                                cleaned_price = (re.sub(r"\D", "", price))
                                int_price = int(cleaned_price) if cleaned_price else 0
                                photo = item[11]
                                description = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', item[12])
                                undercategory = item[13]

                                
                                after_hour_diff = view_count_after_hour - view_count 
                                after_two_diff = view_count_after_two - view_count_after_hour

                                if max_price >= int_price >= min_price and max_view_count >= after_hour_diff >= min_view_count and max_view_count >= after_two_diff >= min_view_count and (banwords is None or not any(banword in title.lower() for banword in banwords)):
                                    for i in range(len(undercategories_list)):
                                        if undercategories_list[i][0] and undercategories_list[i][1] == undercategory:
                                            ad_undercategory = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', undercategories_list[i][1])
                                            caption = f"""
    🕒🇩🇪 *Взято с площадки в:* *{parsed_at}* 
    👀 *Начальное кол\-во просмотров:* `{view_count}`

    ⏳🇩🇪 *Перепроверено в:* *{parsed_at_after_hour}*
    👀 *Просмотров через час:* `{view_count_after_hour}`

    ⏳🇩🇪 *Перепроверено в:* *{parsed_at_after_two}* 
    👀 *Просмотров через 2 часа:* `{view_count_after_two}`


    📜 *Подкатегория*: `{ad_undercategory}`

    🔗 *Ссылка на товар:* [скопировать]({url})

    💥 *Название:* `{formatted_title}`

    💰 *Цена:* `{price}`

    📄 *Описание:* `{description}`
    """                                     
                                            try:
                                                if telegram_id == vintedde:
                                                    if 110 <= int_price < 300:
                                                        telegram_id = kl_1_price_100_300
                                                    elif 300 <= int_price < 800:
                                                        telegram_id = kl_2_price_300_800
                                                    elif 800 <= int_price <= 4500:
                                                        telegram_id = kl_3_price_800_4500

                                                PHOTO_CAPTION_LIMIT = 1024
                                                TEXT_LIMIT = 4096
                                                limiter = AsyncLimiter(5, 1) # Avoid Telegram Flood
                                                async with limiter:
                                                    if photo == "No image":
                                                        for i in range(0, len(caption), TEXT_LIMIT):
                                                            await bot.send_message(
                                                                chat_id=telegram_id, 
                                                                text=caption[i:i+TEXT_LIMIT],
                                                                disable_web_page_preview=True,
                                                                request_timeout=60,

                                                            )
                                                            await asyncio.sleep(0.5)

                                                    elif len(caption) < 1024 and photo != "No image":
                                                        await bot.send_photo(
                                                            chat_id=telegram_id,
                                                            photo=photo,
                                                            caption=caption,
                                                            parse_mode="MarkdownV2",
                                                            request_timeout=60,
                                                        )   
                                                        await asyncio.sleep(0.5)

                                                    elif len(caption) >= 1024 and photo != "No image":
                                                        if len(caption) >= 4096:
                                                            caption = caption[:PHOTO_CAPTION_LIMIT]
                                                            remaining_text = caption[PHOTO_CAPTION_LIMIT:]
                                                            await bot.send_photo(
                                                                chat_id=telegram_id, 
                                                                photo=photo,
                                                                caption=caption,
                                                                request_timeout=60,
                                                            )
                                                            await asyncio.sleep(0.5)

                                                            for i in range(0, len(remaining_text), TEXT_LIMIT):
                                                                text = remaining_text[i:i+TEXT_LIMIT],
                                                                await bot.send_message(
                                                                    chat_id=telegram_id, 
                                                                    text=text,
                                                                    disable_web_page_preview=True
                                                                )
                                                                await asyncio.sleep(0.5)
                                                        elif len(caption) < 4096:
                                                            await bot.send_photo(
                                                                chat_id=telegram_id,
                                                                photo=photo,
                                                                request_timeout=60,
                                                            )   
                                                            await asyncio.sleep(0.5)
                                                            
                                                            await bot.send_message(
                                                                chat_id=telegram_id,
                                                                text=caption,
                                                                parse_mode="MarkdownV2",
                                                                request_timeout=60,
                                                                disable_web_page_preview=True


                                                            )

                                                            await asyncio.sleep(0.5)
                                            except TelegramNotFound:
                                                continue
                                            except TelegramServerError:
                                                continue
                                            except TelegramRetryAfter as e:
                                                print(f"Flood limit reached! Waiting for {e.retry_after} seconds")
                                                await asyncio.sleep(e.retry_after)
                                            except TelegramBadRequest as e:
                                                print(f"Error sending photo: {e}")
                                                await bot.send_message(
                                                    chat_id=telegram_id, 
                                                    text=f"Фото удалено {caption}",
                                                    parse_mode="MarkdownV2",
                                                    disable_web_page_preview=True
                                                )
                                                await asyncio.sleep(0.5)
                                            except Exception as e:
                                                continue

                        except Exception as e:
                            continue

                await init_pool()       
                delete_query = """
                    DELETE FROM telegram_bot
                    WHERE id = $1;
                """
                ids_to_delete = [(id[0],) for id in data]
                await execute_db_query(delete_query, ids_to_delete, target="many")
                await close_pool()

            else:
                logging.info("No new data, sleeping for 5 seconds")
                await asyncio.sleep(5)

        #except Exception as e:
         #   logging.error(f"Error in monitoring database: {e}")
          #  await asyncio.sleep(60)  # Avoid rapid retry on error

