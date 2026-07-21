# handlers/referral.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import get_user, create_user, update_balance
from config import Config

logger = logging.getLogger(__name__)

async def process_referral(update: Update, context: ContextTypes.DEFAULT_TYPE, referral_code: str):
    """پردازش لینک رفرال در /start"""
    new_user = update.effective_user
    # بررسی اگر کاربر قبلاً ثبت‌نام کرده بود، هیچ جایزه‌ای نده
    if get_user(new_user.id):
        return None

    # پیدا کردن کاربر ارجاع‌دهنده بر اساس کد رفرال
    from database.connection import Database
    db = Database()
    cursor = db.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
    referrer_row = cursor.fetchone()
    if not referrer_row:
        return None
    referrer_id = referrer_row[0]
    if referrer_id == new_user.id:
        return None  # جلوگیری از رفرال خود

    # اطمینان از اینکه کاربر جدید رکورد ندارد (حالت مسابقه)
    # در start_command کاربر جدید ساخته می‌شود، ما جایزه را بعد از ایجاد می‌دهیم
    # بهتر است ابتدا کاربر را ایجاد کنیم سپس پاداش
    # ما اینجا یک نشانه به context می‌دهیم
    context.user_data["referrer_id"] = referrer_id

async def apply_referral_rewards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اعمال پاداش‌های رفرال (فراخوانی بعد از ایجاد کاربر جدید)"""
    referrer_id = context.user_data.pop("referrer_id", None)
    if not referrer_id:
        return
    new_user_id = update.effective_user.id
    try:
        # استفاده از transaction
        from database.connection import Database
        db = Database()
        with db.connection:
            # افزایش موجودی دعوت‌کننده
            db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (Config.REFERRAL_REWARD_REFERRER, referrer_id)
            )
            # افزایش موجودی کاربر جدید
            db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (Config.REFERRAL_REWARD_NEW_USER, new_user_id)
            )
        logger.info(f"Referral reward: referrer {referrer_id} +{Config.REFERRAL_REWARD_REFERRER}, new {new_user_id} +{Config.REFERRAL_REWARD_NEW_USER}")
    except Exception as e:
        logger.error(f"Error applying referral reward: {e}")
