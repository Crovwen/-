def cargo_info_message(cargo_type: str, cargo_data: dict) -> str:
    return (
        f"📦 بار: {cargo_type}\n"
        f"⚖️ وزن: {cargo_data['weight']} تن\n"
        f"💰 ارزش پایه: {cargo_data['base_value']:,} سکه\n"
        f"⏱ ضریب زمان: {cargo_data['time_mult']}\n"
        f"⚠️ ریسک: {cargo_data['risk']*100}%\n"
        f"📋 مناسب برای: {', '.join(cargo_data['suitable_trucks'])}"
    )
