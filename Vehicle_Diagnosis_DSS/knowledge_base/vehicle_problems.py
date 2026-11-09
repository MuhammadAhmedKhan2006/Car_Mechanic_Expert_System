# -*- coding: utf-8 -*-
# vehicle_problems.py - the list of possible vehicle problems (English + Urdu)
#
# Each problem has:
#   en / ur      : name shown to the user
#   simple_en/ur : plain-language explanation (no technical jargon)
#   critical     : True = safety critical (stop the car if severe)

PROBLEMS = {
    "battery": {
        "en": "Battery problem", "ur": "بیٹری کی خرابی",
        "simple_en": "The battery is weak or old, so it cannot supply enough power to start the car or run the electrics.",
        "simple_ur": "بیٹری کمزور یا پرانی ہے اس لیے گاڑی سٹارٹ کرنے یا بجلی چلانے کے لیے کافی طاقت نہیں دے سکتی۔",
        "critical": False,
    },
    "starter": {
        "en": "Starter motor problem", "ur": "اسٹارٹر موٹر کی خرابی",
        "simple_en": "The starter motor that turns the engine is faulty, so the engine does not crank.",
        "simple_ur": "انجن گھمانے والی اسٹارٹر موٹر خراب ہے اس لیے انجن نہیں گھومتا۔",
        "critical": False,
    },
    "fuel": {
        "en": "Fuel system problem", "ur": "فیول سسٹم کی خرابی",
        "simple_en": "Fuel is not reaching the engine properly - empty tank, pump or filter problem.",
        "simple_ur": "فیول انجن تک صحیح نہیں پہنچ رہا - ٹینک خالی، پمپ یا فلٹر کی خرابی۔",
        "critical": False,
    },
    "engine_perf": {
        "en": "Engine performance problem", "ur": "انجن کی کارکردگی کی خرابی",
        "simple_en": "The engine runs poorly - loses power, runs rough or uses more fuel than normal.",
        "simple_ur": "انجن خراب چلتا ہے - طاقت کم ہوتی ہے، کھردرا چلتا ہے یا فیول زیادہ لگتا ہے۔",
        "critical": False,
    },
    "overheating": {
        "en": "Engine overheating", "ur": "انجن کا زیادہ گرم ہونا",
        "simple_en": "The cooling system is not removing heat - low coolant, leaks or a fan problem.",
        "simple_ur": "کولنگ سسٹم حرارت نہیں نکال رہا - کولنٹ کم، لیک یا پنکھے کی خرابی۔",
        "critical": True,
    },
    "braking": {
        "en": "Brake problem", "ur": "بریک کی خرابی",
        "simple_en": "The brakes are worn or the fluid is low, so stopping is unsafe.",
        "simple_ur": "بریک گھسے ہوئے ہیں یا فلوئڈ کم ہے، اس لیے روکنا غیر محفوظ ہے۔",
        "critical": True,
    },
    "noise_vibration": {
        "en": "Unusual noise or vibration", "ur": "عجیب آواز یا جھٹکے",
        "simple_en": "Something is loose or worn - belts, suspension or wheel parts making noise or vibration.",
        "simple_ur": "کوئی حصہ ڈھیلا یا گھسا ہوا ہے - بیلٹ، سسپنشن یا وہیل پارٹس آواز یا کانپنے کا سبب بن رہے ہیں۔",
        "critical": False,
    },
    "electrical": {
        "en": "Electrical fault", "ur": "بجلی کے نظام کی خرابی",
        "simple_en": "A wiring, fuse or charging problem is affecting lights, windows or other electrics.",
        "simple_ur": "وائرنگ، فیوز یا چارجنگ کی خرابی لائٹس، ونڈوز یا دیگر بجلی کے پرزوں کو متاثر کر رہی ہے۔",
        "critical": False,
    },
    "tyres": {
        "en": "Tyre / wheel problem", "ur": "ٹائر / پہیے کی خرابی",
        "simple_en": "A tyre is flat, worn, damaged or out of balance, causing pulls or vibration.",
        "simple_ur": "کوئی ٹائر پچا ہوا، گھسا ہوا، خراب یا غیر متوازن ہے جس سے گاڑی کھنچتی یا کانپتی ہے۔",
        "critical": False,
    },
    "steering": {
        "en": "Steering problem", "ur": "اسٹیئرنگ کی خرابی",
        "simple_en": "The steering is heavy, loose or drifting - fluid, alignment or tyre related.",
        "simple_ur": "اسٹیئرنگ بھاری، ڈھیلا یا کھسکتا ہے - فلوئڈ، الائنمنٹ یا ٹائر سے متعلق۔",
        "critical": False,
    },
    "transmission": {
        "en": "Transmission / clutch problem", "ur": "گیئر باکس / کلچ کی خرابی",
        "simple_en": "Gears slip, grind or the clutch is worn, so power is not delivered smoothly.",
        "simple_ur": "گیئر پھسلتے یا رگڑتے ہیں یا کلچ گھسا ہوا ہے، اس لیے طاقت ہموار نہیں پہنچتی۔",
        "critical": False,
    },
    "ac": {
        "en": "Air conditioning problem", "ur": "اے سی کی خرابی",
        "simple_en": "The AC is not cooling - low gas, blocked filter or a compressor problem.",
        "simple_ur": "اے سی ٹھنڈا نہیں کر رہا - گیس کم، فلٹر بند یا کمپریسر کی خرابی۔",
        "critical": False,
    },
    "exhaust": {
        "en": "Exhaust / smoke problem", "ur": "ایگزاسٹ / دھوئیں کی خرابی",
        "simple_en": "The exhaust emits smoke - oil burning, fuel mixture or a leak problem.",
        "simple_ur": "ایگزاسٹ سے دھواں نکلتا ہے - آئل جلنا، فیول مکسچر یا لیک کی خرابی۔",
        "critical": False,
    },
    "oil_leak": {
        "en": "Oil leak", "ur": "آئل لیک",
        "simple_en": "Engine oil is leaking - low oil damages the engine if ignored.",
        "simple_ur": "انجن آئل لیک ہو رہا ہے - نظرانداز کرنے سے آئل کم ہو کر انجن خراب ہو سکتا ہے۔",
        "critical": False,
    },
}

