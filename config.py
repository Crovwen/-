# config.py
import os

class Config:
    # توکن ربات (مستقیماً اینجا تغییر دهید)
    BOT_TOKEN = "8915187134:AAEpyyCEh9lHszxC5PjPzuOsb8VCVDfz9BA"

    # یوزرنیم کانال اجباری (بدون @)
    REQUIRED_CHANNEL = "Transit_game"

    # مسیر دیتابیس SQLite
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database", "game.db")

    # تنظیمات بازی
    REFERRAL_REWARD_REFERRER = 5000      # سکه
    REFERRAL_REWARD_NEW_USER = 2000      # سکه
    HOURLY_QUIZ_REWARD = 1000            # سکه (برای آینده)

    # پیام‌های ثابت
    CHANNEL_NAME_DISPLAY = "𝐓𝐫𝐚𝐧𝐬𝐢𝐭 | ترانزیت"
