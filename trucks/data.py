# trucks/data.py

# قیمت‌های خرید (بر اساس قدرت و ارزش واقعی)
TRUCK_PRICES = {
    # Scania
    "Scania S770 V8": 24000,
    "Scania R770 V8": 23000,
    "Scania S660 V8": 21000,
    "Scania R660 V8": 20000,
    "Scania S590": 18000,
    "Scania R590": 17000,
    "Scania 560 Super": 16000,
    "Scania G560": 15000,
    "Scania G500": 13000,
    "Scania P410": 10000,
    # Volvo
    "Volvo FH16 750": 23500,
    "Volvo FH16 700": 22000,
    "Volvo FH16 650": 21000,
    "Volvo FH16 600": 20000,
    "Volvo FH540": 15000,
    "Volvo FH500": 14000,
    "Volvo FH460": 12500,
    "Volvo FMX 540": 15500,
    "Volvo FMX 500": 14500,
    "Volvo FM 420": 11000,
    # Mercedes
    "Mercedes Actros L 1863": 22500,
    "Mercedes Arocs 4163": 22000,
    "Mercedes Arocs 3358": 19000,
    "Mercedes Actros 1853": 18000,
    "Mercedes Arocs 2653": 17500,
    "Mercedes Actros 1851": 17000,
    "Mercedes Actros 1848": 15000,
    "Mercedes Econic 2635": 12000,
    "Mercedes Atego 1530": 8000,
    "Mercedes Unimog U5023": 7500,
    # DAF
    "DAF XG+ 530": 17500,
    "DAF XF 530": 17000,
    "DAF CF 530": 16500,
    "DAF XG 480": 14500,
    "DAF XF 480": 14000,
    "DAF XD 480": 13500,
    "DAF XF 450": 13000,
    "DAF CF 450": 12500,
    "DAF XD 410": 10500,
    "DAF LF 260": 6500,
    # MAN
    "MAN TGX 640": 21000,
    "MAN TGX 580": 18500,
    "MAN HX 520": 18000,
    "MAN TGX 510": 17500,
    "MAN TGS 510": 17000,
    "MAN TGS 41.480": 14000,
    "MAN TGX 470": 13500,
    "MAN TGS 430": 11000,
    "MAN TGM 290": 7500,
    "MAN TGL 250": 6000,
}

