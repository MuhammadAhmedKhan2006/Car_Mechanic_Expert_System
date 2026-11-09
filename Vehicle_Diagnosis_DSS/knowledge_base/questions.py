# -*- coding: utf-8 -*-
# questions.py - the complete question bank (English + Urdu)
#
# Three groups:
#   GENERAL_QUESTIONS : Mode 2 "I don't know what's wrong" - plain-language questions
#   SYMPTOMS          : symptom statements the user confirms in Mode 2 (in symptoms.py)
#   DIRECT_QUESTIONS  : Mode 1 "I have an idea" - questions per selected problem
#   REPORT_QUESTIONS  : one numeric report input per Mode 1 problem
#
# Every question is only shown when it is relevant (see api.py / decision_rules.py).

# ------------------------------------------------------------------
# MODE 2 - GENERAL QUESTIONS (asked one at a time, answers: yes / no / not sure)
# ------------------------------------------------------------------
GENERAL_QUESTIONS = [
    {"id": "g1",  "en": "Does the car start normally every time you turn the key?", "ur": "کیا گاڑی چابی گھمانے پر ہمیشہ نارمل سٹارٹ ہوتی ہے؟"},
    {"id": "g2",  "en": "Does the engine feel rough, shake or stall while driving?", "ur": "کیا انجن چلتے ہوئے کمزور، کانپتا یا بند تو نہیں ہوتا؟"},
    {"id": "g3",  "en": "Are any warning lights showing on the dashboard?", "ur": "کیا ڈیش بورڈ پر کوئی وارننگ لائٹ تو نہیں جل رہی؟"},
    {"id": "g4",  "en": "Does the engine overheat, or do you see steam from under the bonnet?", "ur": "کیا انجن زیادہ گرم ہوتا ہے یا بونٹ سے بھاپ آتی ہے؟"},
    {"id": "g5",  "en": "Do the brakes feel soft, grab suddenly, or pull the car to one side?", "ur": "کیا بریک پیڈل نرم ہے یا گاڑی بریک لگاتے وقت ایک طرف کھنچتی ہے؟"},
    {"id": "g6",  "en": "Do you hear any unusual noises - from the engine, brakes or tyres?", "ur": "کیا انجن، بریک یا ٹائر سے کوئی عجیب آواز آتی ہے؟"},
    {"id": "g7",  "en": "Do you see smoke coming out of the exhaust?", "ur": "کیا ایگزاسٹ سے کوئی دھواں نکلتا ہے؟"},
    {"id": "g8",  "en": "Is the air conditioning blowing warm air or working weakly?", "ur": "کیا اے سی گرم ہوا دے رہا ہے یا کمزور کام کر رہا ہے؟"},
    {"id": "g9",  "en": "Is it hard to change gears, or does the clutch pedal feel wrong?", "ur": "کیا گیئر بدلنا مشکل ہے یا کلچ پیڈل میں خرابی ہے؟"},
    {"id": "g10", "en": "Is the steering wheel heavy, loose, or does it shake at high speed?", "ur": "کیا اسٹیئرنگ بھاری، ڈھیلا ہے یا تیز رفتار پر ہلتا ہے؟"},
    {"id": "g11", "en": "Do the tyres look worn out, flat, or do they vibrate while driving?", "ur": "کیا ٹائر گھسے ہوئے، پچکے ہیں یا چلتے ہوئے کانپتے ہیں؟"},
    {"id": "g12", "en": "Have you noticed slower acceleration or higher fuel consumption recently?", "ur": "کیا حال ہی میں رفتار کم یا فیول زیادہ خرچ ہو رہا ہے؟"},
]

