# handlers/callbacks.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import is_user_member, send_channel_join_prompt
from keyboards.main_menu import main_menu_keyboard
from database.models import get_user

logger = logging.getLogger(__name__)

async def check_membership_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی عضویت کانال و نمایش منوی اصلی در صورت موفقیت"""
    query = update.callback_query
    await query.answer()  # برای بستن حالت loading
    if await is_user_member(update, context):
        user = update.effective_user
        db_user = get_user(user.id)
        if db_user:
            await query.edit_message_text(
                f"✅ عضویت شما تأیید شد! به بازی خوش آمدید، {user.first_name}",
                reply_markup=main_menu_keyboard()
            )
        else:
            # اگر کاربر رکورد ندارد، دوباره /start را اجرا کنیم
            from handlers.commands import start_command
            await start_command(update, context)
    else:
        await query.answer("❌ شما هنوز عضو کانال نیستید!", show_alert=True)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر کلیک‌های منوی اصلی (فعلاً پیام نمونه)"""
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "menu_trucks":
        await query.edit_message_text("🚛 بخش ماشین‌ها به‌زودی فعال می‌شود.")
    elif data == "menu_cargo":
        await query.edit_message_text("📦 بخش بارها به‌زودی فعال می‌شود.")
    elif data == "menu_profile":
        from handlers.commands import profile_command
        await profile_command(update, context)
    elif data == "menu_referral":
        user = update.effective_user
        db_user = get_user(user.id)
        if db_user:
            link = f"https://t.me/{context.bot.username}?start={db_user['referral_code']}"
            await query.edit_message_text(
                f"🔗 لینک دعوت شما:\n{link}\n\nبا دعوت دوستان {5000} سکه جایزه بگیرید."
            )
        else:
            await query.edit_message_text("ابتدا ثبت‌نام کنید: /start")
    else:
        await query.edit_message_text("🔜 این بخش به‌زودی اضافه می‌شود.")
# handlers/callbacks.py
from trucks.handlers import show_brands

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "menu_trucks":
        await show_brands(update, context)   # <-- تغییر اینجا
    elif data == "menu_cargo":
        await query.edit_message_text("📦 بخش بارها به‌زودی فعال می‌شود.")
    # ... بقیه بدون تغییر
