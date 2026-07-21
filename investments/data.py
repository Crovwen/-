# investments/data.py
BUILDINGS = {
    "پارکینگ": {"base_price": 20000, "income_bonus": 0.1},
    "تعمیرگاه": {"base_price": 25000, "repair_discount": 0.2},
    "پمپ بنزین": {"base_price": 15000, "fuel_discount": 0.15},
    "شرکت حمل‌ونقل": {"base_price": 50000, "income_bonus": 0.2}
}

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

# investments/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from database.connection import Database
from database.models import update_balance
from investments.data import BUILDINGS
from investments.keyboards import buildings_menu_keyboard, building_detail_keyboard
import logging

@require_membership
async def buildings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏗 ساختمان‌های قابل خرید:", reply_markup=buildings_menu_keyboard())

@require_membership
async def buy_building(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    building = query.data.split("_", 1)[1]
    user_id = update.effective_user.id
    price = BUILDINGS[building]["base_price"]
    try:
        update_balance(user_id, -price)
    except ValueError:
        await query.answer("موجودی ناکافی", show_alert=True); return
    db = Database()
    db.execute("INSERT OR IGNORE INTO user_buildings (user_id, building_type) VALUES (?,?)", (user_id, building))
    db.commit()
    await query.edit_message_text(f"✅ ساختمان {building} خریداری شد!")

@require_membership
async def upgrade_building(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    building = query.data.split("_", 1)[1]
    user_id = update.effective_user.id
    db = Database()
    row = db.execute("SELECT level FROM user_buildings WHERE user_id=? AND building_type=?", (user_id, building)).fetchone()
    if not row:
        await query.answer("ابتدا ساختمان را بخرید", show_alert=True); return
    level = row[0]
    cost = int(BUILDINGS[building]["base_price"] * (level + 1) * 0.5)
    try:
        update_balance(user_id, -cost)
    except ValueError:
        await query.answer("موجودی ناکافی", show_alert=True); return
    db.execute("UPDATE user_buildings SET level = level + 1 WHERE user_id=? AND building_type=?", (user_id, building))
    db.commit()
    await query.edit_message_text(f"⬆️ {building} به سطح {level+1} ارتقا یافت. هزینه: {cost} سکه") 
