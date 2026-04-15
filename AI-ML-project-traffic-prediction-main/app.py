"""
Bengaluru Traffic Flow Predictor – app.py
==========================================
Features:
 • Data-driven predictions (45k real records)
 • Strict Bengaluru-only location validation
 • Weather input (manual + optional OpenWeatherMap auto-detect)
 • 7-Day Forecast View
 • Indian Public Holiday detection
"""

import json, os, requests as req_lib
import joblib
from flask import Flask, render_template, request, jsonify
from holidays import get_today_holiday, get_holiday_multiplier, HOLIDAYS
from config import OPENWEATHER_API_KEY, OPENWEATHER_CITY, OPENWEATHER_URL

app = Flask(__name__)

# ── Real traffic data ─────────────────────────────────────────────────────────
DATA_FILE  = os.path.join(os.path.dirname(__file__), "traffic_data.json")
with open(DATA_FILE) as _f:
    INTENSITIES = json.load(_f)["intensities"]

# Load the Machine Learning Model
try:
    ML_MODEL = joblib.load(os.path.join(os.path.dirname(__file__), "traffic_model.pkl"))
    print("SUCCESS: ML Model 'traffic_model.pkl' loaded successfully.")
except Exception as e:
    print(f"WARNING: Could not load ML model: {e}")
    ML_MODEL = None

