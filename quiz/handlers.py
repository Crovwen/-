import random, logging
from telegram import Update
from telegram.ext import ContextTypes
from database.connection import Database
from config import Config

logger = logging.getLogger(__name__)

async def hourly_quiz(context: ContextTypes.DEFAULT_TYPE):
    db = Database()
    groups = db.execute("SELECT chat_id FROM bot_groups").fetchall()
    for (chat_id,) in groups:
        try:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            op = random.choice(["+", "-", "*"])
            if op == "+":
                answer = a + b
            elif op == "-":
                answer = a - b
            else:
                answer = a * b
            msg = await context.bot.send_message(chat_id, f"🧮 سوال: {a} {op} {b} = ?")
            db.execute("INSERT OR REPLACE INTO active_quizzes (chat_id, message_id, answer) VALUES (?,?,?)",
                       (chat_id, msg.message_id, answer))
            db.commit()
        except Exception as e:
            logger.error(f"Quiz error in {chat_id}: {e}")

async def check_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg.text or not msg.text.strip().isdigit():
        return
    user_answer = int(msg.text.strip())
    chat_id = msg.chat.id
    db = Database()
    quiz = db.execute("SELECT * FROM active_quizzes WHERE chat_id=? AND answered=0", (chat_id,)).fetchone()
    if not quiz:
        return
    if user_answer == quiz["answer"]:
        db.execute("UPDATE active_quizzes SET answered=1 WHERE chat_id=?", (chat_id,))
        db.commit()
        try:
            update_balance(msg.from_user.id, Config.HOURLY_QUIZ_REWARD)
        except:
            pass
        await msg.reply_text(f"✅ آفرین {msg.from_user.first_name}! برنده {Config.HOURLY_QUIZ_REWARD} سکه شدی.")
