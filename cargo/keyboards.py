from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from cargo.data import CARGO_TYPES, ROUTES

def cargo_list_keyboard(available_cargos: list):
    keyboard = []
    for c in available_cargos:
        keyboard.append([InlineKeyboardButton(f"📦 {c}", callback_data=f"cargo_{c}")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def route_selection_keyboard(cargo_type: str):
    # نمایش مسیرهای موجود برای بار
    keyboard = [[InlineKeyboardButton(f"🛣️ {r}", callback_data=f"route_{cargo_type}_{r}")] for r in ROUTES]
    keyboard.append([InlineKeyboardButton("🔙 بارها", callback_data="menu_cargo")])
    return InlineKeyboardMarkup(keyboard)