# Which problems each Mode-1 card can point to (used for alternatives)
CARD_PROBLEMS = {
    "start":      ["battery", "starter", "fuel"],
    "overheat":   ["overheating", "electrical"],
    "brake":      ["braking"],
    "noise":      ["noise_vibration", "engine_perf", "tyres"],
    "electrical": ["electrical", "battery"],
    "tyre":       ["tyres", "steering"],
    "oil":        ["oil_leak", "exhaust", "engine_perf"],
    "ac":         ["ac"],
    "steering":   ["steering", "tyres"],
    "gear":       ["transmission"],
    "engine":     ["engine_perf", "overheating", "transmission"],
    "exhaust":    ["exhaust", "oil_leak", "fuel", "engine_perf"],
}

# Card titles shown on the Mode-1 selection screen (no technical jargon needed)
CARDS = {
    "start":      {"en": "Engine won't start", "ur": "انجن سٹارٹ نہیں ہوتا", "icon": "key"},
    "overheat":   {"en": "Overheating / steam", "ur": "زیادہ گرمی / بھاپ", "icon": "thermo"},
    "brake":      {"en": "Brake problem", "ur": "بریک کا مسئلہ", "icon": "brake"},
    "noise":      {"en": "Strange noise / vibration", "ur": "عجیب آواز / جھٹکے", "icon": "sound"},
    "electrical": {"en": "Battery / lights / electrics", "ur": "بیٹری / لائٹس / بجلی", "icon": "bolt"},
    "tyre":       {"en": "Tyre problem", "ur": "ٹائر کا مسئلہ", "icon": "wheel"},
    "oil":        {"en": "Oil leak / smoke", "ur": "آئل لیک / دھواں", "icon": "drop"},
    "ac":         {"en": "AC not cooling", "ur": "اے سی ٹھنڈا نہیں کرتا", "icon": "snow"},
    "steering":   {"en": "Steering problem", "ur": "اسٹیئرنگ کا مسئلہ", "icon": "steer"},
    "gear":       {"en": "Gear / clutch problem", "ur": "گیئر / کلچ کا مسئلہ", "icon": "gear"},
    "engine":     {"en": "Poor performance / fuel use", "ur": "کمزور کارکردگی / زیادہ فیول", "icon": "engine"},
    "exhaust":    {"en": "Smoke from exhaust", "ur": "ایگزاسٹ سے دھواں", "icon": "exhaust"},
}
