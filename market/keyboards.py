from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def market_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 لیست آگهی‌ها", callback_data="market_list")],
        [InlineKeyboardButton("📢 ثبت آگهی فروش", callback_data="market_sell")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
    ])

def market_listings_keyboard(listings):
    keyboard = []
    for ad in listings:
        keyboard.append([InlineKeyboardButton(f"{ad['truck_model']} - {ad['price']} سکه", callback_data=f"buymarket_{ad['id']}")])
    keyboard.append([InlineKeyboardButton("🔙 بازار", callback_data="menu_market")])
    return InlineKeyboardMarkup(keyboard)
