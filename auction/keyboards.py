from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def auction_menu_keyboard(auction_id, current_bid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"💰 پیشنهاد {current_bid+1000}", callback_data=f"bid_{auction_id}_{current_bid+1000}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
    ]) 
