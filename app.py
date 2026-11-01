from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import os
import re
from urllib.parse import quote_plus

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

app = Flask(__name__)

# =========================================
# DATABASE CONNECTION
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "waywise.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# =========================================
# DESTINATION NAME NORMALISATION
# =========================================

DESTINATION_ALIASES = {
    "kerela": "kerala",
    "kerala": "kerala",
}


def normalize_destination(destination):
    """Standardise destination names and common spelling variations."""
    name = (destination or "").split(",")[0].strip().lower()
    name = DESTINATION_ALIASES.get(name, name)
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")


# =========================================
# DESTINATION STARTER GUIDES
# =========================================

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
            "Consider a suitable supervised adventure activity.",
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


# =========================================
# HELPER FUNCTIONS
# =========================================

def clean_number(value, default, minimum=1, maximum=30):
    """Convert form input to a safe integer."""
    try:
        number = int(value)
        return max(minimum, min(number, maximum))
    except (TypeError, ValueError):
        return default


def get_destination_guide(destination):
    """Find a starter guide using the standardised destination name."""
    name = normalize_destination(destination)
    return DESTINATIONS.get(name, DEFAULT_DESTINATION)


# =========================================
# BUILD DAY-BY-DAY ITINERARY
# =========================================

def make_itinerary(destination, days, pace, travel_styles):
    guide = get_destination_guide(destination)
    itinerary = []

    pace = (pace or "balanced").lower()
    styles = [style.lower() for style in (travel_styles or [])]

    if pace == "relaxed":
        slots = ["morning", "afternoon"]
    else:
        slots = ["morning", "afternoon", "evening"]

    if "adventure" in styles:
        extra = (
            "Consider a suitable outdoor or adventure activity "
            "with a reputable local operator."
        )
    elif "culture" in styles:
        extra = "Look for a local cultural experience or artisan workshop."
    elif "freedom" in styles:
        extra = "Keep this time flexible and choose what interests you most."
    elif "popular" in styles:
        extra = (
            "Consider a popular local attraction and check its "
            "current visitor information."
        )
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

        if pace == "packed":
            activities.append({
                "time": "Flexible extra",
                "activity": (
                    "If you still have energy, explore another nearby "
                    "attraction or local experience."
                )
            })

        if day == days and days > 1:
            activities[-1]["activity"] = (
                "Enjoy a final local meal, leave time for checkout, "
                "and prepare for your onward journey."
            )

        if days == 1:
            title = "A Day of First & Last Discoveries"
        elif day == 1:
            title = "Arrival & First Discoveries"
        elif day == days:
            title = "Departure & Last Memories"
        else:
            title = f"Explore {guide['region']}"

        itinerary.append({
            "day": day,
            "title": title,
            "activities": activities,
            "tip": extra,
        })

    return itinerary, guide["region"]


# =========================================
# FETCH DATABASE RECOMMENDATIONS
# =========================================

def get_destination_recommendations(destination, accommodation):
    connection = get_db_connection()

    try:
        destination_slug = normalize_destination(destination)

        destination_row = connection.execute("""
            SELECT * FROM destinations
            WHERE LOWER(name) = ?
               OR LOWER(slug) = ?
            LIMIT 1
        """, (
            destination_slug.replace("-", " "),
            destination_slug
        )).fetchone()

        if destination_row is None:
            return [], [], []

        destination_id = destination_row["id"]

        # Places
        places = connection.execute("""
            SELECT * FROM places
            WHERE destination_id = ?
        """, (destination_id,)).fetchall()

        place_recommendations = []

        for place in places:
            place_name = place["name"]

            place_recommendations.append({
                "name": place_name,
                "type": place["category"] or "Discovery",
                "description": place["description"] or "",
                "area": place["area"] or "",
                "kind": place["kind"] or "Local discovery",
                "url": (
                    "https://www.google.com/maps/search/?api=1&query="
                    + quote_plus(f"{place_name} {destination}")
                )
            })

        # Accommodation
        stays = connection.execute("""
            SELECT * FROM accommodations
            WHERE destination_id = ?
        """, (destination_id,)).fetchall()

        stay_recommendations = []
        accommodation = (accommodation or "homestay").strip().lower()

        for stay in stays:
            stay_type = (stay["type"] or "").strip().lower()

            if stay_type == accommodation:
                stay_recommendations.append({
                    "name": stay["name"],
                    "type": stay["type"] or "",
                    "best_for": stay["best_for"] or "",
                    "area": stay["area"] or "",
                    "url": stay["url"] or ""
                })

        # Budget alternatives
        alternatives = connection.execute("""
            SELECT * FROM budget_alternatives
            WHERE destination_id = ?
        """, (destination_id,)).fetchall()

        budget_alternatives = [
            {
                "category": item["category"],
                "alternative_name": item["alternative_name"],
                "description": item["description"] or "",
                "estimated_saving": item["estimated_saving"]
            }
            for item in alternatives
        ]

        return (
            place_recommendations,
            stay_recommendations,
            budget_alternatives
        )

    finally:
        connection.close()


