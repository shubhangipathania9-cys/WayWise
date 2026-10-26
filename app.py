from flask import Flask, render_template, request
from math import ceil

app = Flask(__name__)

# -----------------------------------------
# WAYWISE: DESTINATION STARTER GUIDE
# -----------------------------------------

DESTINATIONS = {
    "manali": {
        "region": "Mountains & nature",
        "morning": [
            "Enjoy a relaxed breakfast and explore Old Manali.",
            "Visit Hadimba Devi Temple and walk through the cedar forest.",
            "Explore Naggar village and its historic castle.",
            "Enjoy a scenic nature walk near the destination.",
            "Discover a quieter village and its local cafés.",
        ],
        "afternoon": [
            "Explore local cafés and independent shops.",
            "Visit a nearby cultural attraction.",
            "Enjoy mountain views and a relaxed lunch.",
            "Explore local handicrafts and regional food.",
            "Leave time for a scenic walk or optional activity.",
        ],
        "evening": [
            "Try Himachali food and enjoy a relaxed evening.",
            "Explore the local market before dinner.",
            "Enjoy a quiet evening with mountain views.",
        ],
    },
    "jaipur": {
        "region": "Culture & heritage",
        "morning": [
            "Explore the City Palace area and its historic streets.",
            "Visit Amber Fort and discover its architecture.",
            "Explore Hawa Mahal from the surrounding old-city streets.",
            "Discover a local craft market and traditional workshops.",
            "Visit a museum or heritage site of your choice.",
        ],
        "afternoon": [
            "Enjoy Rajasthani food at a local restaurant.",
            "Explore the old city's markets and craft shops.",
            "Visit Jantar Mantar and learn about its instruments.",
            "Discover block printing or another local craft.",
            "Take a break at a café before the next activity.",
        ],
        "evening": [
            "Enjoy a traditional Rajasthani dinner.",
            "Explore the old city at a relaxed pace.",
            "Browse local handicrafts and pick up souvenirs.",
        ],
    },
    "kerala": {
        "region": "Nature & slow travel",
        "morning": [
            "Enjoy a relaxed breakfast and explore the local area.",
            "Take a nature walk through a green landscape.",
            "Discover a local village and its everyday life.",
            "Visit a garden or cultural attraction.",
            "Explore a local market and regional produce.",
        ],
        "afternoon": [
            "Try a traditional Kerala meal.",
            "Explore a nearby nature spot.",
            "Discover local crafts and cultural traditions.",
            "Enjoy a scenic boat ride if available locally.",
            "Keep the afternoon flexible for rest or exploration.",
        ],
        "evening": [
            "Enjoy regional food and a relaxed evening.",
            "Watch the sunset at a suitable nearby viewpoint.",
            "Explore the neighbourhood and its local cafés.",
        ],
    },
    "varanasi": {
        "region": "Culture & local life",
        "morning": [
            "Explore the ghats respectfully in the early morning.",
            "Walk through the old city's lanes with time to explore.",
            "Discover local crafts and traditional shops.",
            "Visit a historic temple area and learn about its setting.",
            "Explore a local market and regional food.",
        ],
        "afternoon": [
            "Try local Banarasi food.",
            "Discover silk weaving traditions and local artisans.",
            "Explore a museum or cultural attraction.",
            "Take a break before continuing through the old city.",
            "Explore a neighbourhood beyond the busiest streets.",
        ],
        "evening": [
            "Experience the Ganga riverfront respectfully.",
            "Enjoy a local dinner and explore nearby streets.",
            "Take a relaxed walk in a suitable public area.",
        ],
    },
    "shimla": {
        "region": "Mountains & heritage",
        "morning": [
            "Explore the Ridge and nearby heritage streets.",
            "Walk along Mall Road and discover local shops.",
            "Visit a historic building or local museum.",
            "Explore a nearby village or scenic walking route.",
            "Enjoy a relaxed breakfast with mountain views.",
        ],
        "afternoon": [
            "Try Himachali food at a local restaurant.",
            "Explore local markets and handicraft shops.",
            "Enjoy a scenic walk suitable for your pace.",
            "Visit a nearby cultural attraction.",
            "Keep time free for rest and unplanned discoveries.",
        ],
        "evening": [
            "Enjoy a relaxed walk through the town centre.",
            "Try local food and unwind.",
            "Enjoy the evening views before returning to your stay.",
        ],
    },
    "goa": {
        "region": "Coastal life & culture",
        "morning": [
            "Explore a nearby beach before the busiest hours.",
            "Discover a heritage neighbourhood and its architecture.",
            "Visit a local market and explore regional produce.",
            "Explore a quieter coastal area.",
            "Discover local cafés and neighbourhood streets.",
        ],
        "afternoon": [
            "Try Goan cuisine at a local restaurant.",
            "Explore a historic church or cultural attraction.",
            "Discover local crafts and independent shops.",
            "Enjoy a beach break or optional water activity.",
            "Leave time to relax away from busy tourist areas.",
        ],
        "evening": [
            "Enjoy a coastal sunset where conditions allow.",
            "Try a regional dinner.",
            "Explore a local neighbourhood at a relaxed pace.",
        ],
    },
    "rishikesh": {
        "region": "Nature & adventure",
        "morning": [
            "Enjoy a peaceful walk near the riverfront.",
            "Explore local cafés and nearby streets.",
            "Visit a cultural or spiritual attraction respectfully.",
            "Enjoy a nature walk suited to your ability.",
            "Discover local markets and regional crafts.",
        ],
        "afternoon": [
            "Try a local vegetarian meal.",
            "Explore a nearby nature spot.",
            "Consider a reputable, appropriately supervised adventure activity.",
            "Discover local shops and neighbourhoods.",
            "Keep the afternoon flexible for rest.",
        ],
        "evening": [
            "Enjoy the riverfront respectfully and follow local guidance.",
            "Try regional food and relax.",
            "Explore the nearby market before returning to your stay.",
        ],
    },
}