# ── Location database ─────────────────────────────────────────────────────────
LOCATION_DB = {
    "whitefield":              ("Whitefield",           "IT & Tech Zone",    "it"),
    "electronic city":         ("Electronic City",      "IT & Tech Zone",    "it"),
    "ecity":                   ("Electronic City",      "IT & Tech Zone",    "it"),
    "marathahalli":            ("Marathahalli",          "IT & Tech Zone",    "it"),
    "bellandur":               ("Bellandur",             "IT & Tech Zone",    "it"),
    "sarjapur":                ("Sarjapur Road",         "IT & Tech Zone",    "it"),
    "sarjapur road":           ("Sarjapur Road",         "IT & Tech Zone",    "it"),
    "itpl":                    ("ITPL",                  "IT & Tech Zone",    "it"),
    "hsr layout":              ("HSR Layout",            "IT & Tech Zone",    "it"),
    "hsr":                     ("HSR Layout",            "IT & Tech Zone",    "it"),
    "domlur":                  ("Domlur",                "IT & Tech Zone",    "it"),
    "bagmane":                 ("Bagmane Tech Park",     "IT & Tech Zone",    "it"),
    "outer ring road":         ("Outer Ring Road",       "IT & Tech Zone",    "it"),
    "orr":                     ("Outer Ring Road",       "IT & Tech Zone",    "it"),
    "mg road":                 ("MG Road",               "Commercial Zone",   "comm"),
    "brigade road":            ("Brigade Road",          "Commercial Zone",   "comm"),
    "brigade":                 ("Brigade Road",          "Commercial Zone",   "comm"),
    "indiranagar":             ("Indiranagar",            "Commercial Zone",   "comm"),
    "church street":           ("Church Street",          "Commercial Zone",   "comm"),
    "commercial street":       ("Commercial Street",      "Commercial Zone",   "comm"),
    "ulsoor":                  ("Ulsoor",                 "Commercial Zone",   "comm"),
    "richmond road":           ("Richmond Road",          "Commercial Zone",   "comm"),
    "lavelle road":            ("Lavelle Road",           "Commercial Zone",   "comm"),
    "cunningham road":         ("Cunningham Road",        "Commercial Zone",   "comm"),
    "koramangala":             ("Koramangala",            "Commercial Zone",   "comm"),
    "kormangala":              ("Koramangala",            "Commercial Zone",   "comm"),
    "silk board":              ("Silk Board",             "Commercial Zone",   "comm"),
    "forum mall":              ("Koramangala",            "Commercial Zone",   "comm"),
    "yelahanka":               ("Yelahanka",              "Residential Zone",  "res"),
    "rr nagar":                ("RR Nagar",               "Residential Zone",  "res"),
    "malleshwaram":            ("Malleshwaram",            "Residential Zone",  "res"),
    "jayanagar":               ("Jayanagar",               "Residential Zone",  "res"),
    "basavanagudi":            ("Basavanagudi",            "Residential Zone",  "res"),
    "banashankari":            ("Banashankari",            "Residential Zone",  "res"),
    "rajajinagar":             ("Rajajinagar",             "Residential Zone",  "res"),
    "vijayanagar":             ("Vijayanagar",             "Residential Zone",  "res"),
    "padmanabhanagar":         ("Padmanabhanagar",         "Residential Zone",  "res"),
    "kuvempu nagar":           ("Kuvempu Nagar",           "Residential Zone",  "res"),
    "nagarbhavi":              ("Nagarbhavi",              "Residential Zone",  "res"),
    "mathikere":               ("Mathikere",               "Residential Zone",  "res"),
    "dollars colony":          ("Dollars Colony",          "Residential Zone",  "res"),
    "thanisandra":             ("Thanisandra",             "Residential Zone",  "res"),
    "devanahalli":             ("Devanahalli",             "Residential Zone",  "res"),
    "btm layout":              ("BTM Layout",             "Mixed Zone",        "mix"),
    "btm":                     ("BTM Layout",             "Mixed Zone",        "mix"),
    "jp nagar":                ("JP Nagar",               "Mixed Zone",        "mix"),
    "j p nagar":               ("JP Nagar",               "Mixed Zone",        "mix"),
    "yeshwanthpur":            ("Yeshwanthpur",            "Mixed Zone",        "mix"),
    "hebbal":                  ("Hebbal",                  "Mixed Zone",        "mix"),
    "shivajinagar":            ("Shivajinagar",            "Mixed Zone",        "mix"),
    "kr puram":                ("KR Puram",                "Mixed Zone",        "mix"),
    "kr market":               ("KR Market",               "Mixed Zone",        "mix"),
    "kengeri":                 ("Kengeri",                 "Mixed Zone",        "mix"),
    "rt nagar":                ("RT Nagar",                "Mixed Zone",        "mix"),
    "rt nagara":               ("RT Nagar",                "Mixed Zone",        "mix"),
    "electronic city phase 1": ("Electronic City Ph-1",   "Mixed Zone",        "mix"),
    "electronic city phase 2": ("Electronic City Ph-2",   "Mixed Zone",        "mix"),
    "cox town":                ("Cox Town",                "Mixed Zone",        "mix"),
    "frazer town":             ("Frazer Town",             "Mixed Zone",        "mix"),
    "fraser town":             ("Frazer Town",             "Mixed Zone",        "mix"),
    "peenya":                  ("Peenya",                  "Mixed Zone",        "mix"),
    "nelamangala":             ("Nelamangala",             "Mixed Zone",        "mix"),
    "tumkur road":             ("Tumkur Road",             "Mixed Zone",        "mix"),
    "bannerghatta road":       ("Bannerghatta Road",       "Mixed Zone",        "mix"),
    "bannerghatta":            ("Bannerghatta Road",       "Mixed Zone",        "mix"),
    "hennur":                  ("Hennur",                  "Mixed Zone",        "mix"),
    "kalyan nagar":            ("Kalyan Nagar",            "Mixed Zone",        "mix"),
    "banaswadi":               ("Banaswadi",               "Mixed Zone",        "mix"),
    "ramamurthy nagar":        ("Ramamurthy Nagar",        "Mixed Zone",        "mix"),
    "hoodi":                   ("Hoodi",                   "Mixed Zone",        "mix"),
    "kadugodi":                ("Kadugodi",                "Mixed Zone",        "mix"),
    "horamavu":                ("Horamavu",                "Mixed Zone",        "mix"),
    "tc palya":                ("TC Palya",                "Mixed Zone",        "mix"),
    "nagawara":                ("Nagawara",                "Mixed Zone",        "mix"),
    "yelahanka new town":      ("Yelahanka New Town",      "Mixed Zone",        "mix"),
    "kogilu":                  ("Kogilu",                  "Mixed Zone",        "mix"),
    "bagalur":                 ("Bagalur",                 "Mixed Zone",        "mix"),
    "jakkur":                  ("Jakkur",                  "Mixed Zone",        "mix"),
    "lottegollahalli":         ("Lottegollahalli",         "Mixed Zone",        "mix"),
}

