# trucks/messages.py
from trucks.data import TRUCK_DETAILS, TRUCK_PRICES
from trucks.keyboards import custom_emoji, EMOJI_IDS

def truck_detail_message(truck_name: str) -> str:
    det = TRUCK_DETAILS[truck_name]
    brand = det["brand"]
    logo = custom_emoji(EMOJI_IDS.get(brand), "🚛")
    parts_emoji = {
        "engine": custom_emoji(5348110594287367157, "⚙️"),
        "gearbox": custom_emoji(5348498150661322304, "⚙️"),
        "tire": custom_emoji(5346177257708749202, "🛞"),
        "brake": custom_emoji(5460747335690654731, "🛑"),
        "air_filter": custom_emoji(5452100432652442573, "🌬️"),
        "oil_filter": custom_emoji(5454404570937592123, "🛢️"),
        "check_engine": custom_emoji(5188577405626784687, "⚠️"),
        "fuel": custom_emoji(5188634915238872632, "⛽"),
    }
    pros = "\n".join(f"  ✓ {p}" for p in det["pros"]) if det["pros"] else "  -"
    cons = "\n".join(f"  ✗ {c}" for c in det["cons"]) if det["cons"] else "  -"
    suitable = "، ".join(det["suitable_cargo"])
    return (
        f"{logo} **{truck_name}**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{parts_emoji['engine']} قدرت موتور: {det['power_hp']} اسب بخار\n"
        f"🚚 نوع کاربری: {det['usage']}\n"
        f"⚖️ ظرفیت حمل: {det['load_capacity_tons']} تن\n"
        f"{parts_emoji['fuel']} مصرف سوخت: {det['fuel_consumption']} L/100km\n"
        f"⛽ حجم باک: {det['tank_volume']} لیتر\n"
        f"🏁 سرعت مناسب: {det['optimal_speed']} km/h\n"
        f"{parts_emoji['check_engine']} نرخ استهلاک: {det['wear_rate']}\n"
        f"🔧 هزینه تعمیر پایه: {det['repair_cost_base']} سکه\n"
        f"💰 قیمت خرید: {TRUCK_PRICES[truck_name]:,} سکه\n\n"
        f"📦 مناسب برای بارهای: {suitable}\n\n"
        f"✅ مزایا:\n{pros}\n\n"
        f"❌ معایب:\n{cons}"
    )