DEFAULT_DESTINATION = {
    "region": "Local discovery",
    "morning": [
        "Explore a well-known local attraction.",
        "Discover the destination's history and culture.",
        "Take a relaxed walk through a local neighbourhood.",
        "Visit a local market or cultural site.",
        "Start with a scenic spot or a popular landmark.",
    ],
    "afternoon": [
        "Try regional food at a local restaurant.",
        "Explore a nearby cultural or nature attraction.",
        "Discover local shops and independent businesses.",
        "Take a break and choose an activity that interests you.",
        "Leave time for a quieter place beyond the main tourist area.",
    ],
    "evening": [
        "Enjoy regional food and explore the local area.",
        "Find a suitable sunset spot or scenic public area.",
        "Take a relaxed walk and prepare for the next day.",
    ],
}


def clean_number(value, default, minimum=1, maximum=30):
    """Convert form input to a safe integer."""
    try:
        number = int(value)
        return max(minimum, min(number, maximum))
    except (TypeError, ValueError):
        return default


def get_destination_guide(destination):
    """Find a starter guide using the destination name."""
    name = destination.strip().lower()

    for key, guide in DESTINATIONS.items():
        if key in name:
            return guide

    return DEFAULT_DESTINATION


def make_itinerary(destination, days, pace, travel_styles):
    """Build a day-by-day starter itinerary."""
    guide = get_destination_guide(destination)
    itinerary = []

    if pace.lower() == "relaxed":
        slots = ["morning", "afternoon"]
    elif pace.lower() == "packed":
        slots = ["morning", "afternoon", "evening"]
    else:
        slots = ["morning", "afternoon", "evening"]

    styles = [style.lower() for style in travel_styles]

    if "adventure" in styles:
        extra = "Consider a suitable outdoor or adventure activity with a reputable local operator."
    elif "culture" in styles:
        extra = "Look for a local cultural experience or artisan workshop."
    elif "freedom" in styles:
        extra = "Keep this time flexible and choose what interests you most."
    elif "popular" in styles:
        extra = "Consider a popular local attraction and check its current visitor information."
    else:
        extra = "Leave some time for a local discovery that catches your interest."

    for day in range(1, days + 1):
        morning = guide["morning"][(day - 1) % len(guide["morning"])]
        afternoon = guide["afternoon"][(day - 1) % len(guide["afternoon"])]
        evening = guide["evening"][(day - 1) % len(guide["evening"])]

        activities = [
            {"time": "Morning", "activity": morning},
            {"time": "Afternoon", "activity": afternoon},
        ]

        if "evening" in slots:
            activities.append({"time": "Evening", "activity": evening})

        if day == days:
            activities[-1]["activity"] = (
                "Enjoy a final local meal, leave time for checkout, "
                "and prepare for your onward journey."
            )

        itinerary.append({
            "day": day,
            "title": (
                "Arrival & First Discoveries" if day == 1
                else "Departure & Last Memories" if day == days
                else f"Explore {guide['region']}"
            ),
            "activities": activities,
            "tip": extra,
        })

    return itinerary, guide["region"]


