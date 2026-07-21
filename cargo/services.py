import random, logging
from datetime import datetime, timedelta
from database.connection import Database
from database.models import get_user_active_truck, update_balance
from trucks.data import TRUCK_DETAILS
from cargo.data import CARGO_TYPES, ROUTES, WEATHERS

logger = logging.getLogger(__name__)

def get_available_cargo_for_user(user_id: int) -> list:
    truck = get_user_active_truck(user_id)
    if not truck:
        return []
    truck_detail = TRUCK_DETAILS.get(truck["truck_model"])
    if not truck_detail:
        return []
    suitable = truck_detail["suitable_cargo"]
    available = []
    for c, data in CARGO_TYPES.items():
        if any(s in data["suitable_trucks"] for s in suitable):
            available.append(c)
    return available

def calculate_travel(user_id: int, cargo_type: str, route_name: str) -> dict:
    truck = get_user_active_truck(user_id)
    if not truck:
        raise ValueError("کامیون فعال ندارید")
    truck_model = truck["truck_model"]
    det = TRUCK_DETAILS[truck_model]
    cargo = CARGO_TYPES[cargo_type]
    route = ROUTES[route_name]

    # آب‌وهوای تصادفی
    weather = random.choice(list(WEATHERS.keys()))
    w = WEATHERS[weather]

    # محاسبه درآمد
    base_income = cargo["base_value"] * (1 + route["distance_km"]/500)
    income = int(base_income)

    # زمان سفر (دقیقه واقعی تبدیل به ثانیه‌های مجازی برای بازی)
    # هر 100 کیلومتر ~ 60 دقیقه واقعی؟ برای جذابیت از زمان کمتر: 1 دقیقه به ازای 10 کیلومتر
    # فاصله بر حسب km، زمان = (distance / speed) * time_mod * weather_speed_mult
    # سرعت میانگین فرضی 80 km/h، زمان واقعی = distance/80 ساعت.
    # برای بازی، زمان را کوچک می‌کنیم: 1 دقیقه واقعی = 1 ساعت بازی (اختیاری)
    travel_hours = (route["distance_km"] / det["optimal_speed"]) * route["time_mod"] * w["speed_mult"]
    # تبدیل به ثانیه (حداقل 5 ثانیه تا حداکثر 60 ثانیه برای تست)
    travel_seconds = max(10, int(travel_hours * 60))  # هر ساعت بازی = 1 دقیقه واقعی
    end_time = datetime.now() + timedelta(seconds=travel_seconds)

    # مصرف سوخت: distance * (fuel_consumption/100) * fuel_mod * weather_fuel_mult
    fuel_used = (route["distance_km"] * (det["fuel_consumption"]/100)) * route["fuel_mod"] * w["fuel_mult"]

    return {
        "weather": weather,
        "income": income,
        "travel_seconds": travel_seconds,
        "end_time": end_time,
        "fuel_used": fuel_used
    }

def start_travel_db(user_id: int, truck_id: int, cargo_type: str, route_name: str, travel_info: dict):
    db = Database()
    with db.connection:
        db.execute("""
            INSERT INTO active_travels (user_id, truck_id, cargo_type, route, weather,
                                        base_income, fuel_used, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, truck_id, cargo_type, route_name, travel_info["weather"],
              travel_info["income"], travel_info["fuel_used"], travel_info["end_time"]))
        last_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    return last_id

def complete_travel(travel_id: int, context):
    db = Database()
    travel = db.execute("SELECT * FROM active_travels WHERE id=? AND completed=0", (travel_id,)).fetchone()
    if not travel:
        return
    travel = dict(travel)
    # انجام محاسبات نهایی، اعمال خسارت، سوخت، اعتبار و ...
    user_id = travel["user_id"]
    truck_id = travel["truck_id"]
    income = travel["base_income"]

    # کسر سوخت (اگر سوخت کافی نباشد، جریمه)
    from database.models import init_truck_parts
    # سلامت قطعات را کاهش بده
    wear_rate = TRUCK_DETAILS[get_active_truck_model(truck_id)]["wear_rate"]
    route = ROUTES[travel["route"]]
    weather_mult = WEATHERS[travel["weather"]]["damage_mult"]
    damage = wear_rate * route["damage_mod"] * weather_mult * 5  # عدد کوچک
    # اعمال کاهش سلامت به قطعات
    parts = db.execute("SELECT * FROM truck_parts WHERE truck_id=?", (truck_id,)).fetchall()
    for part in parts:
        new_health = max(0, part["health"] - damage)
        db.execute("UPDATE truck_parts SET health=? WHERE id=?", (new_health, part["id"]))

    # جریمه سوخت
    fuel_used = travel["fuel_used"]
    # سوخت فعلی؟ فرض می‌کنیم باک پر بوده و fuel_used از 100 کسر می‌شود. ساده: بعداً مدیریت می‌کنیم.

    # افزایش موجودی
    update_balance(user_id, income)

    # ثبت در امتیازات هفتگی
    week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
    db.execute("""
        INSERT INTO weekly_scores (user_id, week_start, total_income, total_cargo_count, total_distance)
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT(user_id, week_start) DO UPDATE SET
            total_income = total_income + ?,
            total_cargo_count = total_cargo_count + 1,
            total_distance = total_distance + ?
    """, (user_id, week_start, income, route["distance_km"], income, route["distance_km"]))

    # علامت تکمیل
    db.execute("UPDATE active_travels SET completed=1 WHERE id=?", (travel_id,))
    db.commit()

    # ارسال پیام به کاربر
    try:
        context.bot.send_message(
            chat_id=user_id,
            text=f"✅ سفر تمام شد!\n💰 درآمد: {income:,} سکه\n🚛 خسارت تقریبی: {damage:.1f}%"
        )
    except Exception as e:
        logger.error(f"Failed to notify user {user_id}: {e}")

def get_active_truck_model(truck_id: int):
    db = Database()
    row = db.execute("SELECT truck_model FROM user_trucks WHERE id=?", (truck_id,)).fetchone()
    return row[0] if row else None

def reschedule_active_travels(job_queue):
    db = Database()
    travels = db.execute("SELECT * FROM active_travels WHERE completed=0").fetchall()
    for t in travels:
        t = dict(t)
        end = datetime.fromisoformat(t["end_time"])
        now = datetime.now()
        if end <= now:
            # فوراً کامل کن
            complete_travel(t["id"], None)  # context نیاز دارد، بهتر است در bot reschedule کنیم
        else:
            delay = (end - now).total_seconds()
            job_queue.run_once(lambda ctx, tid=t["id"]: complete_travel(tid, ctx), delay, data=t["id"])
