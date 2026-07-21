from telegram import Update
from telegram.ext import ContextTypes
from database.connection import Database

async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """وقتی ربات به یک گروه جدید اضافه می‌شود، آن را در دیتابیس ثبت کند."""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            db = Database()
            db.execute(
                "INSERT OR IGNORE INTO bot_groups (chat_id, title) VALUES (?, ?)",
                (update.effective_chat.id, update.effective_chat.title)
            )
            db.commit()
