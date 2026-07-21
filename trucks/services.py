# trucks/services.py
from database.models import add_user_truck

def purchase_truck(user_id: int, truck_model: str) -> tuple[bool, str]:
    """
    تلاش برای خرید کامیون.
    خروجی: (success, message)
    """
    try:
        result = add_user_truck(user_id, truck_model)
        if result:
            return True, "✅ خرید با موفقیت انجام شد! کامیون به گاراژ شما اضافه شد."
        else:
            return False, "❌ موجودی سکه شما کافی نیست."
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Purchase error for user {user_id}: {e}")
        return False, "⚠️ مشکلی در خرید پیش آمد. لطفاً دوباره تلاش کنید."