# مشخصات کامل هر کامیون
TRUCK_DETAILS = {
    # ==================== SCANIA ====================
    "Scania S770 V8": {
        "brand": "Scania",
        "power_hp": 770,
        "usage": "کشنده فوق سنگین",
        "load_capacity_tons": 45,
        "fuel_consumption": 32.5,
        "tank_volume": 800,
        "optimal_speed": 90,
        "wear_rate": 0.8,
        "repair_cost_base": 1800,
        "pros": ["قدرت فوق‌العاده", "کابین لوکس", "مصرف بهینه در مسیرهای طولانی"],
        "cons": ["هزینه تعمیر بالا", "استهلاک لاستیک در بارهای سنگین"],
        "suitable_cargo": ["فوق سنگین", "صنعتی", "یخچالی", "حساس"]
    },
    "Scania R770 V8": {
        "brand": "Scania", "power_hp": 770, "usage": "کشنده",
        "load_capacity_tons": 44, "fuel_consumption": 33.0, "tank_volume": 750,
        "optimal_speed": 90, "wear_rate": 0.85, "repair_cost_base": 1700,
        "pros": ["کشنده قدرتمند", "دوام بالا"],
        "cons": ["کابین کمی کوچک‌تر"],
        "suitable_cargo": ["فوق سنگین", "صنعتی"]
    },
    "Scania S660 V8": {
        "brand": "Scania", "power_hp": 660, "usage": "کشنده سنگین",
        "load_capacity_tons": 42, "fuel_consumption": 31.0, "tank_volume": 700,
        "optimal_speed": 89, "wear_rate": 0.9, "repair_cost_base": 1600,
        "pros": ["نسبت قدرت به مصرف عالی"], "cons": [],
        "suitable_cargo": ["صنعتی", "یخچالی", "فوق سنگین"]
    },
    "Scania R660 V8": {
        "brand": "Scania", "power_hp": 660, "usage": "کشنده",
        "load_capacity_tons": 42, "fuel_consumption": 31.5, "tank_volume": 700,
        "optimal_speed": 89, "wear_rate": 0.9, "repair_cost_base": 1600,
        "pros": [], "cons": [],
        "suitable_cargo": ["صنعتی"]
    },
    "Scania S590": {
        "brand": "Scania", "power_hp": 590, "usage": "کشنده",
        "load_capacity_tons": 40, "fuel_consumption": 30.0, "tank_volume": 650,
        "optimal_speed": 88, "wear_rate": 1.0, "repair_cost_base": 1500,
        "pros": ["اقتصادی"], "cons": [],
        "suitable_cargo": ["یخچالی", "معمولی"]
    },
    "Scania R590": {
        "brand": "Scania", "power_hp": 590, "usage": "کشنده",
        "load_capacity_tons": 40, "fuel_consumption": 30.5, "tank_volume": 650,
        "optimal_speed": 88, "wear_rate": 1.0, "repair_cost_base": 1500,
        "pros": [], "cons": [],
        "suitable_cargo": ["یخچالی"]
    },
    "Scania 560 Super": {
        "brand": "Scania", "power_hp": 560, "usage": "کشنده",
        "load_capacity_tons": 38, "fuel_consumption": 29.0, "tank_volume": 600,
        "optimal_speed": 87, "wear_rate": 1.1, "repair_cost_base": 1400,
        "pros": ["مصرف کم", "مناسب بارهای سنگین"], "cons": [],
        "suitable_cargo": ["سنگین", "معمولی"]
    },
    "Scania G560": {
        "brand": "Scania", "power_hp": 560, "usage": "باری",
        "load_capacity_tons": 36, "fuel_consumption": 29.5, "tank_volume": 600,
        "optimal_speed": 85, "wear_rate": 1.2, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی", "سنگین"]
    },
    "Scania G500": {
        "brand": "Scania", "power_hp": 500, "usage": "باری",
        "load_capacity_tons": 33, "fuel_consumption": 28.0, "tank_volume": 550,
        "optimal_speed": 84, "wear_rate": 1.3, "repair_cost_base": 1300,
        "pros": ["مناسب شروع"], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "Scania P410": {
        "brand": "Scania", "power_hp": 410, "usage": "توزیع",
        "load_capacity_tons": 28, "fuel_consumption": 26.0, "tank_volume": 400,
        "optimal_speed": 80, "wear_rate": 1.5, "repair_cost_base": 1100,
        "pros": ["ارزان", "نگهداری کم"], "cons": ["بارهای سنگین ممنوع"],
        "suitable_cargo": ["معمولی", "حساس"]
    },

    # ==================== VOLVO ====================
    "Volvo FH16 750": {
        "brand": "Volvo", "power_hp": 750, "usage": "کشنده فوق سنگین",
        "load_capacity_tons": 44, "fuel_consumption": 31.8, "tank_volume": 780,
        "optimal_speed": 90, "wear_rate": 0.82, "repair_cost_base": 1750,
        "pros": ["قدرت بالا", "ایمنی"], "cons": ["هزینه سوخت"],
        "suitable_cargo": ["فوق سنگین", "صنعتی", "یخچالی"]
    },
    "Volvo FH16 700": {
        "brand": "Volvo", "power_hp": 700, "usage": "کشنده",
        "load_capacity_tons": 43, "fuel_consumption": 31.5, "tank_volume": 750,
        "optimal_speed": 90, "wear_rate": 0.85, "repair_cost_base": 1700,
        "pros": [], "cons": [],
        "suitable_cargo": ["صنعتی"]
    },
    "Volvo FH16 650": {
        "brand": "Volvo", "power_hp": 650, "usage": "کشنده",
        "load_capacity_tons": 42, "fuel_consumption": 31.0, "tank_volume": 720,
        "optimal_speed": 89, "wear_rate": 0.9, "repair_cost_base": 1650,
        "pros": [], "cons": [],
        "suitable_cargo": ["صنعتی"]
    },
    "Volvo FH16 600": {
        "brand": "Volvo", "power_hp": 600, "usage": "کشنده",
        "load_capacity_tons": 40, "fuel_consumption": 30.5, "tank_volume": 700,
        "optimal_speed": 88, "wear_rate": 0.95, "repair_cost_base": 1600,
        "pros": ["عملکرد متعادل"], "cons": [],
        "suitable_cargo": ["سنگین"]
    },
    "Volvo FH540": {
        "brand": "Volvo", "power_hp": 540, "usage": "کشنده",
        "load_capacity_tons": 38, "fuel_consumption": 29.0, "tank_volume": 650,
        "optimal_speed": 87, "wear_rate": 1.1, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["یخچالی", "معمولی"]
    },
    "Volvo FH500": {
        "brand": "Volvo", "power_hp": 500, "usage": "کشنده",
        "load_capacity_tons": 35, "fuel_consumption": 28.0, "tank_volume": 600,
        "optimal_speed": 86, "wear_rate": 1.2, "repair_cost_base": 1300,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "Volvo FH460": {
        "brand": "Volvo", "power_hp": 460, "usage": "کشنده",
        "load_capacity_tons": 33, "fuel_consumption": 27.0, "tank_volume": 550,
        "optimal_speed": 85, "wear_rate": 1.3, "repair_cost_base": 1200,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "Volvo FMX 540": {
        "brand": "Volvo", "power_hp": 540, "usage": "کمپرسی/ساخت‌وساز",
        "load_capacity_tons": 35, "fuel_consumption": 30.0, "tank_volume": 600,
        "optimal_speed": 80, "wear_rate": 1.2, "repair_cost_base": 1450,
        "pros": ["مقاوم در جاده‌های بد"], "cons": ["سرعت کم"],
        "suitable_cargo": ["سنگین", "صنعتی"]
    },
    "Volvo FMX 500": {
        "brand": "Volvo", "power_hp": 500, "usage": "کمپرسی",
        "load_capacity_tons": 33, "fuel_consumption": 29.5, "tank_volume": 580,
        "optimal_speed": 80, "wear_rate": 1.3, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["سنگین"]
    },
    "Volvo FM 420": {
        "brand": "Volvo", "power_hp": 420, "usage": "توزیع",
        "load_capacity_tons": 30, "fuel_consumption": 27.5, "tank_volume": 450,
        "optimal_speed": 82, "wear_rate": 1.4, "repair_cost_base": 1150,
        "pros": ["مناسب شهر"], "cons": ["ضعیف در بارهای فوق سنگین"],
        "suitable_cargo": ["معمولی", "حساس"]
    },

    # ==================== MERCEDES ====================
    "Mercedes Actros L 1863": {
        "brand": "Mercedes", "power_hp": 630, "usage": "کشنده لوکس",
        "load_capacity_tons": 43, "fuel_consumption": 30.0, "tank_volume": 750,
        "optimal_speed": 89, "wear_rate": 0.9, "repair_cost_base": 1700,
        "pros": ["کابین دیجیتال", "امکانات ایمنی"], "cons": [],
        "suitable_cargo": ["صنعتی", "یخچالی"]
    },
    "Mercedes Arocs 4163": {
        "brand": "Mercedes", "power_hp": 630, "usage": "کمپرسی سنگین",
        "load_capacity_tons": 44, "fuel_consumption": 32.0, "tank_volume": 700,
        "optimal_speed": 82, "wear_rate": 0.95, "repair_cost_base": 1750,
        "pros": ["مناسب معدن"], "cons": ["مصرف بالا"],
        "suitable_cargo": ["فوق سنگین", "صنعتی"]
    },
    "Mercedes Arocs 3358": {
        "brand": "Mercedes", "power_hp": 580, "usage": "کمپرسی",
        "load_capacity_tons": 40, "fuel_consumption": 30.5, "tank_volume": 650,
        "optimal_speed": 83, "wear_rate": 1.0, "repair_cost_base": 1600,
        "pros": ["قابل اعتماد"], "cons": [],
        "suitable_cargo": ["صنعتی", "سنگین"]
    },
    "Mercedes Actros 1853": {
        "brand": "Mercedes", "power_hp": 530, "usage": "کشنده",
        "load_capacity_tons": 38, "fuel_consumption": 28.0, "tank_volume": 600,
        "optimal_speed": 87, "wear_rate": 1.1, "repair_cost_base": 1450,
        "pros": ["مقرون به صرفه"], "cons": [],
        "suitable_cargo": ["یخچالی", "معمولی"]
    },
    "Mercedes Arocs 2653": {
        "brand": "Mercedes", "power_hp": 530, "usage": "کمپرسی",
        "load_capacity_tons": 36, "fuel_consumption": 29.0, "tank_volume": 550,
        "optimal_speed": 83, "wear_rate": 1.2, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["سنگین", "صنعتی"]
    },
    "Mercedes Actros 1851": {
        "brand": "Mercedes", "power_hp": 510, "usage": "کشنده",
        "load_capacity_tons": 36, "fuel_consumption": 27.5, "tank_volume": 570,
        "optimal_speed": 86, "wear_rate": 1.2, "repair_cost_base": 1350,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "Mercedes Actros 1848": {
        "brand": "Mercedes", "power_hp": 480, "usage": "کشنده",
        "load_capacity_tons": 34, "fuel_consumption": 26.5, "tank_volume": 520,
        "optimal_speed": 85, "wear_rate": 1.3, "repair_cost_base": 1250,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی", "حساس"]
    },
    "Mercedes Econic 2635": {
        "brand": "Mercedes", "power_hp": 350, "usage": "شهری/زباله",
        "load_capacity_tons": 26, "fuel_consumption": 28.0, "tank_volume": 300,
        "optimal_speed": 70, "wear_rate": 1.5, "repair_cost_base": 950,
        "pros": ["کابین جادار"], "cons": ["قدرت کم"],
        "suitable_cargo": ["معمولی"]
    },
    "Mercedes Atego 1530": {
        "brand": "Mercedes", "power_hp": 300, "usage": "توزیع سبک",
        "load_capacity_tons": 18, "fuel_consumption": 22.0, "tank_volume": 200,
        "optimal_speed": 80, "wear_rate": 1.7, "repair_cost_base": 700,
        "pros": ["چابک", "مصرف کم"], "cons": ["ظرفیت پایین"],
        "suitable_cargo": ["معمولی", "حساس"]
    },
    "Mercedes Unimog U5023": {
        "brand": "Mercedes", "power_hp": 230, "usage": "آفرود",
        "load_capacity_tons": 14, "fuel_consumption": 24.0, "tank_volume": 160,
        "optimal_speed": 60, "wear_rate": 1.6, "repair_cost_base": 800,
        "pros": ["عبور از هر مسیر"], "cons": ["سرعت بسیار پایین"],
        "suitable_cargo": ["حساس", "معمولی"]
    },

    # ==================== DAF ====================
    "DAF XG+ 530": {
        "brand": "DAF", "power_hp": 530, "usage": "کشنده لوکس",
        "load_capacity_tons": 38, "fuel_consumption": 27.0, "tank_volume": 700,
        "optimal_speed": 87, "wear_rate": 1.0, "repair_cost_base": 1450,
        "pros": ["کابین عالی", "مصرف کم"], "cons": [],
        "suitable_cargo": ["یخچالی", "معمولی"]
    },
    "DAF XF 530": {
        "brand": "DAF", "power_hp": 530, "usage": "کشنده",
        "load_capacity_tons": 38, "fuel_consumption": 27.5, "tank_volume": 680,
        "optimal_speed": 87, "wear_rate": 1.05, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی", "یخچالی"]
    },
    "DAF CF 530": {
        "brand": "DAF", "power_hp": 530, "usage": "ساخت‌وساز/باری",
        "load_capacity_tons": 36, "fuel_consumption": 28.5, "tank_volume": 600,
        "optimal_speed": 84, "wear_rate": 1.2, "repair_cost_base": 1400,
        "pros": ["مقاوم"], "cons": [],
        "suitable_cargo": ["سنگین", "صنعتی"]
    },
    "DAF XG 480": {
        "brand": "DAF", "power_hp": 480, "usage": "کشنده",
        "load_capacity_tons": 34, "fuel_consumption": 26.0, "tank_volume": 650,
        "optimal_speed": 86, "wear_rate": 1.15, "repair_cost_base": 1300,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "DAF XF 480": {
        "brand": "DAF", "power_hp": 480, "usage": "کشنده",
        "load_capacity_tons": 34, "fuel_consumption": 26.5, "tank_volume": 620,
        "optimal_speed": 86, "wear_rate": 1.15, "repair_cost_base": 1300,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "DAF XD 480": {
        "brand": "DAF", "power_hp": 480, "usage": "توزیع منطقه‌ای",
        "load_capacity_tons": 32, "fuel_consumption": 27.0, "tank_volume": 550,
        "optimal_speed": 85, "wear_rate": 1.2, "repair_cost_base": 1250,
        "pros": ["مناسب حمل شهری"], "cons": [],
        "suitable_cargo": ["معمولی", "حساس"]
    },
    "DAF XF 450": {
        "brand": "DAF", "power_hp": 450, "usage": "کشنده",
        "load_capacity_tons": 32, "fuel_consumption": 25.5, "tank_volume": 580,
        "optimal_speed": 85, "wear_rate": 1.25, "repair_cost_base": 1200,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "DAF CF 450": {
        "brand": "DAF", "power_hp": 450, "usage": "باری/ساخت‌وساز",
        "load_capacity_tons": 32, "fuel_consumption": 26.5, "tank_volume": 500,
        "optimal_speed": 83, "wear_rate": 1.3, "repair_cost_base": 1150,
        "pros": ["قابلیت تطبیق"], "cons": [],
        "suitable_cargo": ["سنگین", "معمولی"]
    },
    "DAF XD 410": {
        "brand": "DAF", "power_hp": 410, "usage": "توزیع",
        "load_capacity_tons": 28, "fuel_consumption": 24.0, "tank_volume": 400,
        "optimal_speed": 82, "wear_rate": 1.4, "repair_cost_base": 1050,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "DAF LF 260": {
        "brand": "DAF", "power_hp": 260, "usage": "سبک شهری",
        "load_capacity_tons": 12, "fuel_consumption": 20.0, "tank_volume": 150,
        "optimal_speed": 75, "wear_rate": 1.8, "repair_cost_base": 600,
        "pros": ["ارزان", "نگهداری آسان"], "cons": ["بسیار ضعیف در مسیرهای طولانی"],
        "suitable_cargo": ["معمولی", "حساس"]
    },

    # ==================== MAN ====================
    "MAN TGX 640": {
        "brand": "MAN", "power_hp": 640, "usage": "کشنده قدرتمند",
        "load_capacity_tons": 43, "fuel_consumption": 30.0, "tank_volume": 750,
        "optimal_speed": 89, "wear_rate": 0.85, "repair_cost_base": 1650,
        "pros": ["قدرت و کشش عالی"], "cons": [],
        "suitable_cargo": ["فوق سنگین", "صنعتی"]
    },
    "MAN TGX 580": {
        "brand": "MAN", "power_hp": 580, "usage": "کشنده",
        "load_capacity_tons": 40, "fuel_consumption": 28.5, "tank_volume": 680,
        "optimal_speed": 88, "wear_rate": 0.95, "repair_cost_base": 1500,
        "pros": ["کارآمد"], "cons": [],
        "suitable_cargo": ["صنعتی", "یخچالی"]
    },
    "MAN HX 520": {
        "brand": "MAN", "power_hp": 520, "usage": "نظامی/سنگین",
        "load_capacity_tons": 38, "fuel_consumption": 31.0, "tank_volume": 700,
        "optimal_speed": 80, "wear_rate": 1.0, "repair_cost_base": 1600,
        "pros": ["بسیار مقاوم", "آفرود"], "cons": ["مصرف بالا"],
        "suitable_cargo": ["صنعتی", "فوق سنگین"]
    },
    "MAN TGX 510": {
        "brand": "MAN", "power_hp": 510, "usage": "کشنده",
        "load_capacity_tons": 37, "fuel_consumption": 27.0, "tank_volume": 650,
        "optimal_speed": 87, "wear_rate": 1.05, "repair_cost_base": 1400,
        "pros": [], "cons": [],
        "suitable_cargo": ["یخچالی", "معمولی"]
    },
    "MAN TGS 510": {
        "brand": "MAN", "power_hp": 510, "usage": "ساخت‌وساز",
        "load_capacity_tons": 35, "fuel_consumption": 28.0, "tank_volume": 600,
        "optimal_speed": 83, "wear_rate": 1.15, "repair_cost_base": 1400,
        "pros": ["مناسب کارهای سنگین"], "cons": [],
        "suitable_cargo": ["سنگین", "صنعتی"]
    },
    "MAN TGS 41.480": {
        "brand": "MAN", "power_hp": 480, "usage": "باری/کمپرسی",
        "load_capacity_tons": 33, "fuel_consumption": 27.5, "tank_volume": 550,
        "optimal_speed": 84, "wear_rate": 1.25, "repair_cost_base": 1250,
        "pros": [], "cons": [],
        "suitable_cargo": ["سنگین", "معمولی"]
    },
    "MAN TGX 470": {
        "brand": "MAN", "power_hp": 470, "usage": "کشنده",
        "load_capacity_tons": 33, "fuel_consumption": 26.5, "tank_volume": 580,
        "optimal_speed": 86, "wear_rate": 1.2, "repair_cost_base": 1200,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی"]
    },
    "MAN TGS 430": {
        "brand": "MAN", "power_hp": 430, "usage": "ساخت‌وساز",
        "load_capacity_tons": 30, "fuel_consumption": 27.0, "tank_volume": 480,
        "optimal_speed": 82, "wear_rate": 1.3, "repair_cost_base": 1100,
        "pros": [], "cons": [],
        "suitable_cargo": ["معمولی", "سنگین"]
    },
    "MAN TGM 290": {
        "brand": "MAN", "power_hp": 290, "usage": "توزیع شهری",
        "load_capacity_tons": 20, "fuel_consumption": 24.0, "tank_volume": 250,
        "optimal_speed": 78, "wear_rate": 1.6, "repair_cost_base": 750,
        "pros": ["چابک"], "cons": ["قدرت محدود"],
        "suitable_cargo": ["معمولی", "حساس"]
    },
    "MAN TGL 250": {
        "brand": "MAN", "power_hp": 250, "usage": "سبک",
        "load_capacity_tons": 11, "fuel_consumption": 19.0, "tank_volume": 140,
        "optimal_speed": 75, "wear_rate": 1.8, "repair_cost_base": 550,
        "pros": ["اقتصادی", "مناسب تازه‌کارها"], "cons": ["بسیار محدود"],
        "suitable_cargo": ["معمولی", "حساس"]
    },
} 
