"""Wandr tools: safety lookup, itinerary builder, local tips and live weather for solo travellers.

Data: synthetic destinations and ratings (works offline, deterministic for tests and the demo)
plus open-meteo for live weather (free, no API key needed).
Keep the one-line docstring on each tool: the model reads it, and the tool-selection pattern
uses it as the option description.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any

from strands import tool

# ---------------------------------------------------------------------------
# Synthetic data: destinations, safety ratings and itinerary templates
# ---------------------------------------------------------------------------

DESTINATIONS: dict[str, dict[str, Any]] = {
    "bangkok": {
        "country": "Thailand", "region": "Southeast Asia",
        "safety": {"overall": 7, "solo_female": 6, "solo_male": 8},
        "tips": [
            "Register with your country's embassy before arrival.",
            "Keep a copy of your passport in your accommodation.",
            "Use metered taxis or Grab — avoid unmarked cabs.",
            "Dress modestly when visiting temples.",
            "The BTS Skytrain is safe and easy to navigate solo.",
        ],
        "highlights": ["Grand Palace", "Chatuchak Weekend Market", "Khao San Road", "Wat Pho", "Floating Markets"],
        "budget_per_day_usd": {"budget": 30, "mid": 60, "comfort": 120},
        "best_months": ["Nov", "Dec", "Jan", "Feb"],
        "lat": 13.7563, "lon": 100.5018,
    },
    "lisbon": {
        "country": "Portugal", "region": "Europe",
        "safety": {"overall": 9, "solo_female": 9, "solo_male": 9},
        "tips": [
            "Lisbon is one of the safest capitals in Europe for solo travellers.",
            "Watch for pickpockets in Alfama and on tram 28.",
            "The Zapping card works on all public transport.",
            "Many locals speak English, especially in the centre.",
            "Hills are steep — wear comfortable shoes.",
        ],
        "highlights": ["Belém Tower", "Alfama district", "LX Factory", "Sintra day trip", "Time Out Market"],
        "budget_per_day_usd": {"budget": 50, "mid": 100, "comfort": 180},
        "best_months": ["Mar", "Apr", "May", "Sep", "Oct"],
        "lat": 38.7169, "lon": -9.1399,
    },
    "tokyo": {
        "country": "Japan", "region": "East Asia",
        "safety": {"overall": 10, "solo_female": 10, "solo_male": 10},
        "tips": [
            "Tokyo is one of the safest cities in the world.",
            "Get a Suica or Pasmo card for seamless transit.",
            "Google Translate camera mode handles menus and signs.",
            "7-Eleven and FamilyMart ATMs accept foreign cards.",
            "Tattoos may restrict access to some onsen — check in advance.",
        ],
        "highlights": ["Shinjuku", "Shibuya Crossing", "Senso-ji Temple", "Tsukiji Outer Market", "teamLab Borderless"],
        "budget_per_day_usd": {"budget": 60, "mid": 120, "comfort": 250},
        "best_months": ["Mar", "Apr", "Oct", "Nov"],
        "lat": 35.6762, "lon": 139.6503,
    },
    "medellín": {
        "country": "Colombia", "region": "South America",
        "safety": {"overall": 6, "solo_female": 5, "solo_male": 6},
        "tips": [
            "Stick to El Poblado and Laureles neighbourhoods at night.",
            "Use InDrive or Uber rather than hailing taxis on the street.",
            "Share your itinerary with someone back home daily.",
            "The cable car to Santo Domingo is safe and has great views.",
            "Learn basic Spanish phrases — English is limited outside tourist areas.",
        ],
        "highlights": ["Pablo Escobar tour (educational)", "Metrocable", "Parque Arví", "El Centro", "Guatapé day trip"],
        "budget_per_day_usd": {"budget": 25, "mid": 55, "comfort": 110},
        "best_months": ["Dec", "Jan", "Feb", "Mar"],
        "lat": 6.2442, "lon": -75.5812,
    },
    "reykjavik": {
        "country": "Iceland", "region": "Northern Europe",
        "safety": {"overall": 10, "solo_female": 10, "solo_male": 10},
        "tips": [
            "Iceland is among the safest countries on earth.",
            "Rent a car to explore the Ring Road at your own pace.",
            "Weather changes fast — layer up even in summer.",
            "Northern lights are visible Sep–Mar outside the city.",
            "Tap water is among the purest in the world — no need to buy bottles.",
        ],
        "highlights": ["Blue Lagoon", "Golden Circle", "Hallgrímskirkja", "Northern Lights", "Whale watching"],
        "budget_per_day_usd": {"budget": 100, "mid": 200, "comfort": 400},
        "best_months": ["Jun", "Jul", "Aug", "Sep"],
        "lat": 64.1355, "lon": -21.8954,
    },
}

# Itinerary templates per destination (3-day and 5-day)
ITINERARIES: dict[str, dict[int, list[dict[str, str]]]] = {
    "bangkok": {
        3: [
            {"day": 1, "theme": "Temples and the Old City", "morning": "Grand Palace and Wat Phra Kaew", "afternoon": "Wat Pho and the reclining Buddha", "evening": "Dinner on Khaosan Road, rooftop bar at Sky Bar"},
            {"day": 2, "theme": "Markets and Local Life", "morning": "Chatuchak Weekend Market (Sat/Sun) or Or Tor Kor fresh market", "afternoon": "Jim Thompson House, MBK shopping", "evening": "Chinatown street food on Yaowarat Road"},
            {"day": 3, "theme": "River and Temples", "morning": "Chao Phraya Express Boat, Wat Arun", "afternoon": "Floating market day trip or Damnoen Saduak", "evening": "Farewell dinner in Silom"},
        ],
        5: [
            {"day": 1, "theme": "Arrive and Orient", "morning": "Check in, rest", "afternoon": "Khao San Road area, Sanam Luang park", "evening": "Street food wander in Banglamphu"},
            {"day": 2, "theme": "Temples and the Old City", "morning": "Grand Palace and Wat Phra Kaew", "afternoon": "Wat Pho", "evening": "Sky Bar rooftop drinks"},
            {"day": 3, "theme": "Markets", "morning": "Chatuchak (Sat/Sun) or Damnoen Saduak floating market", "afternoon": "MBK or Siam Paragon", "evening": "Chinatown (Yaowarat)"},
            {"day": 4, "theme": "River Day", "morning": "Chao Phraya boat, Wat Arun", "afternoon": "Jim Thompson House, Lumpini Park", "evening": "Jazz bar in Silom"},
            {"day": 5, "theme": "Day Trip", "morning": "Day trip to Ayutthaya ancient ruins", "afternoon": "Return, last-minute shopping", "evening": "Departure prep"},
        ],
    },
    "lisbon": {
        3: [
            {"day": 1, "theme": "Alfama and the Waterfront", "morning": "São Jorge Castle, Alfama viewpoints", "afternoon": "LX Factory", "evening": "Fado show in a local tasca"},
            {"day": 2, "theme": "Belém and Pastéis", "morning": "Belém Tower, Jerónimos Monastery", "afternoon": "Pastéis de Belém, electric tram ride", "evening": "Time Out Market for dinner"},
            {"day": 3, "theme": "Sintra Day Trip", "morning": "Train to Sintra, Pena Palace", "afternoon": "Quinta da Regaleira", "evening": "Return, wine bar in Bairro Alto"},
        ],
        5: [
            {"day": 1, "theme": "Arrive and Explore", "morning": "Check in, Baixa neighbourhood walk", "afternoon": "Praça do Comércio, riverside", "evening": "Dinner in Chiado"},
            {"day": 2, "theme": "Alfama", "morning": "São Jorge Castle, Alfama alleyways", "afternoon": "Museu do Azulejo", "evening": "Fado in Alfama"},
            {"day": 3, "theme": "Belém", "morning": "Belém Tower, Jerónimos Monastery", "afternoon": "MAAT Museum, pastéis", "evening": "LX Factory night market (Fri/Sat)"},
            {"day": 4, "theme": "Sintra", "morning": "Pena Palace, Sintra old town", "afternoon": "Quinta da Regaleira", "evening": "Back in Lisbon, Bairro Alto wine bars"},
            {"day": 5, "theme": "Beaches", "morning": "Train to Cascais or Estoril beach", "afternoon": "Seafood lunch, relax", "evening": "Farewell sunset at Miradouro da Graça"},
        ],
    },
    "tokyo": {
        3: [
            {"day": 1, "theme": "East Tokyo", "morning": "Senso-ji Temple in Asakusa", "afternoon": "Akihabara electronics district", "evening": "Shibuya crossing, ramen in Shinjuku"},
            {"day": 2, "theme": "West Tokyo", "morning": "Harajuku Takeshita Street, Meiji Shrine", "afternoon": "Omotesando boutiques", "evening": "Golden Gai bar crawl in Shinjuku"},
            {"day": 3, "theme": "Art and Views", "morning": "teamLab Borderless (book ahead)", "afternoon": "Odaiba waterfront", "evening": "Tokyo Skytree sunset views"},
        ],
        5: [
            {"day": 1, "theme": "Arrive", "morning": "Narita/Haneda → hotel", "afternoon": "Shibuya crossing, Hachiko statue", "evening": "Ichiran ramen solo booth"},
            {"day": 2, "theme": "Classic Tokyo", "morning": "Senso-ji, Nakamise shopping street", "afternoon": "Ueno Park and museums", "evening": "Akihabara night walk"},
            {"day": 3, "theme": "Pop Culture", "morning": "Harajuku, Meiji Shrine", "afternoon": "Omotesando, Omohara Woods", "evening": "Shinjuku Golden Gai"},
            {"day": 4, "theme": "Day Trip", "morning": "Nikko or Kamakura (Great Buddha)", "afternoon": "Return by train", "evening": "Ginza dinner"},
            {"day": 5, "theme": "Art and Farewell", "morning": "teamLab Borderless", "afternoon": "Odaiba, last shopping", "evening": "Tokyo Skytree, early night for departure"},
        ],
    },
    "medellín": {
        3: [
            {"day": 1, "theme": "El Poblado", "morning": "Parque Lleras, Poblado streets", "afternoon": "Pablo Escobar neighbourhood tour", "evening": "El Poblado nightlife"},
            {"day": 2, "theme": "Metrocable", "morning": "Metro to Acevedo, Metrocable to Santo Domingo", "afternoon": "Parque Arví by cable car", "evening": "Laureles neighbourhood dinner"},
            {"day": 3, "theme": "Guatapé Day Trip", "morning": "Bus to Guatapé, El Peñol rock climb (740 steps)", "afternoon": "Colourful village walk, boat tour", "evening": "Return to Medellín"},
        ],
        5: [
            {"day": 1, "theme": "Arrive", "morning": "Check in to El Poblado", "afternoon": "Parque Lleras orientation walk", "evening": "Street food in El Hueco"},
            {"day": 2, "theme": "History", "morning": "Plaza Botero, Antioquia Museum", "afternoon": "Pablo Escobar tour", "evening": "El Centro bars"},
            {"day": 3, "theme": "Cable Car", "morning": "Metrocable Line K to Santo Domingo", "afternoon": "Parque Arví eco-park", "evening": "Laureles dinner"},
            {"day": 4, "theme": "Guatapé", "morning": "Bus to Guatapé, El Peñol", "afternoon": "Village walk", "evening": "Return"},
            {"day": 5, "theme": "Relaxed Exit", "morning": "Botanical Garden", "afternoon": "Last shopping in El Centro", "evening": "Farewell dinner in Provenza"},
        ],
    },
    "reykjavik": {
        3: [
            {"day": 1, "theme": "City", "morning": "Hallgrímskirkja tower, Tjörnin lake", "afternoon": "Harpa Concert Hall, Old Harbour", "evening": "Reykjavik craft beer bars"},
            {"day": 2, "theme": "Golden Circle", "morning": "Þingvellir National Park", "afternoon": "Geysir hot springs, Gullfoss waterfall", "evening": "Return, northern lights hunt (Sep–Mar)"},
            {"day": 3, "theme": "Blue Lagoon", "morning": "Blue Lagoon geothermal spa (book ahead)", "afternoon": "Return to city, last shopping on Laugavegur", "evening": "Seafood dinner at Grillmarkaðurinn"},
        ],
        5: [
            {"day": 1, "theme": "Arrive", "morning": "Keflavík airport to Reykjavik", "afternoon": "Laugavegur street walk", "evening": "Fish and chips at Reykjavik's harbour"},
            {"day": 2, "theme": "City Culture", "morning": "Hallgrímskirkja, National Museum", "afternoon": "Tjörnin, Harpa Hall", "evening": "Microbrewery tour"},
            {"day": 3, "theme": "Golden Circle", "morning": "Þingvellir", "afternoon": "Geysir, Gullfoss", "evening": "Kerid Crater, northern lights"},
            {"day": 4, "theme": "South Coast", "morning": "Seljalandsfoss waterfall (walk behind it)", "afternoon": "Skógafoss, black sand beach at Reynisfjara", "evening": "Return"},
            {"day": 5, "theme": "Blue Lagoon and Depart", "morning": "Blue Lagoon", "afternoon": "Keflavík airport", "evening": "Depart"},
        ],
    },
}

LOCAL_TIPS: dict[str, list[str]] = {
    "bangkok": [
        "Tonight: rooftop happy hour at The Nest or Sky Bar, cocktails from 5 PM.",
        "Street food pick: boat noodles at Victory Monument, open until midnight.",
        "Hidden gem: the Lhong 1919 riverside art space — quieter than the usual tourist spots.",
        "Practical: 7-Eleven sells Chang beer cheaper than any bar; drink it by the river.",
        "Transport: the BTS Skytrain runs until midnight; keep your card topped up.",
    ],
    "lisbon": [
        "Tonight: ginjinha (cherry liqueur) at A Ginjinha on Largo de São Domingos — tiny shot, big experience.",
        "Food: pastel de nata from Pastéis de Belém or Manteigaria — join the queue, it's worth it.",
        "Hidden gem: Miradouro da Graça at sunset — fewer tourists than São Pedro de Alcântara.",
        "Practical: the Lisboa Card gives free museum entry and all-day transport from €21.",
        "Walk: the Mouraria neighbourhood is Lisbon's oldest and most authentic — wear comfy shoes.",
    ],
    "tokyo": [
        "Tonight: Golden Gai in Shinjuku — tiny bars each fitting 8 people, open until 5 AM.",
        "Food: depachika (basement food halls) in any department store — try Isetan in Shinjuku.",
        "Hidden gem: Yanaka old town — unchanged since the Edo period, no tourist crowds.",
        "Practical: combini (convenience stores) have ATMs that accept foreign cards and incredible food.",
        "Practical: buy a Suica card at any JR station — tap in and out on trains and buses.",
    ],
    "medellín": [
        "Tonight: El Poblado's Parque Lleras area — dozens of bars in a three-block radius.",
        "Food: bandeja paisa at a local fritanga — Colombia's iconic mixed grill platter.",
        "Hidden gem: Cerro Nutibara hilltop park with panoramic city views and a replica colonial village.",
        "Practical: InDrive is safer than street taxis; agree the price before getting in.",
        "Practical: keep your phone in your pocket in crowds — petty theft is the main risk.",
    ],
    "reykjavik": [
        "Tonight: check the Aurora Forecast app — if it says 4+, drive 20 min outside the city.",
        "Food: hot dog from Bæjarins Beztu Pylsur — the most famous hot dog stand in Iceland, open late.",
        "Hidden gem: Grótta lighthouse at the peninsula tip — peaceful sunset spot with sea views.",
        "Practical: tap water is glacial and delicious — never buy bottled water here.",
        "Practical: book Blue Lagoon and popular restaurants well in advance; they sell out weeks ahead.",
    ],
}


def _normalise(destination: str) -> str:
    return destination.lower().strip().rstrip(".,!?")


def _find_destination(destination: str) -> str | None:
    key = _normalise(destination)
    if key in DESTINATIONS:
        return key
    for k in DESTINATIONS:
        if k in key or key in k:
            return k
    return None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def check_safety(destination: str) -> dict:
    """Check solo travel safety rating and essential tips for a destination."""
    key = _find_destination(destination)
    if not key:
        return {
            "destination": destination,
            "note": "Destination not in database. General advice: research FCO/State Dept advisories, register with your embassy, and use licensed transport.",
            "available_destinations": list(DESTINATIONS.keys()),
        }
    d = DESTINATIONS[key]
    s = d["safety"]
    return {
        "destination": key.title(),
        "country": d["country"],
        "region": d["region"],
        "safety_score_overall": f"{s['overall']}/10",
        "safety_score_solo_female": f"{s['solo_female']}/10",
        "safety_score_solo_male": f"{s['solo_male']}/10",
        "essential_tips": d["tips"],
        "best_travel_months": d["best_months"],
    }



@tool
def build_itinerary(destination: str, days: int = 3, budget_level: str = "mid") -> dict:
    """Build a day-by-day solo travel itinerary for a destination with budget estimate."""
    key = _find_destination(destination)
    if not key:
        return {
            "destination": destination,
            "note": "Destination not in database. Try: Bangkok, Lisbon, Tokyo, Medellín, Reykjavik.",
        }

    d = DESTINATIONS[key]
    days_clamped = max(1, min(int(days), 5))
    budget_key = (
        budget_level.lower()
        if budget_level.lower() in d["budget_per_day_usd"]
        else "mid"
    )
    daily_budget = d["budget_per_day_usd"][budget_key]

    templates = ITINERARIES.get(key, {})
    if days_clamped <= 3:
        itinerary = templates.get(3, [])[:days_clamped]
    else:
        itinerary = templates.get(5, [])[:days_clamped]

    return {
        "destination": key.title(),
        "country": d["country"],
        "days": days_clamped,
        "budget_level": budget_key,
        "estimated_daily_budget_usd": daily_budget,
        "estimated_total_usd": daily_budget * days_clamped,
        "highlights": d["highlights"],
        "itinerary": itinerary,
    }



@tool
def get_local_tips(destination: str) -> dict:
    """Get real-time local tips — things to do, eat and see right now at a destination."""
    key = _find_destination(destination)
    if not key:
        return {
            "destination": destination,
            "note": "Destination not in database. Try: Bangkok, Lisbon, Tokyo, Medellín, Reykjavik.",
        }
    d = DESTINATIONS[key]
    return {
        "destination": key.title(),
        "country": d["country"],
        "local_tips": LOCAL_TIPS.get(key, []),
        "top_highlights": d["highlights"][:3],
    }


@tool
def get_weather(destination: str) -> dict:
    """Get current weather and 3-day forecast for a destination (live data via open-meteo)."""
    key = _find_destination(destination)
    if not key:
        return {"destination": destination, "note": "Destination not in database for coordinates. Try: Bangkok, Lisbon, Tokyo, Medellín, Reykjavik."}
    d = DESTINATIONS[key]
    lat, lon = d["lat"], d["lon"]
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weathercode,windspeed_10m,precipitation"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum"
        f"&timezone=auto&forecast_days=3"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        current = data.get("current", {})
        daily = data.get("daily", {})
        forecast = []
        for i in range(len(daily.get("time", []))):
            forecast.append({
                "date": daily["time"][i],
                "max_c": daily["temperature_2m_max"][i],
                "min_c": daily["temperature_2m_min"][i],
                "precipitation_mm": daily["precipitation_sum"][i],
            })
        return {
            "destination": key.title(),
            "country": d["country"],
            "current": {
                "temperature_c": current.get("temperature_2m"),
                "windspeed_kmh": current.get("windspeed_10m"),
                "precipitation_mm": current.get("precipitation"),
            },
            "forecast_3_day": forecast,
        }
    except Exception as exc:
        return {"destination": key.title(), "error": f"Weather unavailable: {exc}. Check https://open-meteo.com manually."}


TOOLS = [check_safety, build_itinerary, get_local_tips, get_weather]