# =========================================
# ESTIMATE TRIP BUDGET
# =========================================

def estimate_budget(
    budget,
    days,
    travellers,
    accommodation,
    flexibility,
    emergency
):
    """Produce an illustrative split of the total trip budget."""

    total = max(0, budget)

    accommodation = (accommodation or "homestay").lower()
    flexibility = (flexibility or "strict").lower()
    emergency = (emergency or "no").lower()

    lodging_share = {
        "hostel": 0.25,
        "homestay": 0.30,
        "hotel": 0.38,
    }.get(accommodation, 0.30)

    food_share = 0.25
    transport_share = 0.20
    activity_share = 0.20

    if flexibility in ("flexible", "yes", "a little"):
        activity_share += 0.03
        transport_share -= 0.03

    emergency_share = 0.10 if emergency in ("yes", "true") else 0.0

    core_total = (
        lodging_share + food_share + transport_share + activity_share
    )
    available_for_core = total * (1 - emergency_share)

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


# =========================================
# FLASK ROUTES
# =========================================

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
        budget = clean_number(
            request.form.get("budget"), 0, 0, 100000000
        )

        if not destination:
            destination = "India"

        return render_template(
            "preferences.html",
            destination=destination,
            days=days,
            travellers=travellers,
            budget=budget,
        )

    return render_template(
        "preferences.html",
        destination="",
        days=1,
        travellers=1,
        budget=0,
    )


@app.route("/generate-itinerary", methods=["POST"])
def generate_itinerary():
    destination = (
        request.form.get("destination", "India").strip() or "India"
    )

    days = clean_number(request.form.get("days"), 1, 1, 30)
    travellers = clean_number(request.form.get("travellers"), 1, 1, 20)
    budget = clean_number(
        request.form.get("budget"), 0, 0, 100000000
    )

    budget_flexibility = request.form.get("budget_flexibility", "strict")
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

    (
        place_recommendations,
        stay_recommendations,
        budget_alternatives
    ) = get_destination_recommendations(destination, accommodation)

    has_recommendations = bool(
        place_recommendations or stay_recommendations
    )

    return render_template(
        "itinerary.html",
        itinerary=itinerary,
        destination=destination,
        region=region,
        days=days,
        travellers=travellers,
        budget=budget,
        budget_breakdown=budget_breakdown,
        pace=pace,
        accommodation=accommodation,
        travel_styles=travel_styles,
        place_recommendations=place_recommendations,
        stay_recommendations=stay_recommendations,
        budget_alternatives=budget_alternatives,
        has_recommendations=has_recommendations,
    )

@app.route("/get-stays", methods=["GET"])
def get_stays():
    destination = request.args.get("destination", "India")
    accommodation = request.args.get("accommodation", "hotel")

    allowed_types = ["hotel", "homestay", "hostel"]

    if accommodation not in allowed_types:
        return {"error": "Invalid accommodation type"}, 400

    _, stays, _ = get_destination_recommendations(
        destination,
        accommodation
    )

    return {"stays": stays}


# =========================================
# DOWNLOAD ITINERARY AS PDF
# =========================================