# Flat list of display names for autocomplete (sent to frontend)
LOCATION_NAMES = sorted({v[0] for v in LOCATION_DB.values()})

# ── Zone profiles ─────────────────────────────────────────────────────────────
ZONE_PROFILE = {
    "it":   {"weekday_peak_boost": 1.18, "late_night_factor": 0.85, "weekend_factor": 0.70},
    "comm": {"weekday_peak_boost": 1.10, "late_night_factor": 0.90, "weekend_factor": 0.85},
    "res":  {"weekday_peak_boost": 0.92, "late_night_factor": 0.80, "weekend_factor": 0.75},
    "mix":  {"weekday_peak_boost": 1.00, "late_night_factor": 0.88, "weekend_factor": 0.80},
}

PEAK_HOURS_WEEKDAY = {7, 8, 9, 17, 18, 19, 20}
LATE_NIGHT_HOURS   = {0, 1, 2, 3, 4}

DAY_CFG = {
    "Monday":    {"day_type": "Weekday", "scale": 1.05},
    "Tuesday":   {"day_type": "Weekday", "scale": 1.00},
    "Wednesday": {"day_type": "Weekday", "scale": 1.02},
    "Thursday":  {"day_type": "Weekday", "scale": 1.04},
    "Friday":    {"day_type": "Weekday", "scale": 1.12},
    "Saturday":  {"day_type": "Weekend", "scale": 0.90},
    "Sunday":    {"day_type": "Weekend", "scale": 0.78},
}

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ── Weather ───────────────────────────────────────────────────────────────────
WEATHER_CONFIG = {
    "clear":        {"label": "Clear",        "icon": "☀️",  "multiplier": 1.00},
    "light_rain":   {"label": "Light Rain",   "icon": "🌧️", "multiplier": 1.15},
    "heavy_rain":   {"label": "Heavy Rain",   "icon": "⛈️", "multiplier": 1.28},
    "fog":          {"label": "Fog / Mist",   "icon": "🌫️", "multiplier": 1.20},
    "thunderstorm": {"label": "Thunderstorm", "icon": "⚡",  "multiplier": 1.32},
}

# OpenWeatherMap condition → our internal key
OWM_MAP = {
    "Clear":        "clear",
    "Clouds":       "clear",
    "Rain":         "light_rain",
    "Drizzle":      "light_rain",
    "Thunderstorm": "thunderstorm",
    "Fog":          "fog",
    "Mist":         "fog",
    "Haze":         "fog",
    "Smoke":        "fog",
    "Dust":         "fog",
    "Sand":         "fog",
    "Snow":         "clear",  # won't snow in Bengaluru
    "Squall":       "heavy_rain",
    "Tornado":      "thunderstorm",
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_hour(h):
    if h == 0:  return "12 AM"
    if h == 12: return "12 PM"
    if h < 12:  return f"{h} AM"
    return f"{h % 12} PM"


def group_hours(hour_list):
    if not hour_list:
        return "None"
    hours = sorted(set(hour_list))
    groups, start, end = [], hours[0], hours[0]
    for h in hours[1:]:
        if h == end + 1:
            end = h
        else:
            groups.append((start, end))
            start = end = h
    groups.append((start, end))
    parts = []
    for s, e in groups:
        parts.append(fmt_hour(s) if s == e else f"{fmt_hour(s)} – {fmt_hour(e)}")
    return ",  ".join(parts)


def lookup_location(text):
    t = text.lower().strip()
    if t in LOCATION_DB:
        return LOCATION_DB[t]
    for key in sorted(LOCATION_DB.keys(), key=len, reverse=True):
        if key in t:
            return LOCATION_DB[key]
    return None, None, None


def compute_hourly(day_name, zone_id, weather_key, holiday=None):
    # Convert day_name to integer (0=Mon, 6=Sun)
    day_idx = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day_name)
    
    # Map weather_key to ML weather_code (0=Clear, 1=Rain, 2=Thunder, 3=Fog)
    wx_map_to_code = {"clear": 0, "light_rain": 1, "heavy_rain": 1, "thunderstorm": 2, "fog": 3}
    wx_code = wx_map_to_code.get(weather_key, 0)
    
    # Map zone string to numeric ID for ML (0=IT, 1=Com, 2=Res, 3=Mix)
    zone_map = {"it": 0, "com": 1, "res": 2, "mix": 3}
    ml_zone_id = zone_map.get(zone_id, 3)
    
    is_hol = 1 if holiday else 0

    hourly = []
    
    # If model failed to load, fallback to 0 (should not happen in prod)
    if ML_MODEL is None:
        for hour in range(24):
            hourly.append({
                "hour": hour, "label": fmt_hour(hour),
                "level": 0, "level_name": "Error",
                "color": "#9ca3af", "intensity": 0,
            })
        return hourly

    for hour in range(24):
        # Predict using RandomForestRegressor
        features = [[hour, day_idx, ml_zone_id, wx_code, is_hol]]
        pred_val = ML_MODEL.predict(features)[0]
        
        intensity = round(pred_val, 1)
        intensity = round(max(2, min(intensity, 98)), 1)

        if intensity >= 65:
            level, level_name, color = 2, "High",   "#ef4444"
        elif intensity >= 35:
            level, level_name, color = 1, "Medium", "#f97316"
        else:
            level, level_name, color = 0, "Low",    "#22c55e"

        hourly.append({
            "hour": hour, "label": fmt_hour(hour),
            "level": level, "level_name": level_name,
            "color": color, "intensity": intensity,
        })
    return hourly


