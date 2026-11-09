# -*- coding: utf-8 -*-
# recommendations.py - repair / maintenance recommendations per problem
#
# Each recommendation: en/ur action text, why_en/why_ur explanation,
# and a priority hint (low / medium / high / urgent).

RECOMMENDATIONS = {
    "battery": [
        {"en": "Get the battery tested and replaced if it is older than 3 years.", "ur": "بیٹری کی جانچ کروائیں اور اگر وہ تین سال سے پرانی ہے تو بدلوانے لیں۔",
         "why_en": "Weak batteries cause slow cranking, dim lights and no-start situations.", "why_ur": "کمزور بیٹری آہستہ سٹارٹر، مدھم لائٹس اور سٹارٹ نہ ہونے کا سبب بنتی ہے۔", "prio": "medium"},
        {"en": "Clean the battery terminals and check the charging system.", "ur": "بیٹری ٹرمینلز صاف کریں اور چارجنگ سسٹم چیک کروائیں۔",
         "why_en": "Corroded terminals or a faulty alternator keep the battery from charging.", "why_ur": "زنگ آلود ٹرمینلز یا خراب الٹرنیٹر بیٹری کو چارج نہیں ہونے دیتے۔", "prio": "low"},
    ],
    "starter": [
        {"en": "Have the starter motor and solenoid checked by a mechanic.", "ur": "اسٹارٹر موٹر اور سولیئنڈ کی میکینک سے جانچ کروائیں۔",
         "why_en": "A faulty starter is the most common cause of a no-crank condition.", "why_ur": "خراب اسٹارٹر 'کوئی گھماؤ نہیں' کی سب سے عام وجہ ہے۔", "prio": "medium"},
    ],
    "fuel": [
        {"en": "Check the fuel level first - refilling may solve the problem.", "ur": "پہلے فیول کی سطح چیک کریں - ٹینک بھرنے سے مسئلہ حل ہو سکتا ہے۔",
         "why_en": "An empty or nearly empty tank is the simplest cause of starting and stalling problems.", "why_ur": "خالی یا تقریباً خالی ٹینک سٹارٹنگ اور стоп ہونے کی آسان ترین وجہ ہے۔", "prio": "low"},
        {"en": "Ask a mechanic to check the fuel pump and fuel filter.", "ur": "میکینک سے فیول پمپ اور فیول فلٹر چیک کروائیں۔",
         "why_en": "A weak pump or clogged filter starves the engine of fuel.", "why_ur": "کمزور پمپ یا بند فلٹر انجن کو فیول نہیں پہنچنے دیتا۔", "prio": "medium"},
    ],
    "engine_perf": [
        {"en": "Change the engine oil and air filter if they are overdue.", "ur": "اگر آئل اور ایئر فلٹر بدلنے کا وقت گزر گیا ہے تو تبدیل کروائیں۔",
         "why_en": "Old oil and a dirty filter make the engine run rough and lose power.", "why_ur": "پرانا آئل اور گندا فلٹر انجن کو کھردرا اور بے طاقت بناتے ہیں۔", "prio": "medium"},
        {"en": "Have the spark plugs and ignition system checked.", "ur": "اسپارک پلگ اور اگنیشن سسٹم چیک کروائیں۔",
         "why_en": "Worn plugs cause misfires, hesitation and poor acceleration.", "why_ur": "گھسے پلگ مس فائر، ہچکچاہٹ اور کمزور تیز رفتاری کا سبب بنتے ہیں۔", "prio": "medium"},
    ],
    "overheating": [
        {"en": "Stop the car immediately if steam appears or the gauge is in the red.", "ur": "اگر بھاپ آئے یا گیج سرخ زون میں جائے تو گاڑی فوراً روکیں۔",
         "why_en": "Driving while overheating can warp the engine and cause expensive damage.", "why_ur": "گرمی میں گاڑی چلانا انجن کو بگاڑ سکتا ہے اور مہنگی مرمت کا سبب بن سکتا ہے۔", "prio": "urgent"},
        {"en": "Check coolant level and look for leaks once the engine is cool.", "ur": "انجن ٹھنڈا ہونے کے بعد کولنٹ کی سطح چیک کریں اور لیک تلاش کریں۔",
         "why_en": "Low coolant or a leak is the most common cause of overheating.", "why_ur": "کم کولنٹ یا لیک زیادہ گرمی کی سب سے عام وجہ ہے۔", "prio": "high"},
        {"en": "Have the radiator fan and thermostat checked.", "ur": "ریڈی ایٹر پنکھا اور تھرموسٹیٹ چیک کروائیں۔",
         "why_en": "A dead fan or stuck thermostat stops heat from escaping.", "why_ur": "بند پنکھا یا پھسا تھرموسٹیٹ حرارت کو باہر نہیں جانے دیتا۔", "prio": "high"},
    ],
    "braking": [
        {"en": "Do not drive if the brake pedal feels soft or sinks - call a tow truck.", "ur": "اگر بریک پیڈل نرم یا نیچے جاتا ہے تو گاڑی نہ چلائیں - ٹو ٹرک بلائیں۔",
         "why_en": "Soft or sinking brakes can fail completely - this is a safety emergency.", "why_ur": "نرم یا گرتے ہوئے بریک مکمل ناکام ہو سکتے ہیں - یہ حفاظتی ایمرجنسی ہے۔", "prio": "urgent"},
        {"en": "Have brake pads, discs and brake fluid inspected.", "ur": "بریک پیڈز، ڈسک اور بریک فلوئڈ کی جانچ کروائیں۔",
         "why_en": "Worn pads and low fluid reduce braking power and damage discs.", "why_ur": "گھسے پیڈز اور کم فلوئڈ بریکنگ طاقت کم کرتے ہیں اور ڈسک خراب کرتے ہیں۔", "prio": "high"},
    ],
    "noise_vibration": [
        {"en": "Note when the noise happens (speed, bumps, cold start) and tell the mechanic.", "ur": "دیکھیں آواز کب آتی ہے (رفتار، کچے، سرد سٹارٹ) اور میکینک کو بتائیں۔",
         "why_en": "The timing of the noise helps the mechanic find the exact worn part.", "why_ur": "آواز کا وقت میکینک کو درست گھسے ہوئے پرزے تک پہنچنے میں مدد دیتا ہے۔", "prio": "low"},
        {"en": "Have belts, suspension and wheel bearings checked.", "ur": "بیلٹ، سسپنشن اور وہیل بیئرنگ چیک کروائیں۔",
         "why_en": "Loose belts and worn suspension parts are the usual sources of noise and vibration.", "why_ur": "ڈھیلے بیلٹ اور گھسے سسپنشن پارٹس آواز اور کانپنے کے عام ذرائع ہیں۔", "prio": "medium"},
    ],
    "electrical": [
        {"en": "Check fuses and the battery terminals first - they are the easiest fixes.", "ur": "پہلے فیوز اور بیٹری ٹرمینلز چیک کریں - یہ آسان ترین حل ہیں۔",
         "why_en": "A blown fuse or loose terminal causes most electrical symptoms.", "why_ur": "پھٹا فیوز یا ڈھیلا ٹرمینل زیادہ تر بجلی کے علامات کا سبب بنتا ہے۔", "prio": "low"},
        {"en": "Have the alternator and wiring harness checked.", "ur": "الٹرنیٹر اور وائرنگ ہارنس چیک کروائیں۔",
         "why_en": "A failing alternator causes dim lights, slow electrics and a dead battery.", "why_ur": "خراب آلٹرنیٹر مدھم لائٹس، سست بجلی کے پرزے اور بیٹری ختم ہونے کا سبب بنتا ہے۔", "prio": "medium"},
    ],
    "tyres": [
        {"en": "Check tyre pressure and tread depth on all four tyres.", "ur": "چاروں ٹائروں کا پریشر اور گراری چیک کریں۔",
         "why_en": "Low pressure or worn tread causes pulls, vibration and blowouts.", "why_ur": "کم پریشر یا گھسی گراری کھنچاؤ، کانپنا اور بلاسٹ آؤٹ کا سبب بنتے ہیں۔", "prio": "medium"},
        {"en": "If a tyre has a bulge or deep cut, replace it before driving fast.", "ur": "اگر ٹائر میں ابھار یا گہرا کٹ ہے تو تیز چلانے سے پہلے بدلوانے لیں۔",
         "why_en": "A damaged sidewall can burst suddenly at speed.", "why_ur": "خراب پہلو تیز رفتار پر اچانک پھٹ سکتا ہے۔", "prio": "urgent"},
    ],
    "steering": [
        {"en": "Check power steering fluid level and look for leaks.", "ur": "پاور اسٹیئرنگ فلوئڈ کی سطح چیک کریں اور لیک دیکھیں۔",
         "why_en": "Low fluid makes steering heavy and can damage the pump.", "why_ur": "کم فلوئڈ اسٹیئرنگ کو بھاری بناتا ہے اور پمپ خراب کر سکتا ہے۔", "prio": "medium"},
        {"en": "Get a wheel alignment if the car pulls or the tyre edges wear.", "ur": "اگر گاڑی کھنچتی ہے یا ٹائر کے کنارے گھستے ہیں تو وہیل الائنمنٹ کروائیں۔",
         "why_en": "Bad alignment wears tyres unevenly and makes steering wander.", "why_ur": "خراب الائنمنٹ ٹائر کو ناہموار گھساتی ہے اور اسٹیئرنگ کو بھٹکتا ہے۔", "prio": "low"},
    ],
    "transmission": [
        {"en": "Change the transmission / clutch fluid if it is overdue.", "ur": "اگر ٹرانسمیشن / کلچ فلوئڈ بدلنے کا وقت گزر گیا ہے تو تبدیل کروائیں۔",
         "why_en": "Old fluid causes hard shifting, slipping and grinding.", "why_ur": "پرانا فلوئڈ مشکل گیئر بدلی، پھسلاؤ اور رگڑ کا سبب بنتا ہے۔", "prio": "medium"},
        {"en": "Have the clutch and gearbox inspected for wear.", "ur": "کلچ اور گیئر باکس کی گھساؤ کی جانچ کروائیں۔",
         "why_en": "A worn clutch slips under load and cannot be fixed by adjustment.", "why_ur": "گھسا کلچ بوجھ تلے پھسلتا ہے اور ایڈجسٹمنٹ سے درست نہیں ہوتا۔", "prio": "high"},
    ],
    "ac": [
        {"en": "Check the cabin air filter - a blocked filter weakens airflow.", "ur": "کیبن ایئر فلٹر چیک کریں - بند فلٹر ہوا کمزور کرتا ہے۔",
         "why_en": "A dirty filter is the cheapest cause of weak cooling.", "why_ur": "گندا فلٹر کمزور ٹھنڈک کی سب سے سستی وجہ ہے۔", "prio": "low"},
        {"en": "Have the AC gas pressure and compressor checked.", "ur": "اے سی گیس پریشر اور کمپریسر چیک کروائیں۔",
         "why_en": "Low gas or a weak compressor stops the AC from cooling.", "why_ur": "کم گیس یا کمزور کمپریسر اے سی کو ٹھنڈا نہیں ہونے دیتا۔", "prio": "medium"},
    ],
    "exhaust": [
        {"en": "Identify the smoke colour and tell the mechanic - it points to the cause.", "ur": "دھوئیں کا رنگ بتائیں اور میکینک کو بتائیں - یہ وجہ کی نشاندہی کرتا ہے۔",
         "why_en": "Blue smoke = burning oil, black smoke = rich fuel, white smoke = coolant leak.", "why_ur": "نیلا دھواں = جلتا آئل، کالا دھواں = زیادہ فیول، سفید دھواں = کولنٹ لیک۔", "prio": "medium"},
        {"en": "Check for exhaust leaks and catalytic converter issues.", "ur": "ایگزاسٹ لیک اور کیٹالیٹک کنورٹر کی خرابیاں چیک کروائیں۔",
         "why_en": "Leaks and converter faults cause smoke, smell and failed emissions tests.", "why_ur": "لیک اور کنورٹر کی خرابیاں دھواں، بو اور فیل شدہ اخراجات ٹیسٹ کا سبب بنتی ہیں۔", "prio": "medium"},
    ],
    "oil_leak": [
        {"en": "Find and fix the oil leak, then top up to the correct level.", "ur": "آئل لیک ڈھونڈ کر ٹھیک کروائیں، پھر درست سطح تک آئل بھریں۔",
         "why_en": "Low oil destroys engine parts through friction and overheating.", "why_ur": "کم آئل رگڑ اور زیادہ گرمی سے انجن کے پرزے تباہ کر دیتا ہے۔", "prio": "high"},
        {"en": "Check the valve cover gasket, oil pan and drain plug for the leak source.", "ur": "لیک کے ماخذ کے لیے والو کور گیسکیٹ، آئل پین اور ڈرین پلگ چیک کروائیں۔", "why_en": "Gaskets and the drain plug are the most common leak points.", "why_ur": "گسکیٹ اور ڈرین پلگ عام لیک پوائنٹس ہیں۔", "prio": "medium"},
    ],
}

# Generic safety note appended to every result
SAFETY_NOTE = {
    "en": "This is a preliminary assessment based on your answers only. It is NOT a final diagnosis - always confirm with a qualified mechanic.",
    "ur": "یہ آپ کے جوابات پر مبنی ابتدائی جائزہ ہے، حتمی تشخیص نہیں - ہمیشہ مستند مکینک سے تصدیق کروائیں۔",
}

URGENT_WARNING = {
    "en": "SAFETY WARNING: Your answers suggest a safety-critical problem. If brakes fail, the car overheats badly, or steering becomes uncontrollable - stop the car in a safe place and call a tow truck.",
    "ur": "حفاظتی انتباہ: آپ کے جوابات حفاظتی مسئے کی نشاندہی کرتے ہیں۔ اگر بریک ناکام ہوں، گاڑی بہت گرم ہو یا اسٹیئرنگ قابو سے باہر ہو - گاڑی محفوظ جگہ پر روکیں اور ٹو ٹرک بلائیں۔",
}
