import asyncio 
from db import init_pool, close_pool, execute_db_query


async def users_table():
    query = """
        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            referrer_id BIGINT,
            username TEXT,
            balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0, 
            overall_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            referrer_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            overall_referrer_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            registration_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            subscription_time_end TIMESTAMP,
            banned BOOLEAN DEFAULT FALSE
    );
    """
    await execute_db_query(query)


async def user_preferences_table():
    query = """
        CREATE TABLE IF NOT EXISTS user_preferences(
            telegram_id BIGINT PRIMARY KEY,
            min_price SMALLINT DEFAULT 100, 
            max_price SMALLINT DEFAULT 5000,
            min_view_count SMALLINT DEFAULT 20,
            max_view_count SMALLINT DEFAULT 1000,
            banwords TEXT DEFAULT 'Nvidia, Apple, Samsung, Iphone, MacBook, Ipad',
            
            -- Auto, Rad & Boot (Auto, Bike & Boat)
            auto_parts_tires BOOLEAN DEFAULT FALSE,                -- Autoteile & Reifen
            boats_boat_accessories BOOLEAN DEFAULT FALSE,          -- Boote & Bootszubehör
            bicycles_accessories BOOLEAN DEFAULT FALSE,            -- Fahrräder & Zubehör
            motorcycle_parts_accessories BOOLEAN DEFAULT FALSE,    -- Motorradteile & Zubehör
            
            -- Tickets & Admission (Eintrittskarten & Tickets)
            train_public_transport BOOLEAN DEFAULT FALSE,                -- Bahn & ÖPNV
            comedy_cabaret BOOLEAN DEFAULT FALSE,                  -- Comedy & Kabarett
            vouchers BOOLEAN DEFAULT FALSE,                         -- Gutscheine
            kids BOOLEAN DEFAULT FALSE,                             -- Kinder
            concerts BOOLEAN DEFAULT FALSE,                         -- Konzerte
            sports BOOLEAN DEFAULT FALSE,                           -- Sport
            theater_musical BOOLEAN DEFAULT FALSE,                  -- Theater & Musical
            other_tickets BOOLEAN DEFAULT FALSE,                    -- Weitere Eintrittskarten & Tickets
            
            -- Electronics (Elektronik)
            audio_hifi BOOLEAN DEFAULT FALSE,                       -- Audio & Hifi
            electronics_services BOOLEAN DEFAULT FALSE,             -- Dienstleistungen Elektronik
            photo BOOLEAN DEFAULT FALSE,                            -- Foto
            mobile_phones_telephones BOOLEAN DEFAULT FALSE,                   -- Handy & Telefon
            household_appliances BOOLEAN DEFAULT FALSE,             -- Haushaltsgeräte
            consoles BOOLEAN DEFAULT FALSE,                         -- Konsolen
            laptops BOOLEAN DEFAULT FALSE,                          -- Notebooks
            pcs BOOLEAN DEFAULT FALSE,                             -- PCs
            pc_accessories_software BOOLEAN DEFAULT FALSE,          -- PC-Zubehör & Software
            tablets_ereaders BOOLEAN DEFAULT FALSE,                  -- Tablets & Reader
            tv_video BOOLEAN DEFAULT FALSE,                         -- TV & Video
            video_games BOOLEAN DEFAULT FALSE,                      -- Videospiele
            other_electronics BOOLEAN DEFAULT FALSE,                -- Weitere Elektronik
            
            -- Family, Children & Baby (Familie, Kind & Baby)
            elder_care BOOLEAN DEFAULT FALSE,                       -- Altenpflege
            baby_kids_clothing BOOLEAN DEFAULT FALSE,               -- Baby- & Kinderkleidung
            baby_kids_shoes BOOLEAN DEFAULT FALSE,                  -- Baby- & Kinderschuhe
            baby_equipment BOOLEAN DEFAULT FALSE,                        -- Baby-Ausstattung
            baby_seats_child_seats BOOLEAN DEFAULT FALSE,             -- Babyschalen & Kindersitze
            babysitter_childcare BOOLEAN DEFAULT FALSE,             -- Babysitter/-in & Kinderbetreuung
            strollers_buggy BOOLEAN DEFAULT FALSE,                  -- Kinderwagen & Buggys
            children_room_furniture BOOLEAN DEFAULT FALSE,                -- Kinderzimmermöbel
            toys BOOLEAN DEFAULT FALSE,                             -- Spielzeug
            other_family_children_baby BOOLEAN DEFAULT FALSE,                -- Weiteres Familie, Kind & Baby
            
            -- Leisure, Hobby & Neighborhood (Freizeit, Hobby & Nachbarschaft)
            esoteric_spiritual BOOLEAN DEFAULT FALSE,            -- Esoterik & Spirituelles
            food_drink BOOLEAN DEFAULT FALSE,                       -- Essen & Trinken
            leisure_activities BOOLEAN DEFAULT FALSE,               -- Freizeitaktivitäten
            crafts_handmade BOOLEAN DEFAULT FALSE,                  -- Handarbeit, Basteln & Kunsthandwerk
            art_antiques BOOLEAN DEFAULT FALSE,                     -- Kunst & Antiquitäten
            artists_musicians BOOLEAN DEFAULT FALSE,                -- Künstler/-in & Musiker/-in
            model_building BOOLEAN DEFAULT FALSE,                   -- Modellbau
            travel_event_services BOOLEAN DEFAULT FALSE,            -- Reise & Eventservices
            collectibles BOOLEAN DEFAULT FALSE,                       -- Sammeln
            sports_camping BOOLEAN DEFAULT FALSE,                   -- Sport & Camping
            flea_market BOOLEAN DEFAULT FALSE,                      -- Trödel
            lost_found BOOLEAN DEFAULT FALSE,                       -- Verloren & Gefunden
            other_leisure_hobby_neighborhood BOOLEAN DEFAULT FALSE,              -- Weiteres Freizeit, Hobby & Nachbarschaft
            
            -- Home & Garden (Haus & Garten)
            bathroom BOOLEAN DEFAULT FALSE,                         -- Badezimmer
            office BOOLEAN DEFAULT FALSE,                           -- Büro
            decoration BOOLEAN DEFAULT FALSE,                       -- Dekoration
            home_garden_services BOOLEAN DEFAULT FALSE,             -- Dienstleistungen Haus & Garten
            garden_accessories_plants BOOLEAN DEFAULT FALSE,        -- Gartenzubehör & Pflanzen
            home_textiles BOOLEAN DEFAULT FALSE,                    -- Heimtextilien
            diy BOOLEAN DEFAULT FALSE,                              -- Heimwerken
            kitchen_dining_room BOOLEAN DEFAULT FALSE,              -- Küche & Esszimmer
            lighting BOOLEAN DEFAULT FALSE,                         -- Lampen & Licht
            bedroom BOOLEAN DEFAULT FALSE,                          -- Schlafzimmer
            living_room BOOLEAN DEFAULT FALSE,                      -- Wohnzimmer
            other_home_garden BOOLEAN DEFAULT FALSE,                -- Weiteres Haus & Garten
            
            -- Pets (Haustiere)
            fish BOOLEAN DEFAULT FALSE,                             -- Fische
            dogs BOOLEAN DEFAULT FALSE,                             -- Hunde
            cats BOOLEAN DEFAULT FALSE,                             -- Katzen
            small_animals BOOLEAN DEFAULT FALSE,                    -- Kleintiere
            farm_animals BOOLEAN DEFAULT FALSE,                     -- Nutztiere
            horses BOOLEAN DEFAULT FALSE,                           -- Pferde
            pet_care_training BOOLEAN DEFAULT FALSE,                -- Tierbetreuung & Training
            birds BOOLEAN DEFAULT FALSE,                            -- Vögel
            pet_accessories BOOLEAN DEFAULT FALSE,                  -- Zubehör
            
            -- Fashion & Beauty (Mode & Beauty)
            beauty_health BOOLEAN DEFAULT FALSE,                    -- Beauty & Gesundheit
            womens_clothing BOOLEAN DEFAULT FALSE,                  -- Damenbekleidung
            womens_shoes BOOLEAN DEFAULT FALSE,                     -- Damenschuhe
            mens_clothing BOOLEAN DEFAULT FALSE,                    -- Herrenbekleidung
            mens_shoes BOOLEAN DEFAULT FALSE,                       -- Herrenschuhe
            bags_accessories BOOLEAN DEFAULT FALSE,                 -- Taschen & Accessoires
            watches_jewelry BOOLEAN DEFAULT FALSE,                  -- Uhren & Schmuck
            other_fashion_beauty BOOLEAN DEFAULT FALSE,             -- Weiteres Mode & Beauty
            
            -- Music, Movies & Books (Musik, Filme & Bücher)
            books_magazines BOOLEAN DEFAULT FALSE,                  -- Bücher & Zeitschriften
            office_supplies BOOLEAN DEFAULT FALSE,                  -- Büro & Schreibwaren
            comics BOOLEAN DEFAULT FALSE,                           -- Comics
            textbooks_school_study BOOLEAN DEFAULT FALSE,         -- Fachbücher, Schule & Studium
            films_dvds BOOLEAN DEFAULT FALSE,                       -- Filme & DVDs
            music_cds BOOLEAN DEFAULT FALSE,                        -- Musik & CDs
            musical_instruments BOOLEAN DEFAULT FALSE,              -- Musikinstrumente
            other_music_movies_books BOOLEAN DEFAULT FALSE          -- Weitere Musik, Filme & Bücher
        );
    """
    await execute_db_query(query)
    

async def main():
    await init_pool()
    await users_table()
    await user_preferences_table()
    await close_pool()

asyncio.run(main())
