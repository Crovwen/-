from trucks.data import TRUCK_DETAILS, TRUCK_PRICES
from trucks.keyboards import custom_emoji, EMOJI_IDS

def truck_detail_message(truck_name: str) -> str:
    det = TRUCK_DETAILS[truck_name]
    logo = custom_emoji(EMOJI_IDS.get(det["brand"]), "🚛")
    pros = "\n".join(f"  ✓ {p}" for p in det["pros"]) if det["pros"] else "  -"
    cons = "\n".join(f"  ✗ {c}" for c in det["cons"]) if det["cons"] else "  -"
    suitable = "، ".join(det["suitable_cargo"])
    return (
        f"{logo} **{truck_name}**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚙️ قدرت: {det['power_hp']} hp\n"
        f"🚚 کاربری: {det['usage']}\n"
        f"⚖️ ظرفیت: {det['load_capacity_tons']} تن\n"
        f"⛽ مصرف: {det['fuel_consumption']} L/100km\n"
        f"🛢️ باک: {det['tank_volume']} L\n"
        f"🏁 سرعت: {det['optimal_speed']} km/h\n"
        f"🔧 استهلاک: {det['wear_rate']}\n"
        f"💰 قیمت: {TRUCK_PRICES[truck_name]:,} سکه\n\n"
        f"📦 مناسب: {suitable}\n"
        f"✅ مزایا:\n{pros}\n"
        f"❌ معایب:\n{cons}"
    )