# ------------------------------------------------------------------
# MODE 1 - DIRECT QUESTIONS (5 Yes/No questions per problem card)
# Problem keys match vehicle_problems.py
# ------------------------------------------------------------------
DIRECT_QUESTIONS = {
    "start": [
        {"id": "st_q1", "en": "When you turn the key, do the dashboard lights stay completely off?", "ur": "چابی گھمانے پر کیا ڈیش بورڈ کی لائٹس بالکل بند رہتی ہیں؟"},
        {"id": "st_q2", "en": "Do you hear a rapid clicking sound when you try to start the car?", "ur": "کیا اسٹارٹ کرنے پر تیز ٹک ٹک کی آواز آتی ہے؟"},
        {"id": "st_q3", "en": "Does the engine crank (turn over) but still not start?", "ur": "کیا انجن گھومتا ہے مگر پھر بھی اسٹارٹ نہیں ہوتا؟"},
        {"id": "st_q4", "en": "Is the fuel gauge showing empty or very low?", "ur": "کیا فیول گیج خالی یا بہت کم دکھا رہا ہے؟"},
        {"id": "st_q5", "en": "Do you smell petrol, or see smoke coming from the engine area?", "ur": "کیا انجن کے حصے سے پیٹرول کی بو یا دھواں آ رہا ہے؟"},
    ],
    "overheat": [
        {"id": "ov_q1", "en": "Is the temperature warning light on, or is the gauge in the red zone?", "ur": "کیا درجہ حرارت کی وارننگ لائٹ جل رہی ہے یا گیج سرخ زون میں ہے؟"},
        {"id": "ov_q2", "en": "Is steam or smoke coming out from under the bonnet?", "ur": "کیا بونٹ سے بھاپ یا دھواں نکل رہا ہے؟"},
        {"id": "ov_q3", "en": "Is the coolant level low, or do you have to top it up often?", "ur": "کیا کولنٹ کی سطح کم ہے یا اکثر بھرنی پڑتی ہے؟"},
        {"id": "ov_q4", "en": "Is the radiator fan not spinning, or is the AC not working?", "ur": "کیا ریڈی ایٹر کا پنکھا نہیں گھومتا یا اے سی کام نہیں کر رہا؟"},
        {"id": "ov_q5", "en": "Do you see coolant puddles under the car, or smell something sweet?", "ur": "کیا گاڑی کے نیچے کولنٹ کے دھبے ہیں یا میٹھی بو آ رہی ہے؟"},
    ],
    "brake": [
        {"id": "br_q1", "en": "Does the brake pedal feel very soft, or sink to the floor?", "ur": "کیا بریک پیڈل بہت نرم ہے یا فرش تک جاتا ہے؟"},
        {"id": "br_q2", "en": "Do you hear grinding or loud squealing when you brake?", "ur": "کیا بریک لگاتے وقت رگڑ یا اونچی چیخ کی آواز آتی ہے؟"},
        {"id": "br_q3", "en": "Does the car pull to one side when you brake?", "ur": "کیا بریک لگانے پر گاڑی ایک طرف کھنچتی ہے؟"},
        {"id": "br_q4", "en": "Is the brake warning light on the dashboard?", "ur": "کیا ڈیش بورڈ پر بریک کی وارننگ لائٹ جل رہی ہے؟"},
        {"id": "br_q5", "en": "Does the steering wheel or brake pedal shake when you brake?", "ur": "کیا بریک لگانے پر اسٹیئرنگ یا بریک پیڈل کانپتا ہے؟"},
    ],
    "noise": [
        {"id": "nv_q1", "en": "Do you hear a knocking or tapping sound from the engine?", "ur": "کیا انجن سے کھٹکھٹانے یا ٹپکنے کی آواز آتی ہے؟"},
        {"id": "nv_q2", "en": "Do you hear a squealing sound when starting the car or turning the steering wheel?", "ur": "کیا گاڑی سٹارٹ کرتے یا اسٹیئرنگ گھماتے وقت چیخ کی آواز آتی ہے؟"},
        {"id": "nv_q3", "en": "Is there a humming or rumbling noise that gets louder as speed increases?", "ur": "کیا رفتار بڑھنے کے ساتھ گونجنے والی آواز تیز ہوتی ہے؟"},
        {"id": "nv_q4", "en": "Do you hear a clunk when driving over bumps?", "ur": "کیا اونچی نیچی سڑک پر ٹھک ٹھک کی آواز آتی ہے؟"},
        {"id": "nv_q5", "en": "Does the steering wheel or seat vibrate at higher speeds?", "ur": "کیا تیز رفتار پر اسٹیئرنگ یا سیٹ کانپتا ہے؟"},
    ],
    "electrical": [
        {"id": "el_q1", "en": "Is the battery more than 3 years old?", "ur": "کیا بیٹری تین سال سے پرانی ہے؟"},
        {"id": "el_q2", "en": "Are the headlights dim or flickering?", "ur": "کیا ہیڈ لائٹس مدھم یا جھلملا رہی ہیں؟"},
        {"id": "el_q3", "en": "Is the battery warning light on the dashboard?", "ur": "کیا ڈیش بورڈ پر بیٹری کی وارننگ لائٹ جل رہی ہے؟"},
        {"id": "el_q4", "en": "Do the power windows, wipers or radio work slowly or stop at random?", "ur": "کیا پاور ونڈوز، وپرز یا ریڈیو سست یا اچانک بند ہوتے ہیں؟"},
        {"id": "el_q5", "en": "Do you smell burning plastic, or see smoke from the wiring or fuse box?", "ur": "کیا پلاسٹک جلنے کی بو آتی ہے یا وائرنگ / فیوز باکس سے دھواں آتا ہے؟"},
    ],
    "tyre": [
        {"id": "ty_q1", "en": "Does a tyre look flat or low on air?", "ur": "کیا کوئی ٹائر پچکا ہوا یا ہوا کم نظر آتا ہے؟"},
        {"id": "ty_q2", "en": "Is there a bulge or a deep cut on the side of a tyre?", "ur": "کیا ٹائر کے پہلو میں ابھار یا گہرا کٹ ہے؟"},
        {"id": "ty_q3", "en": "Does the car pull to one side while driving straight?", "ur": "کیا سیدھی سڑک پر گاڑی ایک طرف کھنچتی ہے؟"},
        {"id": "ty_q4", "en": "Is the tyre tread worn out or uneven?", "ur": "کیا ٹائر کی گراری گھسی ہوئی یا ناہموار ہے؟"},
        {"id": "ty_q5", "en": "Does the steering wheel shake at higher speeds?", "ur": "کیا تیز رفتار پر اسٹیئرنگ کانپتا ہے؟"},
    ],
    "oil": [
        {"id": "ol_q1", "en": "Is the oil pressure or oil warning light on?", "ur": "کیا آئل پریشر یا آئل وارننگ لائٹ جل رہی ہے؟"},
        {"id": "ol_q2", "en": "Is blue or grey smoke coming from the exhaust?", "ur": "کیا ایگزاسٹ سے نیلا یا خاکستری دھواں آتا ہے؟"},
        {"id": "ol_q3", "en": "Is black smoke coming from the exhaust?", "ur": "کیا ایگزاسٹ سے کالا دھواں آتا ہے؟"},
        {"id": "ol_q4", "en": "Do you see oil spots or puddles under the car?", "ur": "کیا گاڑی کے نیچے آئل کے دھبے ہیں؟"},
        {"id": "ol_q5", "en": "Do you smell burning oil?", "ur": "کیا جلتے ہوئے آئل کی بو آتی ہے؟"},
    ],
    "ac": [
        {"id": "ac_q1", "en": "Is the AC blowing warm or only slightly cool air?", "ur": "کیا اے سی گرم یا ہلکی ٹھنڈی ہوا دے رہا ہے؟"},
        {"id": "ac_q2", "en": "Is the airflow weak even at the highest fan speed?", "ur": "کیا سب سے تیز پنکھے پر بھی ہوا کم آتی ہے؟"},
        {"id": "ac_q3", "en": "Is there a musty or bad smell from the vents?", "ur": "کیا وینٹس سے نمی یا بری بو آتی ہے؟"},
        {"id": "ac_q4", "en": "Do you hear a loud noise or clicking when the AC is on?", "ur": "کیا اے سی چلانے پر اونچی آواز یا کلک آتی ہے؟"},
        {"id": "ac_q5", "en": "Is water leaking inside the car (wet carpet)?", "ur": "کیا گاڑی کے اندر پانی لیک ہو رہا ہے (گیلا قالین)؟"},
    ],
    "steering": [
        {"id": "sr_q1", "en": "Did the steering suddenly lock, or become impossible to control?", "ur": "کیا اسٹیئرنگ اچانک جام گیا یا قابو سے باہر ہو گیا؟"},
        {"id": "sr_q2", "en": "Is the steering wheel very heavy or hard to turn?", "ur": "کیا اسٹیئرنگ بہت بھاری یا گھمانا مشکل ہے؟"},
        {"id": "sr_q3", "en": "Does the car drift to one side on a straight road?", "ur": "کیا سیدھی سڑک پر گاڑی ایک طرف کھسکتی ہے؟"},
        {"id": "sr_q4", "en": "Is there extra play (looseness) in the steering wheel?", "ur": "کیا اسٹیئرنگ میں اضافی ڈھیلا پن (لوفٹ) ہے؟"},
        {"id": "sr_q5", "en": "Do you hear a whining sound when turning the steering wheel?", "ur": "کیا اسٹیئرنگ گھماتے وقت سیٹی جیسی آواز آتی ہے؟"},
    ],
    "gear": [
        {"id": "gc_q1", "en": "Does the gear slip or pop out by itself?", "ur": "کیا گیئر پھسلتا ہے یا خود نکل جاتا ہے؟"},
        {"id": "gc_q2", "en": "Is it hard to shift gears, or do you hear grinding while shifting?", "ur": "کیا گیئر بدلنا مشکل ہے یا رگڑ کی آواز آتی ہے؟"},
        {"id": "gc_q3", "en": "Does the clutch pedal feel soft, stuck or too high?", "ur": "کیا کلچ پیڈل نرم، پھنسا ہوا یا بہت اونچا ہے؟"},
        {"id": "gc_q4", "en": "Do you smell burning when driving uphill or in traffic?", "ur": "کیا اوپر چڑھتے یا ٹریفک میں جلنے کی بو آتی ہے؟"},
        {"id": "gc_q5", "en": "Does the engine rev high but the car does not speed up?", "ur": "کیا انجن تیز چلتا ہے مگر گاڑی رفتار نہیں پکڑتی؟"},
    ],
    "engine": [
        {"id": "en_q1", "en": "Does the engine rev high but the car does not speed up?", "ur": "کیا انجن تیز چلتا ہے مگر گاڑی رفتار نہیں پکڑتی؟"},
        {"id": "en_q2", "en": "Is the engine temperature rising when the AC is on?", "ur": "کیا اے سی چلانے پر انجن کا درجہ حرارت بڑھتا ہے؟"},
        {"id": "en_q3", "en": "Was the oil last changed more than 6 months or 5000 km ago?", "ur": "کیا آئل چھ ماہ یا 5000 کلومیٹر سے زیادہ پہلے بدلا گیا تھا؟"},
        {"id": "en_q4", "en": "Do you smell burning when driving uphill or in traffic?", "ur": "کیا اوپر چڑھتے یا ٹریفک میں جلنے کی بو آتی ہے؟"},
        {"id": "en_q5", "en": "Does the engine run rough, lose power, or stall?", "ur": "کیا انجن کھردرا چلتا ہے، طاقت کم ہوتی ہے یا بند ہو جاتا ہے؟"},
    ],
    "exhaust": [
        {"id": "ex_q1", "en": "Is blue or grey smoke coming from the exhaust?", "ur": "کیا ایگزاسٹ سے نیلا یا خاکستری دھواں آتا ہے؟"},
        {"id": "ex_q2", "en": "Is black smoke coming from the exhaust?", "ur": "کیا ایگزاسٹ سے کالا دھواں آتا ہے؟"},
        {"id": "ex_q3", "en": "Do you see oil spots or puddles under the car?", "ur": "کیا گاڑی کے نیچے آئل کے دھبے ہیں؟"},
        {"id": "ex_q4", "en": "Do you smell burning oil or petrol?", "ur": "کیا جلتے آئل یا پیٹرول کی بو آتی ہے؟"},
        {"id": "ex_q5", "en": "Has the car failed an emissions / pollution check recently?", "ur": "کیا گاڑی حال ہی میں اخراجات / آلودگی ٹیسٹ میں فیل ہوئی ہے؟"},
    ],
}

