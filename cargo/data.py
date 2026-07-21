# انواع بار
CARGO_TYPES = {
    "معمولی": {"weight": 20, "base_value": 3000, "time_mult": 1.0, "risk": 0.1, "suitable_trucks": ["معمولی", "حساس", "یخچالی"]},
    "حساس":    {"weight": 10, "base_value": 5000, "time_mult": 1.2, "risk": 0.2, "suitable_trucks": ["حساس", "یخچالی"]},
    "یخچالی":  {"weight": 25, "base_value": 7000, "time_mult": 1.1, "risk": 0.15,"suitable_trucks": ["یخچالی", "صنعتی"]},
    "فوق سنگین": {"weight": 40, "base_value": 12000,"time_mult": 1.5, "risk": 0.25,"suitable_trucks": ["فوق سنگین", "صنعتی"]},
    "صنعتی":   {"weight": 35, "base_value": 10000,"time_mult": 1.3, "risk": 0.2, "suitable_trucks": ["صنعتی", "فوق سنگین"]}
}

# مسیرها
ROUTES = {
    "اتوبان":     {"distance_km": 500, "time_mod": 0.8, "fuel_mod": 0.9, "risk_mod": 0.7, "damage_mod": 0.8},
    "جاده اصلی": {"distance_km": 400, "time_mod": 1.0, "fuel_mod": 1.0, "risk_mod": 1.0, "damage_mod": 1.0},
    "جاده فرعی": {"distance_km": 350, "time_mod": 1.3, "fuel_mod": 1.2, "risk_mod": 1.3, "damage_mod": 1.2},
    "کوهستانی":  {"distance_km": 300, "time_mod": 1.6, "fuel_mod": 1.5, "risk_mod": 1.6, "damage_mod": 1.5}
}

# آب‌وهوا
WEATHERS = {
    "آفتابی":  {"speed_mult": 1.0, "fuel_mult": 1.0, "damage_mult": 1.0, "risk_mult": 0.8},
    "بارانی":  {"speed_mult": 0.9, "fuel_mult": 1.05,"damage_mult": 1.1, "risk_mult": 1.1},
    "برفی":    {"speed_mult": 0.8, "fuel_mult": 1.15,"damage_mult": 1.3, "risk_mult": 1.4},
    "مه":      {"speed_mult": 0.85,"fuel_mult": 1.1, "damage_mult": 1.2, "risk_mult": 1.3},
    "طوفان":   {"speed_mult": 0.7, "fuel_mult": 1.2, "damage_mult": 1.5, "risk_mult": 1.8}
}
