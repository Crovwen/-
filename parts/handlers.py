from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from database.models import get_user_active_truck, update_balance
from database.connection import Database
from parts.keyboards import parts_menu_keyboard, upgrade_menu_keyboard
from parts.data import PART_REPAIR_COST_PER_POINT, PART_UPGRADE_COST
import logging

logger = logging.getLogger(__name__)

def get_part_health(truck_id: int, part_name: str) -> float:
    db = Database()
    row = db.execute("SELECT health FROM truck_parts WHERE truck_id=? AND part_name=?", (truck_id, part_name)).fetchone()
    return row[0] if row else 100.0

@require_membership
async def parts_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    truck = get_user_active_truck(user_id)
    if not truck:
        await query.edit_message_text("کامیون فعال ندارید.")
        return
    parts_status = []
    for p in ["engine","gearbox","tire","brake","air_filter","oil_filter"]:
        health = get_part_health(truck["id"], p)
        parts_status.append(f"{p}: {health:.1f}%")
    text = "🔧 وضعیت قطعات:\n" + "\n".join(parts_status)
    await query.edit_message_text(text, reply_markup=parts_menu_keyboard(truck["id"]))

@require_membership
async def repair_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")
    part = data[1]
    truck_id = int(data[2])
    user_id = update.effective_user.id
    current_health = get_part_health(truck_id, part)
    damage = 100 - current_health
    if damage <= 0:
        await query.answer("قطعه سالم است"); return
    cost = int(damage * PART_REPAIR_COST_PER_POINT)
    try:
        update_balance(user_id, -cost)
    except ValueError:
        await query.answer("موجودی کافی نیست", show_alert=True); return
    db = Database()
    db.execute("UPDATE truck_parts SET health=100 WHERE truck_id=? AND part_name=?", (truck_id, part))
    db.commit()
    await query.edit_message_text(f"✅ تعمیر {part} با موفقیت. هزینه: {cost} سکه")

@require_membership
async def upgrade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")
    part = data[1]
    truck_id = int(data[2])
    cost = PART_UPGRADE_COST.get(part, 5000)
    user_id = update.effective_user.id
    try:
        update_balance(user_id, -cost)
    except ValueError:
        await query.answer("موجودی کافی نیست", show_alert=True); return
    db = Database()
    db.execute("UPDATE truck_parts SET upgrade_level = upgrade_level + 1 WHERE truck_id=? AND part_name=?", (truck_id, part))
    db.commit()
    await query.edit_message_text(f"⬆️ ارتقاء {part} انجام شد. هزینه: {cost} سکه") 
