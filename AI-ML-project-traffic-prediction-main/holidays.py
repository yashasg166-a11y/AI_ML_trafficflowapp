"""
holidays.py  –  Indian Public Holiday Database (2025–2026)
============================================================
Each entry has:
  name        – display name
  emoji       – festival icon
  type        – 'festival' | 'national' | 'regional'
  desc        – short description shown to user
  mod_morning – traffic multiplier, hours 0–10
  mod_evening – traffic multiplier, hours 17–23
  mod_day     – traffic multiplier, hours 11–16
"""

from datetime import date

# ── Holiday database ──────────────────────────────────────────────────────────
HOLIDAYS = {

    # ─ 2025 ───────────────────────────────────────────────────────────────────
    "2025-01-14": {
        "name": "Makar Sankranti / Pongal",
        "emoji": "🪁",  "type": "festival",
        "desc": "Kite festival — lighter daytime, busy evenings",
        "mod_morning": 0.72, "mod_day": 0.80, "mod_evening": 1.28,
    },
    "2025-01-26": {
        "name": "Republic Day",
        "emoji": "🇮🇳", "type": "national",
        "desc": "Public holiday — light traffic throughout",
        "mod_morning": 0.58, "mod_day": 0.65, "mod_evening": 0.78,
    },
    "2025-02-26": {
        "name": "Maha Shivratri",
        "emoji": "🕉️",  "type": "festival",
        "desc": "Temple crowds in late evening",
        "mod_morning": 0.75, "mod_day": 0.85, "mod_evening": 1.22,
    },
    "2025-03-14": {
        "name": "Holi",
        "emoji": "🎨",  "type": "festival",
        "desc": "Holiday morning, festive evening gatherings",
        "mod_morning": 0.65, "mod_day": 0.70, "mod_evening": 1.18,
    },
    "2025-03-30": {
        "name": "Ugadi",
        "emoji": "🌅",  "type": "regional",
        "desc": "Karnataka New Year — offices closed, family outings",
        "mod_morning": 0.70, "mod_day": 0.80, "mod_evening": 1.32,
    },
    "2025-04-14": {
        "name": "Dr. Ambedkar Jayanti",
        "emoji": "🎂",  "type": "national",
        "desc": "Public holiday — moderate traffic reduction",
        "mod_morning": 0.75, "mod_day": 0.82, "mod_evening": 0.88,
    },
    "2025-04-18": {
        "name": "Good Friday",
        "emoji": "✝️",  "type": "national",
        "desc": "Public holiday — light traffic",
        "mod_morning": 0.65, "mod_day": 0.72, "mod_evening": 0.75,
    },
    "2025-05-01": {
        "name": "Labour Day / Karnataka Rajyotsava",
        "emoji": "🏛️", "type": "national",
        "desc": "Public holiday — significantly lighter roads",
        "mod_morning": 0.60, "mod_day": 0.68, "mod_evening": 0.75,
    },
    "2025-08-15": {
        "name": "Independence Day",
        "emoji": "🇮🇳", "type": "national",
        "desc": "National holiday — very light traffic",
        "mod_morning": 0.52, "mod_day": 0.60, "mod_evening": 0.72,
    },
    "2025-08-16": {
        "name": "Janmashtami",
        "emoji": "🦚",  "type": "festival",
        "desc": "Night celebrations — heavy traffic post 9 PM",
        "mod_morning": 0.72, "mod_day": 0.85, "mod_evening": 1.28,
    },
    "2025-08-27": {
        "name": "Ganesh Chaturthi",
        "emoji": "🐘",  "type": "festival",
        "desc": "Grand processions — very heavy evening congestion",
        "mod_morning": 0.72, "mod_day": 0.88, "mod_evening": 1.42,
    },
    "2025-10-02": {
        "name": "Gandhi Jayanti",
        "emoji": "🪷",  "type": "national",
        "desc": "National holiday — light traffic",
        "mod_morning": 0.60, "mod_day": 0.68, "mod_evening": 0.78,
    },
    "2025-10-02": {
        "name": "Dussehra / Navami",
        "emoji": "🏹",  "type": "festival",
        "desc": "Processions and celebrations — heavy evening traffic",
        "mod_morning": 0.72, "mod_day": 0.85, "mod_evening": 1.38,
    },
    "2025-10-20": {
        "name": "Diwali",
        "emoji": "🪔",  "type": "festival",
        "desc": "Biggest festival — evening roads extremely congested",
        "mod_morning": 0.65, "mod_day": 0.82, "mod_evening": 1.42,
    },
    "2025-11-01": {
        "name": "Karnataka Rajyotsava",
        "emoji": "🏛️", "type": "regional",
        "desc": "Karnataka Formation Day — state holiday",
        "mod_morning": 0.58, "mod_day": 0.68, "mod_evening": 0.80,
    },
    "2025-11-05": {
        "name": "Guru Nanak Jayanti",
        "emoji": "🙏",  "type": "national",
        "desc": "National holiday — moderate traffic reduction",
        "mod_morning": 0.72, "mod_day": 0.80, "mod_evening": 0.85,
    },
    "2025-12-25": {
        "name": "Christmas",
        "emoji": "🎄",  "type": "national",
        "desc": "Public holiday — lighter traffic, mall zones busier",
        "mod_morning": 0.65, "mod_day": 0.80, "mod_evening": 0.90,
    },

    # ─ 2026 ───────────────────────────────────────────────────────────────────
    "2026-01-14": {
        "name": "Makar Sankranti / Pongal",
        "emoji": "🪁",  "type": "festival",
        "desc": "Kite festival — lighter daytime, busy evenings",
        "mod_morning": 0.72, "mod_day": 0.80, "mod_evening": 1.28,
    },
    "2026-01-26": {
        "name": "Republic Day",
        "emoji": "🇮🇳", "type": "national",
        "desc": "Public holiday — light traffic throughout",
        "mod_morning": 0.58, "mod_day": 0.65, "mod_evening": 0.78,
    },
    "2026-03-20": {
        "name": "Ugadi",
        "emoji": "🌅",  "type": "regional",
        "desc": "Karnataka New Year — offices closed, family outings",
        "mod_morning": 0.70, "mod_day": 0.80, "mod_evening": 1.32,
    },
    "2026-03-25": {
        "name": "Holi",
        "emoji": "🎨",  "type": "festival",
        "desc": "Holiday morning, festive evening gatherings",
        "mod_morning": 0.65, "mod_day": 0.70, "mod_evening": 1.18,
    },
    "2026-04-03": {
        "name": "Good Friday",
        "emoji": "✝️",  "type": "national",
        "desc": "Public holiday — light traffic",
        "mod_morning": 0.65, "mod_day": 0.72, "mod_evening": 0.75,
    },
    "2026-08-15": {
        "name": "Independence Day",
        "emoji": "🇮🇳", "type": "national",
        "desc": "National holiday — very light traffic",
        "mod_morning": 0.52, "mod_day": 0.60, "mod_evening": 0.72,
    },
    "2026-09-16": {
        "name": "Ganesh Chaturthi",
        "emoji": "🐘",  "type": "festival",
        "desc": "Grand processions — very heavy evening congestion",
        "mod_morning": 0.72, "mod_day": 0.88, "mod_evening": 1.42,
    },
    "2026-10-02": {
        "name": "Gandhi Jayanti",
        "emoji": "🪷",  "type": "national",
        "desc": "National holiday — light traffic",
        "mod_morning": 0.60, "mod_day": 0.68, "mod_evening": 0.78,
    },
    "2026-11-01": {
        "name": "Karnataka Rajyotsava",
        "emoji": "🏛️", "type": "regional",
        "desc": "Karnataka Formation Day — state holiday",
        "mod_morning": 0.58, "mod_day": 0.68, "mod_evening": 0.80,
    },
    "2026-11-08": {
        "name": "Diwali",
        "emoji": "🪔",  "type": "festival",
        "desc": "Biggest festival — evening roads extremely congested",
        "mod_morning": 0.65, "mod_day": 0.82, "mod_evening": 1.42,
    },
    "2026-12-25": {
        "name": "Christmas",
        "emoji": "🎄",  "type": "national",
        "desc": "Public holiday — lighter traffic, mall zones busier",
        "mod_morning": 0.65, "mod_day": 0.80, "mod_evening": 0.90,
    },
}

MORNING_HOURS = set(range(0, 11))    # 12 AM–10 AM
DAY_HOURS     = set(range(11, 17))   # 11 AM–4 PM
EVENING_HOURS = set(range(17, 24))   # 5 PM–11 PM


def get_today_holiday():
    """Return today's holiday dict or None."""
    today_str = date.today().isoformat()
    return HOLIDAYS.get(today_str)


def get_holiday_multiplier(holiday_dict, hour):
    """Return the traffic multiplier for a specific hour given a holiday."""
    if not holiday_dict:
        return 1.0
    if hour in MORNING_HOURS:
        return holiday_dict["mod_morning"]
    if hour in DAY_HOURS:
        return holiday_dict.get("mod_day", 0.80)
    return holiday_dict["mod_evening"]
