from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from database.connection import Database
from database.models import update_balance, get_user_active_truck
from market.keyboards import market_menu_keyboard, market_listings_keyboard
import logging

@require_membership
async def market_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📊 بازار ماشین‌ها:", reply_markup=market_menu_keyboard())

@require_membership
async def list_truck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    truck = get_user_active_truck(user_id)
    if not truck:
        await query.answer("کامیون فعال ندارید"); return
    # قیمت پیشنهادی
    await query.edit_message_text("لطفاً قیمت فروش را به صورت عددی ارسال کنید (مثلاً 15000)")

@require_membership
async def buy_listed_truck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    listing_id = int(query.data.split("_")[1])
    db = Database()
    ad = db.execute("SELECT * FROM market_listings WHERE id=? AND sold=0", (listing_id,)).fetchone()
    if not ad:
        await query.answer("آگهی موجود نیست"); return
    buyer_id = update.effective_user.id
    price = ad["price"]
    try:
        update_balance(buyer_id, -price)
        update_balance(ad["seller_id"], price)
    except ValueError:
        await query.answer("موجودی ناکافی", show_alert=True); return
    # انتقال مالکیت
    db.execute("UPDATE user_trucks SET user_id=? WHERE id=?", (buyer_id, ad["truck_id"]))
    db.execute("UPDATE market_listings SET sold=1 WHERE id=?", (listing_id,))
    db.commit()
    await query.edit_message_text("✅ خرید موفق! کامیون به گاراژ شما اضافه شد.")