@app.route("/download-itinerary", methods=["POST"])
def download_itinerary():
    data = request.get_json(silent=True) or {}

    # Read and validate trip information
    destination = str(data.get("destination", "Your destination"))[:100]
    days = clean_number(data.get("days"), 1, 1, 30)
    travellers = clean_number(data.get("travellers"), 1, 1, 20)
    accommodation = str(data.get("accommodation", "Not specified"))[:50]
    pace = str(data.get("pace", "Not specified"))[:50]

    try:
        budget = max(0, float(data.get("budget", 0)))
        savings = max(0, float(data.get("savings", 0)))
    except (TypeError, ValueError):
        budget = 0
        savings = 0

    revised_budget = max(0, budget - savings)

    itinerary = data.get("itinerary", [])
    budget_categories = data.get("budget_categories", [])
    places = data.get("places", [])
    stays = data.get("stays", [])

    if not isinstance(itinerary, list):
        itinerary = []

    # Create an in-memory PDF
    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=f"WayWise Itinerary - {destination}",
        author="WayWise",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "WayWiseTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=27,
        leading=33,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#263746"),
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        "WayWiseSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#61717F"),
    )

    heading_style = ParagraphStyle(
        "WayWiseHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#42677D"),
        spaceBefore=12,
        spaceAfter=9,
    )

    body_style = ParagraphStyle(
        "WayWiseBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor("#303943"),
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "WayWiseSmall",
        parent=styles["BodyText"],
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#66717A"),
    )

    story = []

    def safe_paragraph(value, style=body_style):
        """Escape text before adding it to a ReportLab paragraph."""
        from xml.sax.saxutils import escape
        return Paragraph(escape(str(value or "")), style)

    def add_section_heading(text):
        story.append(Paragraph(text, heading_style))

    # Cover
    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph("WAYWISE.", title_style))
    story.append(Paragraph(
        "Plan Within Your Budget. Discover Beyond The Ordinary.",
        subtitle_style
    ))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph(
        f"Your Travel Journal for {escape(destination)}",
        ParagraphStyle(
            "DestinationTitle",
            parent=title_style,
            fontSize=21,
            leading=27,
        )
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "A personalised starting plan for your journey.",
        subtitle_style
    ))
    story.append(Spacer(1, 35 * mm))

    cover_details = [
        ["DURATION", f"{days} days"],
        ["TRAVELLERS", str(travellers)],
        ["ACCOMMODATION", accommodation.title()],
        ["TRAVEL PACE", pace.title()],
        ["ESTIMATED BUDGET", f"Rs. {revised_budget:,.0f}"],
    ]

    cover_table = Table(cover_details, colWidths=[55 * mm, 85 * mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#42677D")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#263746")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
    ]))

    story.append(cover_table)
    story.append(PageBreak())

    # Budget overview
    add_section_heading("Your Trip Budget")

    story.append(safe_paragraph(
        f"Original estimated budget: Rs. {budget:,.0f}"
    ))
    story.append(safe_paragraph(
        f"Potential savings applied: Rs. {savings:,.0f}"
    ))
    story.append(safe_paragraph(
        f"Revised estimated budget: Rs. {revised_budget:,.0f}"
    ))
    story.append(Spacer(1, 5 * mm))

    if isinstance(budget_categories, list) and budget_categories:
        budget_rows = [["CATEGORY", "ESTIMATED AMOUNT"]]

        for category in budget_categories:
            if not isinstance(category, dict):
                continue

            name = str(category.get("name", "Category"))[:80]

            try:
                amount = max(0, float(category.get("amount", 0)))
            except (TypeError, ValueError):
                amount = 0

            budget_rows.append([name, f"Rs. {amount:,.0f}"])

        budget_table = Table(
            budget_rows,
            colWidths=[100 * mm, 45 * mm],
            repeatRows=1
        )

        budget_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#42677D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F1F5F7")),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#303943")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ]))

        story.append(budget_table)

    story.append(Spacer(1, 8 * mm))
    story.append(safe_paragraph(
        "Budget figures are illustrative planning estimates, not live prices "
        "or guaranteed costs. Check current rates before booking.",
        small_style
    ))

    # Day-by-day itinerary
    story.append(PageBreak())
    add_section_heading("Your Day-by-Day Journey")

    for day in itinerary:
        if not isinstance(day, dict):
            continue

        day_number = day.get("day", "")
        day_title = day.get("title", "")

        story.append(Paragraph(
            f"Day {day_number}: {escape(str(day_title))}",
            heading_style
        ))

        activities = day.get("activities", [])

        if isinstance(activities, list):
            for activity in activities:
                if not isinstance(activity, dict):
                    continue

                activity_time = activity.get("time", "Activity")
                activity_text = activity.get("activity", "")

                story.append(safe_paragraph(
                    f"<b>{escape(str(activity_time))}</b> — "
                    f"{escape(str(activity_text))}"
                ))

        if day.get("tip"):
            story.append(safe_paragraph(
                f"<b>WayWise tip:</b> {day['tip']}"
            ))

        story.append(Spacer(1, 5 * mm))

    # Places to discover
    if isinstance(places, list) and places:
        story.append(PageBreak())
        add_section_heading("Places Worth Discovering")

        for place in places:
            if not isinstance(place, dict):
                continue

            story.append(Paragraph(
                f"<b>{escape(str(place.get('name', '')))}</b>",
                body_style
            ))
            story.append(safe_paragraph(place.get("description", "")))
            story.append(safe_paragraph(
                f"{place.get('type', 'Discovery')} | "
                f"{place.get('area', '')}",
                small_style
            ))
            story.append(Spacer(1, 3 * mm))

    # Accommodation recommendations
    if isinstance(stays, list) and stays:
        add_section_heading("Stays to Explore")

        for stay in stays:
            if not isinstance(stay, dict):
                continue

            story.append(Paragraph(
                f"<b>{escape(str(stay.get('name', '')))}</b>",
                body_style
            ))
            story.append(safe_paragraph(stay.get("best_for", "")))
            story.append(safe_paragraph(
                f"{stay.get('type', '')} | {stay.get('area', '')}",
                small_style
            ))

            if stay.get("url"):
                story.append(safe_paragraph(
                    f"Explore: {stay['url']}",
                    small_style
                ))

            story.append(Spacer(1, 3 * mm))

    # Footer note
    story.append(Spacer(1, 10 * mm))
    story.append(safe_paragraph(
        "Travel thoughtfully. Support local businesses. Leave room for "
        "unexpected discoveries.",
        small_style
    ))

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#7A8790"))
        canvas.drawString(20 * mm, 12 * mm, "WAYWISE. | Your Travel Journal")
        canvas.drawRightString(
            A4[0] - 20 * mm,
            12 * mm,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    pdf_buffer.seek(0)

    filename = (
        re.sub(r"[^a-zA-Z0-9-]+", "-", destination).strip("-").lower()
        or "trip"
    )

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"waywise-{filename}-itinerary.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
