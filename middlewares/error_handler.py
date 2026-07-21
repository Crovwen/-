# middlewares/error_handler.py
import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """گرفتن تمام خطاهای پیش‌بینی‌نشده و لاگ آن بدون کرش"""
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    logger.error(f"Exception while handling an update: {context.error}\n{tb_string}")
    # می‌توان به کاربر پیام خطای عمومی داد، اما نه خطای فنی
    if update and hasattr(update, "effective_chat"):
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید."
            )
        except Exception:
            pass
