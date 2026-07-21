from telegram import Update
from telegram.ext import ContextTypes
from middlewares.membership import is_user_member, send_channel_join_prompt, require_membership
from keyboards.main_menu import main_menu_keyboard
from database.models import get_user
from trucks.handlers import show_brands
from cargo.handlers import show_cargo_list, select_route, start_travel
from parts.handlers import parts_menu_handler, repair_handler, upgrade_handler
from investments.handlers import buildings_menu, buy_building, upgrade_building
from market.handlers import market_menu, list_truck, buy_listed_truck, remove_listing
from auction.handlers import auction_menu, place_bid
from weekly.handlers import weekly_menu
import logging

logger = logging.getLogger(__name__)

async def check_membership_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await is_user_member(update, context):
        user = update.effective_user
        db_user = get_user(user.id)
        if db_user:
            from messages.welcome import welcome_message
            await query.edit_message_text(
                f"✅ عضویت شما تأیید شد! به بازی خوش آمدید، {user.first_name}",
                reply_markup=main_menu_keyboard()
            )
        else:
            from handlers.commands import start_command
            await start_command(update, context)
    else:
        await query.answer("❌ هنوز عضو کانال نیستید!", show_alert=True)

async def go_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from messages.welcome import welcome_message
    await query.edit_message_text(
        welcome_message(update.effective_user.first_name),
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

@require_membership
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    # دیسپچ به ماژول‌های مختلف
    if data == "menu_trucks":
        await show_brands(update, context)
    elif data == "menu_cargo":
        await show_cargo_list(update, context)
    elif data == "menu_parts":
        await parts_menu_handler(update, context)
    elif data == "menu_buildings":
        await buildings_menu(update, context)
    elif data == "menu_market":
        await market_menu(update, context)
    elif data == "menu_auction":
        await auction_menu(update, context)
    elif data == "menu_weekly":
        await weekly_menu(update, context)
    elif data == "menu_profile":
        from handlers.commands import profile_command
        await profile_command(update, context)
    elif data == "menu_referral":
        user = update.effective_user
        db_user = get_user(user.id)
        if db_user:
            link = f"https://t.me/{context.bot.username}?start={db_user['referral_code']}"
            await query.edit_message_text(f"🔗 لینک دعوت:\n{link}\n\nبا دعوت دوستان 5000 سکه جایزه بگیرید.")
        else:
            await query.edit_message_text("ابتدا ثبت‌نام کنید: /start")
    elif data == "menu_help":
        await query.edit_message_text("راهنما: ابتدا یک ماشین بخرید، سپس بار بگیرید و حمل کنید.")
    else:
        await query.answer("گزینه نامشخص")
