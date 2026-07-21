from database.models import add_user_truck, init_truck_parts
from database.connection import Database

def purchase_truck(user_id: int, truck_model: str) -> tuple[bool, str]:
    try:
        result = add_user_truck(user_id, truck_model)
        if result:
            # قطعات اولیه را ایجاد کن
            db = Database()
            truck = db.execute("SELECT id FROM user_trucks WHERE user_id=? AND truck_model=? ORDER BY id DESC LIMIT 1",
                               (user_id, truck_model)).fetchone()
            if truck:
                init_truck_parts(truck[0])
            return True, "✅ خرید با موفقیت انجام شد!"
        else:
            return False, "❌ موجودی سکه کافی نیست."
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Purchase error: {e}")
        return False, "⚠️ خطا در خرید."
