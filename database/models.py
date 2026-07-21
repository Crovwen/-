# database/models.py
from database.connection import Database

def init_db():
    db = Database()
    # جدول کاربران
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language_code TEXT,
            is_premium INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 10000,     -- سکه شروع
            referral_code TEXT UNIQUE,
            referred_by INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referred_by) REFERENCES users(user_id) ON DELETE SET NULL
        );
    """)
    # ایندکس برای جستجوی کد رفرال
    db.execute("CREATE INDEX IF NOT EXISTS idx_referral_code ON users(referral_code);")
    db.execute("CREATE INDEX IF NOT EXISTS idx_referred_by ON users(referred_by);")
    db.commit()

def get_user(user_id: int):
    db = Database()
    cursor = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None

def create_user(user_id: int, username: str, first_name: str, last_name: str,
                language_code: str, is_premium: bool, referred_by: int = None):
    db = Database()
    # تولید کد رفرال یکتا
    referral_code = f"REF{user_id}{hash(user_id)%10000}"
    try:
        with db.connection:  # استفاده از context manager برای transaction
            db.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name,
                                            language_code, is_premium, referral_code, referred_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, language_code,
                  int(is_premium), referral_code, referred_by))
    except Exception as e:
        # اگر کاربر وجود داشت، ignore می‌کند
        pass
    return get_user(user_id)

def update_balance(user_id: int, amount: int):
    """افزایش یا کاهش موجودی (عدد مثبت افزایش، منفی کاهش)"""
    db = Database()
    with db.connection:
        cursor = db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ? AND balance + ? >= 0",
            (amount, user_id, amount)
        )
        if cursor.rowcount == 0:
            raise ValueError("موجودی کافی نیست یا کاربر وجود ندارد") 
# database/models.py (بخش اضافه‌شده)
def init_db():
    # ... (کدهای قبلی)
    # جدول کامیون‌های کاربر
    db.execute("""
        CREATE TABLE IF NOT EXISTS user_trucks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            truck_model TEXT NOT NULL,
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_user_trucks ON user_trucks(user_id, truck_model);")
    db.commit()

def add_user_truck(user_id: int, truck_model: str) -> bool:
    """اضافه کردن کامیون به گاراژ کاربر. اگر کاربر پول کافی نداشته باشد False برمی‌گرداند."""
    from .connection import Database
    db = Database()
    # ابتدا قیمت کامیون را از دیتای کامیون‌ها بگیریم (import از trucks.data)
    from trucks.data import TRUCK_PRICES  # بعداً تعریف می‌کنیم
    price = TRUCK_PRICES.get(truck_model)
    if price is None:
        raise ValueError("مدل کامیون نامعتبر است.")
    with db.connection:
        # قفل کردن ردیف کاربر و کسر موجودی
        cursor = db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ? AND balance >= ?",
            (price, user_id, price)
        )
        if cursor.rowcount == 0:
            return False  # موجودی کافی نیست
        # افزودن کامیون
        db.execute(
            "INSERT INTO user_trucks (user_id, truck_model) VALUES (?, ?)",
            (user_id, truck_model)
        )
        # اگر این اولین کامیون کاربر است، فعالش کن
        count = db.execute("SELECT COUNT(*) FROM user_trucks WHERE user_id = ?", (user_id,)).fetchone()[0]
        if count == 1:
            db.execute("UPDATE user_trucks SET is_active = 1 WHERE id = last_insert_rowid()")
    return True
