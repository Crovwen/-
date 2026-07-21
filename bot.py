import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, JobQueue
from config import Config
from database.models import init_db
from middlewares.error_handler import error_handler
from handlers.commands import start_command, profile_command
from handlers.callbacks import (
    check_membership_callback, go_main_menu, menu_callback
)
from trucks.handlers import show_brands, show_truck_list, show_truck_detail, buy_truck
from cargo.handlers import show_cargo_list, select_route, start_travel
from parts.handlers import parts_menu_handler, repair_handler, upgrade_handler
from investments.handlers import buildings_menu, buy_building, upgrade_building
from market.handlers import market_menu, list_truck, buy_listed_truck
from auction.handlers import auction_menu, place_bid
from weekly.handlers import weekly_menu
from quiz.handlers import hourly_quiz, check_quiz_answer
#from handlers.group_events import track_group

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    init_db()
    app = Application.builder().token(Config.BOT_TOKEN).build()

    # job queue
    job_queue = app.job_queue
    job_queue.run_repeating(hourly_quiz, interval=3600, first=10)
    # ریست هفتگی: هر دوشنبه ساعت ۰
    # job_queue.run_daily(weekly_reset, days=(0,), time=time(hour=0)) # در صورت نیاز

    app.add_error_handler(error_handler)

    # command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("profile", profile_command))

    # callback handlers
    app.add_handler(CallbackQueryHandler(check_membership_callback, pattern="^check_membership$"))
    app.add_handler(CallbackQueryHandler(go_main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))

    # trucks
    app.add_handler(CallbackQueryHandler(show_truck_list, pattern="^brand_"))
    app.add_handler(CallbackQueryHandler(show_truck_detail, pattern="^truck_"))
    app.add_handler(CallbackQueryHandler(buy_truck, pattern="^buy_"))

    # cargo
    app.add_handler(CallbackQueryHandler(select_route, pattern="^cargo_"))
    app.add_handler(CallbackQueryHandler(start_travel, pattern="^route_"))

    # parts
    app.add_handler(CallbackQueryHandler(repair_handler, pattern="^repair_"))
    app.add_handler(CallbackQueryHandler(upgrade_handler, pattern="^upgrade_"))

    # investments
    app.add_handler(CallbackQueryHandler(buy_building, pattern="^buybuilding_"))
    app.add_handler(CallbackQueryHandler(upgrade_building, pattern="^upgradebuilding_"))

    # market
    app.add_handler(CallbackQueryHandler(buy_listed_truck, pattern="^buymarket_"))
    # auction
    app.add_handler(CallbackQueryHandler(place_bid, pattern="^bid_"))

    # group tracking
    #app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_group))
    # quiz answer
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_quiz_answer), group=1)

    logger.info("Bot started...")
    app.run_polling(allowed_updates=["message", "callback_query", "chat_member"])

if __name__ == "__main__":
    main()
