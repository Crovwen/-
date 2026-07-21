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