# ------------------------------------------------------------------
# MODE 1 - REPORT (numeric) INPUTS, one per problem card
# ------------------------------------------------------------------
REPORT_QUESTIONS = {
    "start":     {"id": "rp_start", "kind": "number", "en": "Battery voltage from a multimeter (normal 12.4 - 12.8 V)", "ur": "ملٹی میٹر سے بیٹری وولٹیج (نارمل 12.4 تا 12.8 وولٹ)", "min": 0.0, "max": 20.0, "step": 0.1, "fmt": "%.1f", "unit": "V"},
    "overheat":  {"id": "rp_ov",    "kind": "number", "en": "Engine temperature from the dashboard gauge (normal 85 - 105 °C)", "ur": "ڈیش بورڈ گیج سے انجن کا درجہ حرارت (نارمل 85 تا 105 ڈگری)", "min": 0.0, "max": 150.0, "step": 1.0, "fmt": "%.0f", "unit": "°C"},
    "brake":     {"id": "rp_br",    "kind": "number", "en": "Kilometres since the last brake service", "ur": "آخری بریک سروس کے بعد کے کلومیٹر", "min": 0.0, "max": 200000.0, "step": 500.0, "fmt": "%.0f", "unit": "km"},
    "noise":     {"id": "rp_nv",    "kind": "number", "en": "Oil level from the dipstick as a percentage (normal 60 - 100 %)", "ur": "ڈپ اسٹک سے آئل کی سطح فیصد میں (نارمل 60 تا 100 فیصد)", "min": 0.0, "max": 100.0, "step": 5.0, "fmt": "%.0f", "unit": "%"},
    "electrical":{"id": "rp_el",   "kind": "number", "en": "Battery voltage (normal 12.4 - 12.8 V)", "ur": "بیٹری وولٹیج (نارمل 12.4 تا 12.8 وولٹ)", "min": 0.0, "max": 20.0, "step": 0.1, "fmt": "%.1f", "unit": "V"},
    "tyre":      {"id": "rp_ty",    "kind": "number", "en": "Tyre pressure from a gauge (normal 30 - 35 PSI)", "ur": "گیج سے ٹائر کا پریشر (نارمل 30 تا 35 پی ایس آئی)", "min": 0.0, "max": 60.0, "step": 0.5, "fmt": "%.1f", "unit": "PSI"},
    "oil":       {"id": "rp_ol",    "kind": "number", "en": "Oil level percentage (normal 60 - 100 %)", "ur": "آئل کی سطح فیصد (نارمل 60 تا 100 فیصد)", "min": 0.0, "max": 100.0, "step": 5.0, "fmt": "%.0f", "unit": "%"},
    "ac":        {"id": "rp_ac",    "kind": "number", "en": "Kilometres since the AC was last serviced", "ur": "اے سی کی آخری سروس کے بعد کے کلومیٹر", "min": 0.0, "max": 200000.0, "step": 500.0, "fmt": "%.0f", "unit": "km"},
    "steering":  {"id": "rp_sr",    "kind": "number", "en": "Tyre pressure (normal 30 - 35 PSI)", "ur": "ٹائر کا پریشر (نارمل 30 تا 35 پی ایس آئی)", "min": 0.0, "max": 60.0, "step": 0.5, "fmt": "%.1f", "unit": "PSI"},
    "gear":      {"id": "rp_gc",    "kind": "number", "en": "Kilometres since the last transmission service", "ur": "آخری ٹرانسمیشن سروس کے بعد کے کلومیٹر", "min": 0.0, "max": 200000.0, "step": 500.0, "fmt": "%.0f", "unit": "km"},
    "engine":    {"id": "rp_en",    "kind": "number", "en": "Kilometres since the last oil change (normal below 5000 km)", "ur": "آخری آئل چینج کے بعد کے کلومیٹر (نارمل 5000 کلومیٹر سے کم)", "min": 0.0, "max": 200000.0, "step": 500.0, "fmt": "%.0f", "unit": "km"},
    "exhaust":   {"id": "rp_ex",    "kind": "number", "en": "Kilometres since the last service", "ur": "آخری سروس کے بعد کے کلومیٹر", "min": 0.0, "max": 200000.0, "step": 500.0, "fmt": "%.0f", "unit": "km"},
}
