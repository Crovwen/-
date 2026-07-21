import os

class Config:
    BOT_TOKEN = "8915187134:AAEpyyCEh9lHszxC5PjPzuOsb8VCVDfz9BA"  # توکن ربات را اینجا بگذارید
    REQUIRED_CHANNEL = "Transit_game"
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database", "game.db")
    REFERRAL_REWARD_REFERRER = 5000
    REFERRAL_REWARD_NEW_USER = 2000
    HOURLY_QUIZ_REWARD = 1000
    CHANNEL_NAME_DISPLAY = "𝐓𝐫𝐚𝐧𝐬𝐢𝐭 | ترانزیت"
    INITIAL_BALANCE = 10000  # سکه شروع