def day_summary(day_name, zone_id, weather_key, holiday=None):
    hourly = compute_hourly(day_name, zone_id, weather_key, holiday)
    vals   = [d["intensity"] for d in hourly]
    low    = [d["hour"] for d in hourly if d["level"] == 0]
    avg    = round(sum(vals) / 24, 1)
    badge  = "Heavy" if avg >= 60 else "Moderate" if avg >= 40 else "Light"
    badge_color = "#ef4444" if avg >= 60 else "#f97316" if avg >= 40 else "#22c55e"
    return {
        "day_name": day_name, "day_short": day_name[:3],
        "day_type": DAY_CFG.get(day_name, {}).get("day_type", "Weekday"),
        "avg": avg, "peak": max(vals), "low": min(vals),
        "best_time": group_hours(low[:4]) if low else "—",
        "badge": badge, "badge_color": badge_color, "spark": vals,
    }


# ── API: Real-time Bengaluru weather (OpenWeatherMap) ─────────────────────────
@app.route("/api/weather")
def api_weather():
    if not OPENWEATHER_API_KEY:
        return jsonify({"error": "no_key",
                        "message": "Add your free API key to config.py"}), 503
    try:
        resp = req_lib.get(OPENWEATHER_URL, params={
            "q": OPENWEATHER_CITY,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }, timeout=5)
        resp.raise_for_status()
        data       = resp.json()
        owm_main   = data["weather"][0]["main"]
        owm_desc   = data["weather"][0]["description"].title()
        temp_c     = round(data["main"]["temp"])
        humidity   = data["main"]["humidity"]
        wx_key     = OWM_MAP.get(owm_main, "clear")
        wx_cfg     = WEATHER_CONFIG[wx_key]
        return jsonify({
            "weather_key":   wx_key,
            "weather_label": wx_cfg["label"],
            "weather_icon":  wx_cfg["icon"],
            "multiplier":    wx_cfg["multiplier"],
            "owm_desc":      owm_desc,
            "temp_c":        temp_c,
            "humidity":      humidity,
        })
    except Exception as exc:
        return jsonify({"error": "fetch_failed", "message": str(exc)}), 502


# ── API: Autocomplete suggestions ─────────────────────────────────────────────
@app.route("/api/suggest")
def api_suggest():
    q = request.args.get("q", "").lower().strip()
    if len(q) < 2:
        return jsonify([])
    matches = [n for n in LOCATION_NAMES if q in n.lower()][:8]
    return jsonify(matches)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    today_holiday = get_today_holiday()
    return render_template("index.html",
                           today_holiday=today_holiday,
                           holidays_db=HOLIDAYS,
                           location_names=LOCATION_NAMES,
                           api_key_set=bool(OPENWEATHER_API_KEY))


