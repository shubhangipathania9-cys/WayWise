
import sqlite3
import os

# ========================================
# DATABASE PATH
# ========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "waywise.db")


# ========================================
# DESTINATIONS
# ========================================

DESTINATIONS = [
    ("Manali", "manali", "Himachal Pradesh"),
    ("Jaipur", "jaipur", "Rajasthan"),
    ("Kerala", "kerala", "South India"),
    ("Varanasi", "varanasi", "Uttar Pradesh"),
    ("Shimla", "shimla", "Himachal Pradesh"),
    ("Goa", "goa", "West India"),
    ("Rishikesh", "rishikesh", "Uttarakhand"),
]


# ========================================
# PLACES TO EXPLORE
# ========================================

PLACES = {
    "Manali": [
        ("Hadimba Devi Temple", "Culture", "A historic wooden temple surrounded by cedar forests.", "Old Manali", "popular"),
        ("Vashisht Village", "Culture", "Explore traditional village life and natural hot springs.", "Vashisht", "hidden"),
        ("Naggar Castle", "History", "A heritage castle with beautiful Himalayan views.", "Naggar", "popular"),
        ("Solang Valley", "Adventure", "Enjoy mountain scenery and adventure activities.", "Solang", "adventure"),
        ("Sajla Waterfall", "Nature", "A peaceful waterfall away from the busiest tourist areas.", "Sajla", "hidden"),
        ("Himalayan Nyingmapa Monastery", "Culture", "Visit a peaceful Buddhist monastery.", "Manali", "hidden"),
    ],

    "Jaipur": [
        ("Hawa Mahal", "History", "The iconic Palace of Winds with beautiful architecture.", "Pink City", "popular"),
        ("Amber Fort", "History", "Explore the grand hilltop fort and its courtyards.", "Amer", "popular"),
        ("Panna Meena ka Kund", "Culture", "Discover a historic stepwell with geometric staircases.", "Amer", "hidden"),
        ("Jantar Mantar", "Science", "Explore the historic astronomical instruments.", "Pink City", "popular"),
        ("Patrika Gate", "Photography", "A colourful architectural landmark.", "Jawahar Circle", "popular"),
    ],

    "Kerala": [
        ("Alleppey Backwaters", "Nature", "Experience Kerala's scenic network of canals and lakes.", "Alappuzha", "popular"),
        ("Fort Kochi", "Culture", "Explore heritage streets, art cafes and colonial architecture.", "Kochi", "popular"),
        ("Munnar Tea Gardens", "Nature", "Enjoy rolling tea plantations and mountain views.", "Munnar", "popular"),
        ("Kumbalangi", "Culture", "Discover village life and local fishing traditions.", "Kochi", "hidden"),
        ("Varkala Cliff", "Nature", "Enjoy coastal views, cafes and beach walks.", "Varkala", "popular"),
        ("Periyar Wildlife Sanctuary", "Wildlife", "Explore forests and wildlife around Periyar Lake.", "Thekkady", "adventure"),
    ],

    "Varanasi": [
        ("Dashashwamedh Ghat", "Culture", "Experience the famous Ganga Aarti.", "Ganga River", "popular"),
        ("Assi Ghat", "Culture", "Explore riverside life and peaceful morning views.", "Assi", "popular"),
        ("Sarnath", "History", "Visit an important Buddhist heritage site.", "Sarnath", "popular"),
        ("Manikarnika Ghat", "Culture", "Learn about the city's historic and spiritual traditions.", "Ganga River", "culture"),
        ("Ramnagar Fort", "History", "Explore a historic fort overlooking the Ganga.", "Ramnagar", "hidden"),
    ],

    "Shimla": [
        ("The Ridge", "Culture", "Enjoy open views and the heart of Shimla town.", "Mall Road", "popular"),
        ("Jakhoo Temple", "Culture", "Visit a hilltop temple with panoramic views.", "Jakhoo Hill", "popular"),
        ("Viceregal Lodge", "History", "Explore an important colonial-era heritage building.", "Observatory Hill", "popular"),
        ("Annandale", "Nature", "Discover a quiet open space surrounded by hills.", "Annandale", "hidden"),
        ("Chadwick Falls", "Nature", "Visit a waterfall surrounded by forest.", "Summer Hill", "hidden"),
    ],

    "Goa": [
        ("Baga Beach", "Beach", "Enjoy the lively beach atmosphere and water activities.", "North Goa", "popular"),
        ("Fontainhas", "Culture", "Walk through colourful Portuguese-style heritage streets.", "Panaji", "hidden"),
        ("Dudhsagar Falls", "Nature", "See one of India's spectacular waterfalls.", "Mollem", "adventure"),
        ("Cola Beach", "Beach", "Discover a quieter beach and scenic lagoon.", "South Goa", "hidden"),
        ("Chapora Fort", "History", "Enjoy panoramic coastal views from the fort.", "Vagator", "popular"),
        ("Divar Island", "Culture", "Explore peaceful village roads and local heritage.", "Old Goa", "hidden"),
    ],

    "Rishikesh": [
        ("Lakshman Jhula Area", "Culture", "Explore riverside cafes and views of the Ganga.", "Tapovan", "popular"),
        ("Triveni Ghat", "Culture", "Experience the evening Ganga Aarti.", "Rishikesh", "popular"),
        ("Neer Garh Waterfall", "Nature", "Enjoy a scenic walk to a forest waterfall.", "Rishikesh", "adventure"),
        ("Beatles Ashram", "Culture", "Explore the peaceful ashram and its artwork.", "Swarg Ashram", "hidden"),
        ("Kunjapuri Temple", "Nature", "Enjoy beautiful Himalayan sunrise views.", "Narendra Nagar", "adventure"),
    ],
}


