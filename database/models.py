from database.connection import Database

def init_db():
    db = Database()
    # کاربران
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language_code TEXT,
            is_premium INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 10000,
            referral_code TEXT UNIQUE,
            referred_by INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referred_by) REFERENCES users(user_id) ON DELETE SET NULL
        );
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_referral_code ON users(referral_code);")
    db.execute("CREATE INDEX IF NOT EXISTS idx_referred_by ON users(referred_by);")

    # کامیون‌های کاربر
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

    # سلامت قطعات هر کامیون (هر رکورد برای یک قطعه از یک کامیون)
    db.execute("""
        CREATE TABLE IF NOT EXISTS truck_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id INTEGER NOT NULL,
            part_name TEXT NOT NULL,
            health REAL DEFAULT 100.0,
            upgrade_level INTEGER DEFAULT 0,
            FOREIGN KEY (truck_id) REFERENCES user_trucks(id) ON DELETE CASCADE,
            UNIQUE(truck_id, part_name)
        );
    """)

    # سفرهای فعال
    db.execute("""
        CREATE TABLE IF NOT EXISTS active_travels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            truck_id INTEGER NOT NULL,
            cargo_type TEXT NOT NULL,
            route TEXT NOT NULL,
            weather TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP NOT NULL,
            base_income INTEGER NOT NULL,
            fuel_used REAL NOT NULL,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (truck_id) REFERENCES user_trucks(id)
        );
    """)

    # املاک کاربر (ساختمان‌ها)
    db.execute("""
        CREATE TABLE IF NOT EXISTS user_buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            building_type TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, building_type)
        );
    """)

    # آگهی‌های فروش کامیون در بازار
    db.execute("""
        CREATE TABLE IF NOT EXISTS market_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            truck_id INTEGER NOT NULL,
            price INTEGER NOT NULL,
            listed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sold INTEGER DEFAULT 0,
            FOREIGN KEY (seller_id) REFERENCES users(user_id),
            FOREIGN KEY (truck_id) REFERENCES user_trucks(id)
        );
    """)

    # مزایده‌های بار
    db.execute("""
        CREATE TABLE IF NOT EXISTS auction_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo_data TEXT NOT NULL,
            starting_price INTEGER NOT NULL,
            current_bid INTEGER,
            highest_bidder INTEGER,
            end_time TIMESTAMP NOT NULL,
            active INTEGER DEFAULT 1,
            FOREIGN KEY (highest_bidder) REFERENCES users(user_id)
        );
    """)

    # امتیازات هفتگی
    db.execute("""
        CREATE TABLE IF NOT EXISTS weekly_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            week_start DATE NOT NULL,
            total_income INTEGER DEFAULT 0,
            total_cargo_count INTEGER DEFAULT 0,
            total_distance REAL DEFAULT 0,
            total_damage_cost INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_weekly ON weekly_scores(week_start, user_id);")

    # گروه‌هایی که ربات در آن‌ها عضو است (برای سوال ساعتی)
    db.execute("""
        CREATE TABLE IF NOT EXISTS bot_groups (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # سوالات فعال در گروه‌ها
    db.execute("""
        CREATE TABLE IF NOT EXISTS active_quizzes (
            chat_id INTEGER PRIMARY KEY,
            message_id INTEGER,
            answer INTEGER,
            answered INTEGER DEFAULT 0,
            asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    db.commit()

# ========== توابع کاربران ==========
def get_user(user_id: int):
    db = Database()
    cursor = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None

def create_user(user_id, username, first_name, last_name, language_code, is_premium, referred_by=None):
    db = Database()
    referral_code = f"REF{user_id}{hash(user_id)%10000}"
    try:
        with db.connection:
            db.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name,
                                            language_code, is_premium, referral_code, referred_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, language_code, int(is_premium), referral_code, referred_by))
    except:
        pass
    return get_user(user_id)

def update_balance(user_id: int, amount: int):
    db = Database()
    with db.connection:
        cursor = db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ? AND balance + ? >= 0",
            (amount, user_id, amount)
        )
        if cursor.rowcount == 0:
            raise ValueError("موجودی کافی نیست یا کاربر وجود ندارد")

def get_user_active_truck(user_id: int):
    db = Database()
    cursor = db.execute(
        "SELECT * FROM user_trucks WHERE user_id = ? AND is_active = 1", (user_id,)
    )
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None

def add_user_truck(user_id: int, truck_model: str):
    from trucks.data import TRUCK_PRICES
    price = TRUCK_PRICES.get(truck_model)
    if price is None:
        raise ValueError("مدل کامیون نامعتبر")
    db = Database()
    with db.connection:
        cursor = db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ? AND balance >= ?",
            (price, user_id, price)
        )
        if cursor.rowcount == 0:
            return False
        db.execute(
            "INSERT INTO user_trucks (user_id, truck_model) VALUES (?, ?)",
            (user_id, truck_model)
        )
        # اولین کامیون -> فعال کن
        count = db.execute("SELECT COUNT(*) FROM user_trucks WHERE user_id = ?", (user_id,)).fetchone()[0]
        if count == 1:
            last_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.execute("UPDATE user_trucks SET is_active = 1 WHERE id = ?", (last_id,))
    return True

def set_active_truck(user_id: int, truck_id: int):
    db = Database()
    with db.connection:
        db.execute("UPDATE user_trucks SET is_active = 0 WHERE user_id = ?", (user_id,))
        db.execute("UPDATE user_trucks SET is_active = 1 WHERE id = ? AND user_id = ?", (truck_id, user_id))

def init_truck_parts(truck_id: int):
    parts = ["engine", "gearbox", "tire", "brake", "air_filter", "oil_filter"]
    db = Database()
    with db.connection:
        for p in parts:
            db.execute(
                "INSERT OR IGNORE INTO truck_parts (truck_id, part_name) VALUES (?, ?)",
                (truck_id, p)
            )
    # مقدار fuel جداگانه ذخیره می‌شود، اینجا فقط اولیه 100% 
