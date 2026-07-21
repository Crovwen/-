# bot.py
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import Config
from database.models import init_db
from middlewares.error_handler import error_handler
from handlers.commands import start_command, profile_command
from handlers.callbacks import check_membership_callback, menu_callback

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # راه‌اندازی دیتابیس
    init_db()
    logger.info("Database initialized.")

    # ساخت Application
    app = Application.builder().token(Config.BOT_TOKEN).build()

    # ثبت خطایاب سراسری
    app.add_error_handler(error_handler)

    # ثبت هندلرهای دستوری
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("profile", profile_command))

    # ثبت هندلرهای Callback
    app.add_handler(CallbackQueryHandler(check_membership_callback, pattern="^check_membership$"))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))

    logger.info("Bot started. Polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main() 
from trucks.handlers import show_brands, show_truck_list, show_truck_detail, buy_truck

# ... بعد از ثبت قبلی ها
app.add_handler(CallbackQueryHandler(show_brands, pattern="^menu_trucks$"))
app.add_handler(CallbackQueryHandler(show_truck_list, pattern="^brand_"))
app.add_handler(CallbackQueryHandler(show_truck_detail, pattern="^truck_"))
app.add_handler(CallbackQueryHandler(buy_truck, pattern="^buy_"))
# همچنین هندلر main_menu (برای بازگشت)
app.add_handler(CallbackQueryHandler(go_main_menu, pattern="^main_menu$"))
