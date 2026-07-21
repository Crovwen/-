# investments/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from investments.data import BUILDINGS

def buildings_menu_keyboard():
    keyboard = [[InlineKeyboardButton(f"🏗 {b}", callback_data=f"building_{b}")] for b in BUILDINGS]
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def building_detail_keyboard(building_type):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید", callback_data=f"buybuilding_{building_type}")],
        [InlineKeyboardButton("⬆️ ارتقاء", callback_data=f"upgradebuilding_{building_type}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="menu_buildings")]
    ])