@app.route("/predict", methods=["POST"])
def predict():
    location_raw  = request.form.get("location", "").strip()
    day_name      = request.form.get("day_name", "Monday")
    weather_key   = request.form.get("weather", "auto") or "auto"
    simulated_holiday = request.form.get("simulated_holiday", "")

    if not location_raw:
        return render_template("index.html",
                               error="Please enter a location name.",
                               today_holiday=get_today_holiday(),
                               holidays_db=HOLIDAYS,
                               location_names=LOCATION_NAMES,
                               api_key_set=bool(OPENWEATHER_API_KEY))

    display_name, zone_label, zone_id = lookup_location(location_raw)
    if display_name is None:
        err = (
            f"'{location_raw.title()}' is not in our Bengaluru location database. "
            f"Try: Whitefield, MG Road, Koramangala, BTM Layout, Jayanagar, Yelahanka, Hebbal."
        )
        return render_template("index.html", error=err,
                               today_holiday=get_today_holiday(),
                               holidays_db=HOLIDAYS,
                               location_names=LOCATION_NAMES,
                               api_key_set=bool(OPENWEATHER_API_KEY))

    if weather_key == "auto":
        if OPENWEATHER_API_KEY:
            try:
                resp = req_lib.get(OPENWEATHER_URL, params={
                    "q": OPENWEATHER_CITY, "appid": OPENWEATHER_API_KEY, "units": "metric"
                }, timeout=3)
                if resp.status_code == 200:
                    owm_main = resp.json()["weather"][0]["main"]
                    weather_key = OWM_MAP.get(owm_main, "clear")
                else:
                    weather_key = "clear"
            except:
                weather_key = "clear"
        else:
            weather_key = "clear"

    wdata        = WEATHER_CONFIG.get(weather_key, WEATHER_CONFIG["clear"])
    weather_mult = wdata["multiplier"]

    holiday = None
    if simulated_holiday and simulated_holiday in HOLIDAYS:
        holiday = HOLIDAYS[simulated_holiday]
    elif request.form.get("apply_holiday") == "1":
        holiday = get_today_holiday()

    hourly_data = compute_hourly(day_name, zone_id, weather_key, holiday)
    intensities = [d["intensity"] for d in hourly_data]
    high_hrs    = [d["hour"] for d in hourly_data if d["level"] == 2]
    med_hrs     = [d["hour"] for d in hourly_data if d["level"] == 1]
    low_hrs     = [d["hour"] for d in hourly_data if d["level"] == 0]
    weekly_data = [day_summary(d, zone_id, weather_key, holiday) for d in ALL_DAYS]

    result = {
        "location":         display_name,
        "mapped_zone":      zone_label,
        "day_name":         day_name,
        "weather_key":      weather_key,
        "weather_label":    wdata["label"],
        "weather_icon":     wdata["icon"],
        "weather_affected": weather_mult > 1.0,
        "weather_boost":    f"+{round((weather_mult - 1) * 100)}%",
        "holiday_applied":  holiday is not None,
        "holiday_info":     holiday,
        "high_traffic":     group_hours(high_hrs),
        "medium_traffic":   group_hours(med_hrs),
        "best_time":        group_hours(low_hrs),
        "peak_intensity":   max(intensities),
        "low_intensity":    min(intensities),
        "avg_intensity":    round(sum(intensities) / 24, 1),
        "high_count":       len(high_hrs),
        "med_count":        len(med_hrs),
        "low_count":        len(low_hrs),
        "hourly_data":      hourly_data,
        "graph_data":       intensities,
        "graph_labels":     [fmt_hour(h) for h in range(24)],
        "weekly_data":      weekly_data,
    }

    return render_template("index.html", result=result,
                           today_holiday=get_today_holiday(),
                           holidays_db=HOLIDAYS,
                           location_names=LOCATION_NAMES,
                           api_key_set=bool(OPENWEATHER_API_KEY))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
