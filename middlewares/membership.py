from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import Config
from keyboards.channel_join import channel_join_keyboard
from functools import wraps

async def is_user_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(
            chat_id=f"@{Config.REQUIRED_CHANNEL}", user_id=user_id
        )
        return member.status not in ("left", "kicked")
    except:
        return False

async def send_channel_join_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = channel_join_keyboard()
    text = f"🚛 برای استفاده از ربات، ابتدا عضو کانال {Config.CHANNEL_NAME_DISPLAY} شوید.\n\nپس از عضویت، روی «بررسی عضویت» کلیک کنید."
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

def require_membership(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not await is_user_member(update, context):
            await send_channel_join_prompt(update, context)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
