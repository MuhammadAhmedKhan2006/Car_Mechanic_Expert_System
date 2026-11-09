# -*- coding: utf-8 -*-
# symptoms.py - symptom statements used in Mode 2 ("I don't know what's wrong")
#
# Each symptom has a unique id, English/Urdu text, and a list of
# (problem_id, points) showing which problems it supports.
# The user confirms or rejects each symptom with Yes / No / Not Sure.

SYMPTOMS = [
    {"id": "sym_dim_lights",  "en": "Headlights or dashboard lights look dim, especially at idle.", "ur": "ہیڈ لائٹس یا ڈیش بورڈ مدھم نظر آتے ہیں، خاص طور پر کار کھڑی حالت میں۔",
     "fx": [("battery", 3), ("electrical", 2)]},
    {"id": "sym_slow_crank",  "en": "The engine cranks slowly or makes a clicking sound when starting.", "ur": "سٹارٹ کرتے وقت انجن آہستہ گھومتا ہے یا کلک کی آواز آتی ہے۔",
     "fx": [("battery", 3), ("starter", 3)]},
    {"id": "sym_no_crank",    "en": "Nothing happens at all when you turn the key.", "ur": "چابی گھمانے پر بالکل کچھ نہیں ہوتا۔",
     "fx": [("battery", 3), ("starter", 3)]},
    {"id": "sym_stall",       "en": "The car stalls, hesitates or loses power when accelerating.", "ur": "گاڑی تیز چلانے پر بند ہو جاتی ہے، ہچکچاتی ہے یا طاقت کم ہوتی ہے۔",
     "fx": [("fuel", 3), ("engine_perf", 2), ("transmission", 1)]},
    {"id": "sym_overheat",    "en": "The temperature gauge goes into the red, or steam appears from under the bonnet.", "ur": "ٹیمپریچر گیج سرخ زون میں جاتا ہے یا بونٹ سے بھاپ آتی ہے۔",
     "fx": [("overheating", 4)]},
    {"id": "sym_brake_soft",  "en": "The brake pedal feels soft, sinks down, or needs pumping.", "ur": "بریک پیڈل نرم ہے، نیچے جاتا ہے یا بار بار دبانا پڑتا ہے۔",
     "fx": [("braking", 4)]},
    {"id": "sym_brake_noise", "en": "You hear squealing or grinding when you brake.", "ur": "بریک لگاتے وقت چیخ یا رگڑ کی آواز آتی ہے۔",
     "fx": [("braking", 3), ("noise_vibration", 1)]},
    {"id": "sym_pull_brake",  "en": "The car pulls to one side when you brake.", "ur": "بریک لگانے پر گاڑی ایک طرف کھنچتی ہے۔",
     "fx": [("braking", 3), ("tyres", 1)]},
    {"id": "sym_engine_knock","en": "There is knocking, ticking or rumbling from the engine.", "ur": "انجن سے کھٹکھٹاہٹ، ٹک ٹک یا گرج سنائی دیتی ہے۔",
     "fx": [("engine_perf", 3), ("noise_vibration", 2)]},
    {"id": "sym_smoke_blue",  "en": "Blue or grey smoke comes from the exhaust.", "ur": "ایگزاسٹ سے نیلا یا خاکستری دھواں آتا ہے۔",
     "fx": [("oil_leak", 3), ("engine_perf", 2), ("exhaust", 1)]},
    {"id": "sym_smoke_black", "en": "Black smoke comes from the exhaust, especially under acceleration.", "ur": "تیز چلانے پر ایگزاسٹ سے کالا دھواں آتا ہے۔",
     "fx": [("fuel", 3), ("engine_perf", 2), ("exhaust", 1)]},
    {"id": "sym_ac_warm",     "en": "The AC blows warm air or the airflow is weak.", "ur": "اے سی گرم ہوا دیتا ہے یا ہوا کی رفتار کم ہے۔",
     "fx": [("ac", 4)]},
    {"id": "sym_gear_hard",   "en": "Changing gears is difficult, or you hear grinding while shifting.", "ur": "گیئر بدلنا مشکل ہے یا بدلتے وقت رگڑ کی آواز آتی ہے۔",
     "fx": [("transmission", 4)]},
    {"id": "sym_steer_shake", "en": "The steering wheel shakes at higher speeds.", "ur": "تیز رفتار پر اسٹیئرنگ کانپتا ہے۔",
     "fx": [("tyres", 3), ("steering", 2)]},
    {"id": "sym_tyre_worn",   "en": "Tyres look worn, flat, or the car pulls to one side while driving straight.", "ur": "ٹائر گھسے ہوئے یا پچکے ہیں، یا سیدھی سڑک پر گاڑی ایک طرف کھنچتی ہے۔",
     "fx": [("tyres", 4), ("steering", 1)]},
    {"id": "sym_oil_spot",    "en": "You see oil spots or puddles under the car.", "ur": "گاڑی کے نیچے آئل کے دھبے ہیں۔",
     "fx": [("oil_leak", 4)]},
]
