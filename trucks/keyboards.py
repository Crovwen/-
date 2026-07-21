from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from trucks.data import TRUCK_DETAILS

EMOJI_IDS = {
    "Scania": 5440882648090186943,
    "Mercedes": 5300762707312520262,
    "Volvo": 5316999135390353675,
    "MAN": 5440791019257892531,
    "DAF": None
}
def custom_emoji(emoji_id, fallback):
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    return fallback

def brand_selection_keyboard():
    brands = [
        ("Scania", custom_emoji(EMOJI_IDS["Scania"], "🚛")),
        ("Volvo", custom_emoji(EMOJI_IDS["Volvo"], "🚛")),
        ("Mercedes", custom_emoji(EMOJI_IDS["Mercedes"], "🚛")),
        ("DAF", "🇳🇱 DAF"),
        ("MAN", custom_emoji(EMOJI_IDS["MAN"], "🚛")),
    ]
    keyboard = [[InlineKeyboardButton(label, callback_data=f"brand_{brand}")] for brand, label in brands]
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def truck_list_keyboard(brand: str):
    trucks = [n for n, d in TRUCK_DETAILS.items() if d["brand"] == brand]
    trucks.sort(key=lambda x: TRUCK_DETAILS[x]["power_hp"], reverse=True)
    keyboard = [[InlineKeyboardButton(name, callback_data=f"truck_{name}")] for name in trucks]
    keyboard.append([InlineKeyboardButton("🔙 برندها", callback_data="menu_trucks")])
    return InlineKeyboardMarkup(keyboard)

def truck_detail_keyboard(truck_name: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید ماشین", callback_data=f"buy_{truck_name}")],
        [InlineKeyboardButton("🔙 لیست کامیون‌ها", callback_data=f"brand_{TRUCK_DETAILS[truck_name]['brand']}")]
    ])
