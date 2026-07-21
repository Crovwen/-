# auction/handlers.py
import random, logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import require_membership
from database.connection import Database
from database.models import update_balance

@require_membership
async def auction_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    db = Database()
    # آخرین مزایده فعال
    auction = db.execute("SELECT * FROM auction_listings WHERE active=1 AND end_time > ?", (datetime.now(),)).fetchone()
    if not auction:
        # ایجاد مزایده جدید
        end = datetime.now() + timedelta(minutes=5)
        db.execute("INSERT INTO auction_listings (cargo_data, starting_price, current_bid, end_time) VALUES (?,?,?,?)",
                   ("بار الماس", 20000, 20000, end))
        db.commit()
        auction = db.execute("SELECT * FROM auction_listings WHERE active=1 AND end_time > ?", (datetime.now(),)).fetchone()
    text = f"🎁 مزایده: {auction['cargo_data']}\n💰 بالاترین پیشنهاد: {auction['current_bid']} سکه\n⏳ زمان: {auction['end_time']}"
    await query.edit_message_text(text, reply_markup=auction_menu_keyboard(auction["id"], auction["current_bid"]))

@require_membership
async def place_bid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, auction_id, bid_amount = query.data.split("_")
    auction_id, bid_amount = int(auction_id), int(bid_amount)
    user_id = update.effective_user.id
    try:
        update_balance(user_id, -bid_amount)
    except ValueError:
        await query.answer("موجودی ناکافی", show_alert=True); return
    db = Database()
    # refund previous bidder if any
    old = db.execute("SELECT highest_bidder, current_bid FROM auction_listings WHERE id=?", (auction_id,)).fetchone()
    if old and old["highest_bidder"] and old["current_bid"]:
        try:
            update_balance(old["highest_bidder"], old["current_bid"])
        except:
            pass
    db.execute("UPDATE auction_listings SET current_bid=?, highest_bidder=? WHERE id=?", (bid_amount, user_id, auction_id))
    db.commit()
    await query.edit_message_text(f"✅ پیشنهاد شما ثبت شد: {bid_amount} سکه")