# ========================================
# ACCOMMODATION SUGGESTIONS
# ========================================

ACCOMMODATIONS = {
    "Manali": [
        ("The Hosteller Manali", "Hostel", "Budget travellers", "Old Manali", "https://www.google.com/maps/search/?api=1&query=The+Hosteller+Manali"),
        ("Manali Woods BnB", "Homestay", "Quiet stays", "Manali", "https://www.google.com/maps/search/?api=1&query=Manali+Woods+BnB"),
        ("Kropha HomeStay Manali", "Homestay", "Local experience", "Manali", "https://www.google.com/maps/search/?api=1&query=Kropha+Homestay+Manali"),
        ("Zen Manali by Keekoo Stays", "Hotel", "Comfortable stays", "Manali", "https://www.google.com/maps/search/?api=1&query=Zen+Manali+Keekoo"),
    ],

    "Jaipur": [
        ("Budget hostels in Jaipur", "Hostel", "Solo and student travellers", "Pink City", "https://www.google.com/maps/search/?api=1&query=budget+hostels+Jaipur"),
        ("Heritage homestays in Jaipur", "Homestay", "Local cultural experience", "Old Jaipur", "https://www.google.com/maps/search/?api=1&query=heritage+homestays+Jaipur"),
        ("Budget hotels in Jaipur", "Hotel", "Affordable private rooms", "Jaipur", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Jaipur"),
    ],

    "Kerala": [
        ("Backpacker hostels in Kochi", "Hostel", "Solo travellers", "Fort Kochi", "https://www.google.com/maps/search/?api=1&query=backpacker+hostels+Fort+Kochi"),
        ("Backwater homestays", "Homestay", "Local experiences", "Alleppey", "https://www.google.com/maps/search/?api=1&query=backwater+homestays+Alleppey"),
        ("Budget hotels in Munnar", "Hotel", "Affordable mountain stays", "Munnar", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Munnar"),
        ("Family homestays in Wayanad", "Homestay", "Families and groups", "Wayanad", "https://www.google.com/maps/search/?api=1&query=family+homestays+Wayanad"),
    ],

    "Varanasi": [
        ("Budget hostels near Assi Ghat", "Hostel", "Backpackers", "Assi Ghat", "https://www.google.com/maps/search/?api=1&query=budget+hostels+Assi+Ghat"),
        ("Traditional guesthouses in Varanasi", "Homestay", "Cultural experience", "Old Varanasi", "https://www.google.com/maps/search/?api=1&query=guesthouses+Varanasi"),
        ("Budget hotels in Varanasi", "Hotel", "Affordable private rooms", "Varanasi", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Varanasi"),
    ],

    "Shimla": [
        ("Backpacker hostels in Shimla", "Hostel", "Solo travellers", "Shimla", "https://www.google.com/maps/search/?api=1&query=backpacker+hostels+Shimla"),
        ("Mountain homestays in Shimla", "Homestay", "Local experiences", "Mashobra", "https://www.google.com/maps/search/?api=1&query=mountain+homestays+Shimla"),
        ("Budget hotels in Shimla", "Hotel", "Affordable stays", "Shimla", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Shimla"),
    ],

    "Goa": [
        ("Backpacker hostels in North Goa", "Hostel", "Solo and student travellers", "North Goa", "https://www.google.com/maps/search/?api=1&query=backpacker+hostels+North+Goa"),
        ("Beachside homestays in South Goa", "Homestay", "Peaceful beach stays", "South Goa", "https://www.google.com/maps/search/?api=1&query=homestays+South+Goa"),
        ("Budget hotels in Panaji", "Hotel", "Affordable private rooms", "Panaji", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Panaji"),
        ("Affordable guesthouses in Goa", "Homestay", "Budget travellers", "Goa", "https://www.google.com/maps/search/?api=1&query=affordable+guesthouses+Goa"),
    ],

    "Rishikesh": [
        ("Backpacker hostels in Tapovan", "Hostel", "Solo travellers", "Tapovan", "https://www.google.com/maps/search/?api=1&query=backpacker+hostels+Tapovan+Rishikesh"),
        ("Riverside homestays in Rishikesh", "Homestay", "Nature lovers", "Rishikesh", "https://www.google.com/maps/search/?api=1&query=riverside+homestays+Rishikesh"),
        ("Budget hotels in Rishikesh", "Hotel", "Affordable private rooms", "Rishikesh", "https://www.google.com/maps/search/?api=1&query=budget+hotels+Rishikesh"),
    ],
}


# ========================================
# BUDGET-SAVING ALTERNATIVES
# Each entry has FOUR values:
# category, alternative name, description, saving
# ========================================

BUDGET_ALTERNATIVES = {
    "Manali": [
        ("Accommodation", "Budget homestay", "Choose a budget homestay instead of a premium hotel.", 500),
        ("Local transport", "Shared transport", "Use shared local transport instead of private taxis.", 300),
        ("Activities", "Free attractions", "Explore free local attractions and walking routes.", 400),
    ],

    "Jaipur": [
        ("Accommodation", "Budget guesthouse", "Choose a hostel or guesthouse instead of a luxury hotel.", 600),
        ("Local transport", "Local buses", "Use local buses and shared transport.", 350),
        ("Activities", "Free heritage areas", "Explore public heritage areas and free attractions.", 300),
    ],

    "Kerala": [
        ("Accommodation", "Family-run homestay", "Choose a family-run homestay instead of a resort.", 700),
        ("Local transport", "Public transport", "Use public buses and ferries where available.", 500),
        ("Activities", "Free nature spots", "Explore beaches, village walks and free viewpoints.", 400),
    ],

    "Varanasi": [
        ("Accommodation", "Budget guesthouse", "Stay in a budget guesthouse near your main sightseeing area.", 500),
        ("Local transport", "Walk nearby", "Walk through nearby old-city attractions where practical.", 300),
        ("Activities", "Free public spaces", "Explore the ghats and public spaces without paid tours.", 350),
    ],

    "Shimla": [
        ("Accommodation", "Budget homestay", "Choose a budget homestay away from the busiest areas.", 600),
        ("Local transport", "Local buses", "Use local buses and walk between nearby attractions.", 350),
        ("Activities", "Public viewpoints", "Explore public viewpoints and walking trails.", 300),
    ],

    "Goa": [
        ("Accommodation", "Budget hostel", "Choose a hostel or guesthouse instead of a beach resort.", 800),
        ("Local transport", "Shared rides", "Use public transport or shared rides where available.", 500),
        ("Activities", "Free beaches", "Enjoy public beaches and free heritage walks.", 450),
    ],

    "Rishikesh": [
        ("Accommodation", "Budget hostel", "Choose a hostel or homestay instead of a premium resort.", 500),
        ("Local transport", "Walk nearby", "Walk between nearby attractions and use shared transport.", 300),
        ("Activities", "Free riverside areas", "Explore free riverside areas and walking trails.", 350),
    ],
}


# ========================================
# CREATE DATABASE TABLES
# ========================================

def initialize_database():
    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                region TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                area TEXT,
                kind TEXT,
                url TEXT,
                FOREIGN KEY(destination_id) REFERENCES destinations(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accommodations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                best_for TEXT,
                area TEXT,
                url TEXT,
                FOREIGN KEY(destination_id) REFERENCES destinations(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget_alternatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                alternative_name TEXT NOT NULL,
                description TEXT,
                estimated_saving REAL NOT NULL DEFAULT 0,
                FOREIGN KEY(destination_id) REFERENCES destinations(id)
            )
        """)

        # Insert destinations
        for name, slug, region in DESTINATIONS:
            cursor.execute("""
                INSERT OR IGNORE INTO destinations (name, slug, region)
                VALUES (?, ?, ?)
            """, (name, slug, region))

        # Insert destination-related information
        for destination_name in PLACES:
            cursor.execute("""
                SELECT id FROM destinations
                WHERE LOWER(name) = LOWER(?)
            """, (destination_name,))

            result = cursor.fetchone()

            if result is None:
                continue

            destination_id = result[0]

            # Places
            for place in PLACES[destination_name]:
                cursor.execute("""
                    INSERT OR IGNORE INTO places
                    (destination_id, name, category, description, area, kind)
                    SELECT ?, ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM places
                        WHERE destination_id = ? AND name = ?
                    )
                """, (
                    destination_id, *place,
                    destination_id, place[0]
                ))

            # Accommodation
            for stay in ACCOMMODATIONS.get(destination_name, []):
                cursor.execute("""
                    INSERT OR IGNORE INTO accommodations
                    (destination_id, name, type, best_for, area, url)
                    SELECT ?, ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM accommodations
                        WHERE destination_id = ? AND name = ?
                    )
                """, (
                    destination_id, *stay,
                    destination_id, stay[0]
                ))

            # Budget alternatives
            for alternative in BUDGET_ALTERNATIVES.get(destination_name, []):
                category, alternative_name, description, estimated_saving = alternative

                cursor.execute("""
                    INSERT OR IGNORE INTO budget_alternatives
                    (destination_id, category, alternative_name, description, estimated_saving)
                    SELECT ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM budget_alternatives
                        WHERE destination_id = ?
                        AND category = ?
                        AND alternative_name = ?
                    )
                """, (
                    destination_id,
                    category,
                    alternative_name,
                    description,
                    estimated_saving,
                    destination_id,
                    category,
                    alternative_name
                ))

        connection.commit()

        print("\nWayWise database initialized successfully!")
        print(f"Database location: {DATABASE_PATH}")

        for table in [
            "destinations",
            "places",
            "accommodations",
            "budget_alternatives"
        ]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"{table}: {cursor.fetchone()[0]} records")

        print("\nDESTINATION-WISE COVERAGE")

        cursor.execute("SELECT id, name FROM destinations ORDER BY name")

        for destination_id, name in cursor.fetchall():
            print(f"\n{name}:")

            for table in ["places", "accommodations", "budget_alternatives"]:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE destination_id = ?",
                    (destination_id,)
                )
                print(f"  {table}: {cursor.fetchone()[0]}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()


