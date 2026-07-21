from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from cargo.services import get_available_cargo_for_user, calculate_travel, start_travel_db
from cargo.keyboards import cargo_list_keyboard, route_selection_keyboard
from cargo.messages import cargo_info_message
from cargo.data import CARGO_TYPES, ROUTES
from database.models import get_user_active_truck
import logging

logger = logging.getLogger(__name__)

@require_membership
async def show_cargo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    available = get_available_cargo_for_user(user_id)
    if not available:
        await query.edit_message_text("🚛 ابتدا یک کامیون مناسب بخرید.")
        return
    await query.edit_message_text("📦 بارهای موجود:", reply_markup=cargo_list_keyboard(available))

@require_membership
async def select_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cargo_type = query.data.split("_", 1)[1]
    if cargo_type not in CARGO_TYPES:
        await query.answer("نامعتبر"); return
    text = cargo_info_message(cargo_type, CARGO_TYPES[cargo_type])
    await query.edit_message_text(text, reply_markup=route_selection_keyboard(cargo_type))

@require_membership
async def start_travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_", 2)  # route_{cargo}_{route}
    if len(data) < 3:
        return
    cargo_type, route_name = data[1], data[2]
    if route_name not in ROUTES:
        await query.answer("مسیر نامعتبر"); return
    user_id = update.effective_user.id
    truck = get_user_active_truck(user_id)
    if not truck:
        await query.answer("کامیون فعال ندارید"); return
    try:
        travel_info = calculate_travel(user_id, cargo_type, route_name)
    except Exception as e:
        await query.answer(str(e)); return
    # ثبت سفر
    travel_id = start_travel_db(user_id, truck["id"], cargo_type, route_name, travel_info)
    # زمان‌بندی اتمام سفر
    delay = travel_info["travel_seconds"]
    context.job_queue.run_once(
        lambda ctx: complete_travel_callback(ctx, travel_id),
        delay,
        data=travel_id,
        name=f"travel_{travel_id}"
    )
    await query.edit_message_text(
        f"🚛 سفر آغاز شد!\n📦 بار: {cargo_type}\n🛣️ مسیر: {route_name}\n🌤 آب‌وهوا: {travel_info['weather']}\n⏳ زمان تقریبی: {delay} ثانیه"
    )

async def complete_travel_callback(context: ContextTypes.DEFAULT_TYPE, travel_id: int):
    from cargo.services import complete_travel
    complete_travel(travel_id, context)
