import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.models import get_user, create_user, get_user_active_truck, update_balance
from middlewares.membership import require_membership, send_channel_join_prompt, is_user_member
from keyboards.main_menu import main_menu_keyboard
from messages.welcome import welcome_message
from handlers.referral import process_referral, apply_referral_rewards

logger = logging.getLogger(__name__)

@require_membership
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    referred_by = None
    if args:
        await process_referral(update, context, args[0])
    db_user = get_user(user.id)
    if not db_user:
        create_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            is_premium=user.is_premium or False,
            referred_by=referred_by   # حالا تعریف شده است
        )
        if "referrer_id" in context.user_data:
            await apply_referral_rewards(update, context)
    await update.message.reply_text(
        welcome_message(user.first_name),
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = get_user(user.id)
    if not db_user:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کنید.")
        return
    truck = get_user_active_truck(user.id)
    truck_text = truck["truck_model"] if truck else "ندارید"
    text = (
        f"👤 پروفایل شما:\n"
        f"🆔 شناسه: {user.id}\n"
        f"💰 سکه: {db_user['balance']:,}\n"
        f"🚛 ماشین فعال: {truck_text}\n"
        f"🔗 لینک دعوت: https://t.me/{context.bot.username}?start={db_user['referral_code']}"
    )
    await update.message.reply_text(text, parse_mode="HTML")
