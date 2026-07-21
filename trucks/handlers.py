# trucks/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from trucks.keyboards import (
    brand_selection_keyboard,
    truck_list_keyboard,
    truck_detail_keyboard
)
from trucks.messages import truck_detail_message
from trucks.services import purchase_truck
from trucks.data import TRUCK_DETAILS

@require_membership
async def show_brands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🚛 برند مورد نظر خود را انتخاب کنید:",
        reply_markup=brand_selection_keyboard(),
        parse_mode="HTML"
    )

@require_membership
async def show_truck_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand = query.data.split("_", 1)[1]  # brand_Scania -> Scania
    keyboard = truck_list_keyboard(brand)
    await query.edit_message_text(
        f"🚛 کامیون‌های {brand} (به ترتیب قدرت):",
        reply_markup=keyboard
    )

@require_membership
async def show_truck_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    truck_name = query.data.split("_", 1)[1]  # truck_Scania S770 V8
    if truck_name not in TRUCK_DETAILS:
        await query.answer("کامیون نامعتبر!", show_alert=True)
        return
    text = truck_detail_message(truck_name)
    keyboard = truck_detail_keyboard(truck_name)
    await query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@require_membership
async def buy_truck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    truck_name = query.data.split("_", 1)[1]  # buy_Scania S770 V8
    await query.answer("در حال بررسی ...")
    success, message = purchase_truck(user.id, truck_name)
    if success:
        # موفقیت: پیام را به‌روز کنیم
        await query.edit_message_text(
            message,
            parse_mode="HTML"
        )
    else:
        # خطا (موجودی ناکافی) - نمایش پیام
        await query.answer(message, show_alert=True)
