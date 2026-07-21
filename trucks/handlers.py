from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from trucks.keyboards import brand_selection_keyboard, truck_list_keyboard, truck_detail_keyboard
from trucks.messages import truck_detail_message
from trucks.services import purchase_truck
from trucks.data import TRUCK_DETAILS

@require_membership
async def show_brands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🚛 برند مورد نظر:", reply_markup=brand_selection_keyboard(), parse_mode="HTML")

@require_membership
async def show_truck_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand = query.data.split("_", 1)[1]
    await query.edit_message_text(f"🚛 کامیون‌های {brand}:", reply_markup=truck_list_keyboard(brand))

@require_membership
async def show_truck_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    truck_name = query.data.split("_", 1)[1]
    if truck_name not in TRUCK_DETAILS:
        await query.answer("نامعتبر", show_alert=True); return
    await query.edit_message_text(truck_detail_message(truck_name),
                                  reply_markup=truck_detail_keyboard(truck_name), parse_mode="HTML")

@require_membership
async def buy_truck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("در حال خرید...")
    truck_name = query.data.split("_", 1)[1]
    success, msg = purchase_truck(update.effective_user.id, truck_name)
    if success:
        await query.edit_message_text(msg)
    else:
        await query.answer(msg, show_alert=True) 
