from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def parts_menu_keyboard(truck_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔧 تعمیر موتور", callback_data=f"repair_engine_{truck_id}")],
        [InlineKeyboardButton("🔧 تعمیر گیربکس", callback_data=f"repair_gearbox_{truck_id}")],
        [InlineKeyboardButton("🛞 تعویض لاستیک", callback_data=f"repair_tire_{truck_id}")],
        [InlineKeyboardButton("🛑 تعمیر ترمز", callback_data=f"repair_brake_{truck_id}")],
        [InlineKeyboardButton("🌬️ فیلتر هوا", callback_data=f"repair_air_filter_{truck_id}")],
        [InlineKeyboardButton("🛢️ فیلتر روغن", callback_data=f"repair_oil_filter_{truck_id}")],
        [InlineKeyboardButton("⬆️ ارتقاء", callback_data=f"upgrade_menu_{truck_id}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
    ])

def upgrade_menu_keyboard(truck_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ موتور", callback_data=f"upgrade_engine_{truck_id}")],
        [InlineKeyboardButton("⚙️ گیربکس", callback_data=f"upgrade_gearbox_{truck_id}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="menu_parts")]
    ]) 
