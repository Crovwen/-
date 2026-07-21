# trucks/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from trucks.data import TRUCK_DETAILS

# ایموجی‌های پریمیوم (شناسه‌ها)
EMOJI_IDS = {
    "Scania": 5440882648090186943,
    "Mercedes": 5300762707312520262,
    "Volvo": 5316999135390353675,
    "MAN": 5440791019257892531,
    "DAF": None  # از ایموجی معمولی 🇳🇱 استفاده می‌کنیم
}
def custom_emoji(emoji_id: int, fallback: str) -> str:
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
    keyboard = []
    for brand, label in brands:
        keyboard.append([InlineKeyboardButton(label, callback_data=f"brand_{brand}")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def truck_list_keyboard(brand: str):
    """لیست کامیون‌های یک برند، مرتب نزولی قدرت"""
    trucks = [name for name, det in TRUCK_DETAILS.items() if det["brand"] == brand]
    # مرتب‌سازی بر اساس قدرت (نزولی)
    trucks.sort(key=lambda x: TRUCK_DETAILS[x]["power_hp"], reverse=True)
    keyboard = []
    for name in trucks:
        # فقط اسم انگلیسی داخل دکمه شیشه‌ای (بدون لوگو)
        keyboard.append([InlineKeyboardButton(name, callback_data=f"truck_{name}")])
    keyboard.append([InlineKeyboardButton("🔙 برندها", callback_data="menu_trucks")])
    return InlineKeyboardMarkup(keyboard)

def truck_detail_keyboard(truck_name: str):
    """دکمه‌های زیر جزئیات کامیون"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید ماشین", callback_data=f"buy_{truck_name}")],
        [InlineKeyboardButton("🔙 لیست کامیون‌ها", callback_data=f"brand_{TRUCK_DETAILS[truck_name]['brand']}")]
    ])
