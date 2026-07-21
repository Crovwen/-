# keyboards/channel_join.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config

def channel_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{Config.REQUIRED_CHANNEL}")],
        [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check_membership")]
    ])
