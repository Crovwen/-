import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import get_user, create_user, update_balance
from config import Config

logger = logging.getLogger(__name__)

async def process_referral(update: Update, context: ContextTypes.DEFAULT_TYPE, referral_code: str):
    new_user = update.effective_user
    if get_user(new_user.id):
        return None
    from database.connection import Database
    db = Database()
    cursor = db.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
    row = cursor.fetchone()
    if not row:
        return None
    referrer_id = row[0]
    if referrer_id == new_user.id:
        return None
    context.user_data["referrer_id"] = referrer_id

async def apply_referral_rewards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referrer_id = context.user_data.pop("referrer_id", None)
    if not referrer_id:
        return
    new_user_id = update.effective_user.id
    try:
        from database.connection import Database
        db = Database()
        with db.connection:
            db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",
                       (Config.REFERRAL_REWARD_REFERRER, referrer_id))
            db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",
                       (Config.REFERRAL_REWARD_NEW_USER, new_user_id))
        logger.info(f"Referral reward: {referrer_id} +{Config.REFERRAL_REWARD_REFERRER}, {new_user_id} +{Config.REFERRAL_REWARD_NEW_USER}")
    except Exception as e:
        logger.error(f"Error applying referral reward: {e}")