def estimate_budget(budget, days, travellers, accommodation, flexibility, emergency):
    """
    Produce an illustrative split of the user's total trip budget.
    This is a planning estimate, not a live quotation.
    """
    total = max(0, budget)

    # Accommodation preference influences the suggested split.
    lodging_share = {
        "hostel": 0.25,
        "homestay": 0.30,
        "hotel": 0.38,
    }.get(accommodation.lower(), 0.30)

    food_share = 0.25
    transport_share = 0.20
    activity_share = 0.20

    if flexibility.lower() in ("flexible", "yes", "a little"):
        activity_share += 0.03
        transport_share -= 0.03

    emergency_share = 0.10 if emergency.lower() in ("yes", "true") else 0.05
    core_total = lodging_share + food_share + transport_share + activity_share
    available_for_core = total * (1 - emergency_share)

    # Normalize the categories to the amount remaining after the buffer.
    categories = [
        ("Accommodation", lodging_share),
        ("Food", food_share),
        ("Local transport", transport_share),
        ("Activities & experiences", activity_share),
    ]

    estimates = []
    for name, share in categories:
        amount = round(available_for_core * share / core_total)
        estimates.append({"name": name, "amount": amount})

    buffer_amount = round(total * emergency_share)
    allocated = sum(item["amount"] for item in estimates) + buffer_amount

    # Put any rounding difference into the final category so the total matches.
    estimates[-1]["amount"] += total - allocated

    per_person = round(total / travellers) if travellers else total
    per_day = round(total / days) if days else total

    return {
        "total": total,
        "per_person": per_person,
        "per_day": per_day,
        "emergency_buffer": buffer_amount,
        "categories": estimates,
        "travellers": travellers,
        "days": days,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/plan")
def plan():
    return render_template("plan.html")


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        destination = request.form.get("destination", "").strip()
        days = clean_number(request.form.get("days"), 1, 1, 30)
        travellers = clean_number(request.form.get("travellers"), 1, 1, 20)
        budget = clean_number(request.form.get("budget"), 0, 0, 100000000)

        if not destination:
            destination = "India"

        return render_template(
            "preferences.html",
            destination=destination,
            days=days,
            travellers=travellers,
            budget=budget,
        )

    return render_template("preferences.html")


@app.route("/generate-itinerary", methods=["POST"])
def generate_itinerary():
    destination = request.form.get("destination", "India").strip() or "India"
    days = clean_number(request.form.get("days"), 1, 1, 30)
    travellers = clean_number(request.form.get("travellers"), 1, 1, 20)
    budget = clean_number(request.form.get("budget"), 0, 0, 100000000)

    budget_flexibility = request.form.get("budget_flexibility", "not specified")
    emergency_fund = request.form.get("emergency_fund", "no")
    accommodation = request.form.get("accommodation", "homestay")
    pace = request.form.get("pace", "balanced")
    travel_styles = request.form.getlist("travel_style")

    itinerary, region = make_itinerary(
        destination, days, pace, travel_styles
    )

    budget_breakdown = estimate_budget(
        budget,
        days,
        travellers,
        accommodation,
        budget_flexibility,
        emergency_fund,
    )
    # Destination-specific recommendations
    is_manali = "manali" in destination.lower()

    place_recommendations = MANALI_PLACES if is_manali else []
    stay_recommendations = MANALI_STAYS if is_manali else []

    # Filter stays using the user's accommodation preference
    preferred_type = accommodation.strip().lower()

    if preferred_type == "hostel":
        stay_recommendations = [
        stay for stay in stay_recommendations
        if stay["type"] == "Hostel"
    ]
    elif preferred_type == "homestay":
        stay_recommendations = [
        stay for stay in stay_recommendations
        if stay["type"] == "Homestay"
    ]
    elif preferred_type == "hotel":
        stay_recommendations = [
        stay for stay in stay_recommendations
        if stay["type"] == "Hotel"
    ]
    return render_template(
        "itinerary.html",
        destination=destination,
        days=days,
        travellers=travellers,
        budget=budget,
        budget_flexibility=budget_flexibility,
        emergency_fund=emergency_fund,
        accommodation=accommodation,
        pace=pace,
        travel_styles=travel_styles,
        itinerary=itinerary,
        region=region,
        budget_breakdown=budget_breakdown,
        place_recommendations=place_recommendations,
        stay_recommendations=stay_recommendations,
        is_manali=is_manali,
    )

# -----------------------------------------
# WAYWISE: MANALI PLACE RECOMMENDATIONS
# -----------------------------------------

MANALI_PLACES = [
    {
        "name": "Hadimba Devi Temple",
        "type": "Culture & heritage",
        "description": "Explore the distinctive wooden temple surrounded by tall deodar trees.",
        "area": "Dhungri",
        "kind": "Popular",
        "url": "https://www.google.com/maps/search/?api=1&query=Hadimba+Devi+Temple+Manali",
    },
    {
        "name": "Vashisht Village",
        "type": "Village & culture",
        "description": "Discover the village temple, traditional surroundings and public hot springs.",
        "area": "Vashisht",
        "kind": "Local discovery",
        "url": "https://www.google.com/maps/search/?api=1&query=Vashisht+Village+Manali",
    },
    {
        "name": "Naggar Castle",
        "type": "History & architecture",
        "description": "Explore historic architecture and views across the Kullu Valley.",
        "area": "Naggar",
        "kind": "Cultural escape",
        "url": "https://www.google.com/maps/search/?api=1&query=Naggar+Castle+Himachal+Pradesh",
    },
    {
        "name": "Solang Valley",
        "type": "Nature & adventure",
        "description": "Enjoy mountain scenery and check which outdoor activities are available for your visit.",
        "area": "North of Manali",
        "kind": "Adventure",
        "url": "https://www.google.com/maps/search/?api=1&query=Solang+Valley+Manali",
    },
    {
        "name": "Sajla Waterfall",
        "type": "Nature & short walk",
        "description": "Explore a greener, quieter waterfall area; check local trail and weather conditions first.",
        "area": "Sajla",
        "kind": "Hidden gem",
        "url": "https://www.google.com/maps/search/?api=1&query=Sajla+Waterfall+Manali",
    },
    {
        "name": "Himalayan Nyingmapa Monastery",
        "type": "Culture & reflection",
        "description": "Visit a colourful Buddhist monastery near central Manali and take time to appreciate its art.",
        "area": "Central Manali",
        "kind": "Cultural discovery",
        "url": "https://www.google.com/maps/search/?api=1&query=Himalayan+Nyingmapa+Monastery+Manali",
    },
]

# -----------------------------------------
# WAYWISE: MANALI STAY RECOMMENDATIONS
# -----------------------------------------

MANALI_STAYS = [
    {
        "name": "The Hosteller Manali, Old Manali",
        "type": "Hostel",
        "best_for": "Backpackers and social travellers",
        "area": "Old Manali, Log Huts area",
        "url": "https://www.google.com/maps/search/?api=1&query=The+Hosteller+Manali+Old+Manali",
    },
    {
        "name": "Manali Woods BnB",
        "type": "Homestay",
        "best_for": "Travellers wanting a central base",
        "area": "Model Town, Siyal",
        "url": "https://www.google.com/maps/search/?api=1&query=Manali+Woods+BnB",
    },
    {
        "name": "Kropha HomeStay Manali",
        "type": "Homestay",
        "best_for": "A homely stay near central Manali",
        "area": "Siyal, near the Volvo bus stand",
        "url": "https://www.google.com/maps/search/?api=1&query=Kropha+HomeStay+Manali",
    },
    {
        "name": "Zen Manali by Keekoo Stays",
        "type": "Hotel",
        "best_for": "Travellers seeking private rooms or dorm-style options",
        "area": "Log Huts, Hadimba Temple Road",
        "url": "https://www.google.com/maps/search/?api=1&query=Zen+Manali+by+Keekoo+Stays",
    },
]



if __name__ == "__main__":
    app.run(debug=True)