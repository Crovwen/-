from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚛 ماشین‌ها", callback_data="menu_trucks")],
        [InlineKeyboardButton("📦 بارها", callback_data="menu_cargo")],
        [InlineKeyboardButton("🔧 قطعات و تعمیرات", callback_data="menu_parts")],
        [InlineKeyboardButton("🏗 ساختمان‌ها", callback_data="menu_buildings")],
        [InlineKeyboardButton("📊 بازار", callback_data="menu_market")],
        [InlineKeyboardButton("🎁 مزایده", callback_data="menu_auction")],
        [InlineKeyboardButton("🏆 رقابت هفتگی", callback_data="menu_weekly")],
        [InlineKeyboardButton("👤 پروفایل", callback_data="menu_profile")],
        [InlineKeyboardButton("📖 راهنما", callback_data="menu_help")],
        [InlineKeyboardButton("🔗 دعوت دوستان", callback_data="menu_referral")]
    ]) 
