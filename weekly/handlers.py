# weekly/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from database.connection import Database
from datetime import date, timedelta

async def weekly_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    week_start = date.today() - timedelta(days=date.today().weekday())
    db = Database()
    scores = db.execute("""
        SELECT user_id, total_income FROM weekly_scores
        WHERE week_start = ? ORDER BY total_income DESC LIMIT 10
    """, (week_start,)).fetchall()
    text = "🏆 رقابت هفتگی:\n" + "\n".join(f"{i+1}. {s[0]}: {s[1]} سکه" for i,s in enumerate(scores))
    await query.edit_message_text(text)
