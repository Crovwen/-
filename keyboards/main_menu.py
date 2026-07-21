# keyboards/main_menu.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("🚛 ماشین‌ها", callback_data="menu_trucks")],
        [InlineKeyboardButton("📦 بارها", callback_data="menu_cargo")],
        [InlineKeyboardButton("👤 پروفایل", callback_data="menu_profile")],
        [InlineKeyboardButton("🏗 ساختمان‌ها", callback_data="menu_buildings")],
        [InlineKeyboardButton("📊 بازار", callback_data="menu_market")],
        [InlineKeyboardButton("🏆 رقابت هفتگی", callback_data="menu_weekly")],
        [InlineKeyboardButton("🎁 مزایده", callback_data="menu_auction")],
        [InlineKeyboardButton("📖 راهنما", callback_data="menu_help")],
        [InlineKeyboardButton("🔗 دعوت دوستان", callback_data="menu_referral")]
    ]
    return InlineKeyboardMarkup(buttons)
