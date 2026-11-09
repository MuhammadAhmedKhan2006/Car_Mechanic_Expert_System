# =====================================================================
#  car_ai.py - IAI Project
#  Rule-Based Expert System for Car Problems (CAR MECHANIC ASSISTANT)
#  A DECISION SUPPORT tool - bilingual: English / Urdu (one button switches the whole app)
#  Run with:  streamlit run car_ai.py
#
#  Features: decision tree on st.session_state.step | report inputs (st.number_input)
#            DECISION MAKING : risk score 0-100 -> urgency level -> drive-or-stop decision
#            DECISION SUPPORT: why-this-decision list, "defending this suggestion" panel
#                              (strongest factor, why not higher/lower, confidence), action plan,
#                              downloadable mechanic handover report (extra feature)
#            safe wording (never a final diagnosis)
# =====================================================================
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Car Mechanic AI", page_icon="🚗", layout="centered")   # first Streamlit command

s = st.session_state   # short name for st.session_state

def reset_system():
    # Start a new consultation (the language choice is kept)
    s.step = 'start'; s.patient_data = {}; s.report_data = {}
    s.risk = 0; s.reasons = []; s.balloons_done = False; s.area = "-|-"


# ---------- Look and feel: animated, responsive CSS (one block, injected with st.markdown) ----------
CSS = """<style>
html, body, .stApp, button, input, textarea {font-family: 'Segoe UI', 'Noto Naskh Arabic', 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', Tahoma, Arial, sans-serif;}
.stApp {background: linear-gradient(135deg, #eaf2ff 0%, #f7fbff 45%, #e9f8f0 100%) !important; background-size: 300% 300% !important; animation: bgshift 20s ease infinite; color: #14213D;}
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp span, .stApp div[data-testid="stMarkdownContainer"] {color: #14213D;}
.block-container {max-width: 860px; padding-top: 2rem;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #ffffff, #e8f1ff) !important; border-right: 1px solid #d9e6f7;}
h1 {font-weight: 800 !important; color: #1F3A5F !important; letter-spacing: -0.5px; animation: fadeUp .6s ease both;}
@keyframes bgshift {0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;}}
@keyframes fadeUp {from {opacity: 0; transform: translateY(14px);} to {opacity: 1; transform: translateY(0);}}
@keyframes grow {from {width: 0;}}
@keyframes drive {0% {left: -60px;} 100% {left: calc(100% + 10px);}}
@keyframes roadmove {to {background-position: -34px 0;}}
@keyframes slide {from {left: 0;}}
@keyframes pulse {0%, 100% {box-shadow: 0 0 0 0 rgba(239,68,68,.55);} 50% {box-shadow: 0 0 0 14px rgba(239,68,68,0);}}
@keyframes bob {0%, 100% {transform: translateY(0);} 50% {transform: translateY(-2px);}}
.hero {position: relative; overflow: hidden; border-radius: 20px; padding: 18px 20px 38px; margin: 6px 0 14px; background: linear-gradient(120deg, #1F3A5F, #0F766E, #2563EB); background-size: 240% 240%; animation: bgshift 10s ease infinite, fadeUp .6s ease both; box-shadow: 0 10px 30px rgba(31,58,95,.28);}
.stApp .hero, .stApp .hero * {color: #ffffff !important;}
.hero .tag {font-size: 1.15rem; font-weight: 800; letter-spacing: .3px;}
.hero .sub {opacity: .92; font-size: .88rem; margin-top: 2px;}
.road {position: absolute; left: 0; right: 0; bottom: 10px; height: 3px; background: repeating-linear-gradient(90deg, rgba(255,255,255,.9) 0 18px, transparent 18px 34px); background-size: 34px 3px; animation: roadmove 1.1s linear infinite;}
.car {position: absolute; bottom: 13px; left: -60px; font-size: 1.7rem; animation: drive 7s linear infinite, bob .5s ease-in-out infinite;}
.qcard {background: #ffffff; color: #14213D; border-radius: 18px; padding: 16px 18px; margin: 8px 0 12px; border: 1px solid #e0e9f6; box-shadow: 0 8px 24px rgba(20,33,61,.09); animation: fadeUp .45s ease both;}
.qtop {display: flex; align-items: center; gap: 12px; margin-bottom: 10px;}
.qno {background: linear-gradient(135deg, #0F766E, #2563EB); border-radius: 999px; padding: 3px 12px; font-weight: 700; font-size: .8rem; white-space: nowrap;}
.stApp .qno {color: #ffffff;}
.qbar {flex: 1; height: 8px; border-radius: 99px; background: #e3ecf8; overflow: hidden;}
.qbar span {display: block; height: 100%; border-radius: 99px; background: linear-gradient(90deg, #0F766E, #22C55E); animation: grow .8s ease both;}
.qtext {font-size: 1.12rem; font-weight: 600; line-height: 1.55;}
.stButton > button, .stDownloadButton > button {border-radius: 14px; min-height: 3rem; height: auto; padding: .55rem .9rem; font-weight: 700; white-space: normal; border: 1.5px solid #cfe0f5; background: #ffffff; color: #14213D; box-shadow: 0 4px 12px rgba(20,33,61,.08); transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;}
.stButton > button:hover, .stDownloadButton > button:hover {transform: translateY(-3px) scale(1.02); box-shadow: 0 12px 24px rgba(37,99,235,.24); border-color: #2563EB;}
.stButton > button:active, .stDownloadButton > button:active {transform: scale(.97);}
.stButton > button p, .stDownloadButton > button p {color: inherit; margin: 0;}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {background: linear-gradient(135deg, #0F766E, #22C55E); color: #ffffff; border: none;}
.stDownloadButton > button {background: linear-gradient(135deg, #C2410C, #F59E0B); color: #ffffff; border: none;}
.stApp .stButton > button[kind="primary"] p, .stApp .stButton > button[data-testid="stBaseButton-primary"] p, .stApp .stDownloadButton > button p {color: #ffffff;}
[data-testid="stAlert"] {border-radius: 16px; box-shadow: 0 6px 18px rgba(20,33,61,.08); animation: fadeUp .5s ease both;}
[data-testid="stNumberInput"] input {border-radius: 12px; font-weight: 700;}
.drive {border-radius: 18px; padding: 14px 18px; margin: 10px 0; font-weight: 700; box-shadow: 0 8px 22px rgba(0,0,0,.16); animation: fadeUp .5s ease both;}
.stApp .drive {color: #ffffff;}
.v-emergency {background: linear-gradient(135deg, #B91C1C, #EF4444); animation: fadeUp .5s ease both, pulse 1.6s ease-in-out infinite;}
.v-urgent {background: linear-gradient(135deg, #C2410C, #F59E0B);}
.v-routine {background: linear-gradient(135deg, #CA8A04, #FACC15);}
.stApp .v-routine {color: #3B2F00;}
.v-selfcare {background: linear-gradient(135deg, #15803D, #22C55E);}
.meter {position: relative; display: flex; direction: ltr; height: 16px; border-radius: 99px; margin: 44px 6px 12px;}
.meter .sg {height: 100%;}
.s1 {width: 20%; background: #22C55E; border-radius: 99px 0 0 99px;}
.s2 {width: 20%; background: #F4C430;}
.s3 {width: 30%; background: #F08A24;}
.s4 {width: 30%; background: #D62828; border-radius: 0 99px 99px 0;}
.pointer {position: absolute; top: -34px; left: var(--p); transform: translateX(-50%); animation: slide 1.3s cubic-bezier(.2,.8,.2,1) both; text-align: center;}
.pointer span {display: block; background: #14213D; border-radius: 8px; padding: 1px 9px; font-size: .78rem; font-weight: 800;}
.stApp .pointer span {color: #ffffff;}
.pointer::after {content: ''; display: block; width: 4px; height: 26px; background: #14213D; border-radius: 4px; margin: 2px auto 0;}
.legend {display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: .78rem; margin-bottom: 8px;}
.legend span::before {content: ''; display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-inline-end: 5px; background: var(--c);}
.stepc {display: flex; gap: 12px; align-items: center; background: #ffffff; color: #14213D; border: 1px solid #e0e9f6; border-radius: 14px; padding: 10px 14px; margin: 6px 0; box-shadow: 0 4px 12px rgba(20,33,61,.07); animation: fadeUp .5s ease both;}
.stepc b {flex: 0 0 30px; height: 30px; border-radius: 50%; background: linear-gradient(135deg, #0F766E, #2563EB); display: flex; align-items: center; justify-content: center;}
.stApp .stepc b {color: #ffffff;}
@media (max-width: 640px) {
  .block-container {padding: 1rem .8rem 3rem;}
  h1 {font-size: 1.45rem !important; line-height: 1.25;}
  .hero {padding: 14px 14px 34px; border-radius: 16px;}
  .hero .tag {font-size: 1rem;}
  .qtext {font-size: 1.02rem;}
  [data-testid="stHorizontalBlock"] {flex-direction: row !important; flex-wrap: nowrap !important; gap: .5rem !important;}
  [data-testid="stColumn"], [data-testid="column"] {min-width: 0 !important; width: auto !important; flex: 1 1 0 !important;}
  .stButton > button, .stDownloadButton > button {min-height: 3.2rem; font-size: .92rem; padding: .5rem .5rem;}
  .drive {font-size: .95rem; padding: 12px 14px;}
}
@media (prefers-reduced-motion: reduce) {* {animation: none !important; transition: none !important;}}
</style>"""
CSS_UR = "<style>.stApp {direction: rtl; text-align: right; line-height: 2.1;} .qtext {line-height: 2.2;} .legend {flex-direction: row;}</style>"

if 'step' not in s:    # first time only
    s.lang = 'en'; reset_system()

# ---------- Language: 'en' = English, 'ur' = Urdu ----------
L = s.lang


def T(en, ur):
    # Pick UI text for the active language (English or Urdu)
    return en if L == 'en' else ur


YES = T('✅ Yes', '✅ جی ہاں')
NO = T('❌ No', '❌ نہیں')
QN = T('Q', 'سوال ')
SUBMIT = T('📥 Submit Report Value', '📥 رپورٹ کی قدر جمع کریں')
NEW = T('🔄 Start New Consultation', '🔄 نیا مشورہ شروع کریں')
RPT = T('📄 Report input', '📄 رپورٹ کی قدر')
st.markdown(CSS, unsafe_allow_html=True)
if L == 'ur':   # right-to-left layout for Urdu
    st.markdown(CSS_UR, unsafe_allow_html=True)

st.title(T('🚗 IAI Expert System: Car Mechanic Assistant', '🚗 آئی اے آئی ایکسپرٹ سسٹم: کار مکینک اسسٹنٹ'))
st.markdown("<div class='hero'><div class='tag'>" + (T('Decide. Defend. Drive safe.', 'فیصلہ۔ وضاحت۔ محفوظ سفر۔')) + "</div><div class='sub'>" + (T('Your pocket car mechanic: answer a few questions and get a clear, explained decision.', 'آپ کا جیبی کار مکینک: چند سوالوں کے جواب دیں اور وضاحت کے ساتھ واضح فیصلہ پائیں۔')) + "</div><div class='road'></div><div class='car'>🚗</div></div>", unsafe_allow_html=True)
st.warning(T('⚠️ Disclaimer: This is a DECISION SUPPORT tool, NOT a replacement for a qualified mechanic. It never gives a final diagnosis. Always get your car checked by a qualified mechanic.', '⚠️ اعلان: یہ صرف فیصلہ سازی میں مدد کا ٹول ہے، کسی مستند مکینک کا متبادل نہیں۔ یہ کبھی حتمی تشخیص نہیں دیتا۔ اپنی گاڑی ہمیشہ کسی مستند مکینک سے چیک کروائیں۔'))
_next_lang = {'en': 'ur', 'ur': 'en'}
_lang_label = {'en': '🇬🇧 English', 'ur': '🇵🇰 اردو'}
if st.button(_lang_label[_next_lang[L]], key="lang_btn"):
    s.lang = _next_lang[L]; st.rerun()

step = s.step

# =====================================================================
#  ONE BIG DECISION TREE (if / elif on s.step)
#  Every serious answer adds risk points + a reason INLINE.
#  Reasons are stored as "English|Urdu|points" so the language button works anytime.
#  max(risk + points, 70) = emergency sign; max(risk + points, 40) = needs a mechanic today.
# =====================================================================
if step == 'start':
    st.write("### " + (T('👋 Welcome! What problem is your car having?', '👋 خوش آمدید! آپ کی گاڑی میں کیا مسئلہ ہے؟')))
    st.write((T('Choose the problem that matches best:', 'جو مسئلہ سب سے زیادہ ملتا ہو اسے منتخب کریں:')))
    c1, c2 = st.columns(2); c3, c4 = st.columns(2); c5, c6 = st.columns(2); c7, c8 = st.columns(2); c9, c10 = st.columns(2)
    if c1.button((T("🔑 Engine won't start", '🔑 انجن اسٹارٹ نہیں ہوتا')), key="s1"): s.patient_data['complaint'] = 'Engine will not start'; s.area = "Starting system (battery / starter / fuel)|اسٹارٹنگ سسٹم (بیٹری / سیلف اسٹارٹر / فیول)"; s.step = 'ns1'; st.rerun()
    elif c2.button((T('🌡️ Overheating', '🌡️ انجن زیادہ گرم ہو رہا ہے')), key="s2"): s.patient_data['complaint'] = 'Overheating'; s.area = "Cooling system (coolant / radiator / fan)|کولنگ سسٹم (کولنٹ / ریڈی ایٹر / پنکھا)"; s.step = 'oh1'; st.rerun()
    elif c3.button((T('🛑 Brake problem', '🛑 بریک کا مسئلہ')), key="s3"): s.patient_data['complaint'] = 'Brake problem'; s.area = "Brake system (pads / fluid / discs)|بریک سسٹم (پیڈز / فلوئڈ / ڈسک)"; s.step = 'br1'; st.rerun()
    elif c4.button((T('🔊 Strange noise / vibration', '🔊 عجیب آواز یا جھٹکے')), key="s4"): s.patient_data['complaint'] = 'Strange noise or vibration'; s.area = "Engine, belts or suspension (source of the noise)|انجن، بیلٹ یا سسپنشن (آواز کا ماخذ)"; s.step = 'nv1'; st.rerun()
    elif c5.button((T('🔋 Battery / electrical / lights', '🔋 بیٹری / بجلی / لائٹس کا مسئلہ')), key="s5"): s.patient_data['complaint'] = 'Battery / electrical / lights'; s.area = "Electrical system (battery / charging / wiring)|بجلی کا نظام (بیٹری / چارجنگ / وائرنگ)"; s.step = 'el1'; st.rerun()
    elif c6.button((T('🛞 Tyre problem', '🛞 ٹائر کا مسئلہ')), key="s6"): s.patient_data['complaint'] = 'Tyre problem'; s.area = "Tyres and wheels|ٹائر اور پہیے"; s.step = 'ty1'; st.rerun()
    elif c7.button((T('🛢️ Oil leak / smoke', '🛢️ آئل لیک / دھواں')), key="s7"): s.patient_data['complaint'] = 'Oil leak or smoke'; s.area = "Engine oil system (oil level / leaks / burning oil)|انجن آئل سسٹم (آئل کی سطح / لیک / جلتا آئل)"; s.step = 'ol1'; st.rerun()
    elif c8.button((T('❄️ AC not cooling', '❄️ اے سی ٹھنڈا نہیں کر رہا')), key="s8"): s.patient_data['complaint'] = 'AC not cooling'; s.area = "Air conditioning system (gas / filter / compressor)|ایئر کنڈیشننگ سسٹم (گیس / فلٹر / کمپریسر)"; s.step = 'ac1'; st.rerun()
    elif c9.button((T('🎡 Steering problem', '🎡 اسٹیئرنگ کا مسئلہ')), key="s9"): s.patient_data['complaint'] = 'Steering problem'; s.area = "Steering system (fluid / alignment / tyres)|اسٹیئرنگ سسٹم (فلوئڈ / الائنمنٹ / ٹائر)"; s.step = 'sr1'; st.rerun()
    elif c10.button((T('⚙️ Gear / clutch problem', '⚙️ گیئر / کلچ کا مسئلہ')), key="s10"): s.patient_data['complaint'] = 'Gear or clutch problem'; s.area = "Gearbox and clutch|گیئر باکس اور کلچ"; s.step = 'gc1'; st.rerun()

# ---------- PROBLEM: Engine will not start ----------
elif step == 'ns1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('When you turn the key, do the dashboard lights stay completely off?', 'چابی گھمانے پر کیا ڈیش بورڈ کی لائٹس بالکل بند رہتی ہیں؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns1y", type="primary"):
        s.patient_data['dash_lights_off'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Dashboard lights completely off: +15 risk|ڈیش بورڈ کی لائٹس بالکل بند: +15 رسک|15")
        s.step = 'ns2'; st.rerun()
    if c2.button(NO, key="ns1n"): s.patient_data['dash_lights_off'] = "No"; s.step = 'ns2'; st.rerun()
elif step == 'ns2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Do you hear a rapid clicking sound when you try to start the car?', 'کیا اسٹارٹ کرنے پر تیز ٹک ٹک کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns2y", type="primary"):
        s.patient_data['clicking_sound'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Rapid clicking when starting: +10 risk|اسٹارٹ کرتے وقت تیز ٹک ٹک: +10 رسک|10")
        s.step = 'ns3'; st.rerun()
    if c2.button(NO, key="ns2n"): s.patient_data['clicking_sound'] = "No"; s.step = 'ns3'; st.rerun()
elif step == 'ns3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Does the engine crank (turn over) but still not start?', 'کیا انجن گھومتا ہے مگر پھر بھی اسٹارٹ نہیں ہوتا؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns3y", type="primary"):
        s.patient_data['cranks_no_start'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Engine cranks but does not start: +10 risk|انجن گھومتا ہے مگر اسٹارٹ نہیں ہوتا: +10 رسک|10")
        s.step = 'ns4'; st.rerun()
    if c2.button(NO, key="ns3n"): s.patient_data['cranks_no_start'] = "No"; s.step = 'ns4'; st.rerun()
elif step == 'ns4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Is the fuel gauge showing empty or very low?', 'کیا فیول گیج خالی یا بہت کم دکھا رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns4y", type="primary"):
        s.patient_data['fuel_low'] = "Yes"; s.reasons.append("Fuel is low: refilling may solve the problem (lower concern)|فیول کم ہے: ٹینک بھروانے سے مسئلہ حل ہو سکتا ہے (کم تشویش)|0")
        s.step = 'ns5'; st.rerun()
    if c2.button(NO, key="ns4n"): s.patient_data['fuel_low'] = "No"; s.step = 'ns5'; st.rerun()
elif step == 'ns5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Do you smell petrol, or see smoke coming from the engine area?', 'کیا انجن کے حصے سے پیٹرول کی بو یا دھواں آ رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns5y", type="primary"):
        s.patient_data['petrol_smell_smoke'] = "Yes"; s.risk = max(s.risk + 40, 70); s.reasons.append("Petrol smell / smoke from the engine area: +40 risk (EMERGENCY sign)|انجن کے حصے سے پیٹرول کی بو یا دھواں: +40 رسک (ایمرجنسی کی علامت)|40")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ns5n"): s.patient_data['petrol_smell_smoke'] = "No"; s.step = 'ns_bat'; st.rerun()
elif step == 'ns_bat':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the battery voltage from a multimeter or workshop report (normal 12.4 - 12.8 V)', '📄 ملٹی میٹر یا ورکشاپ کی رپورٹ سے بیٹری وولٹیج درج کریں (نارمل 12.4 تا 12.8 وولٹ)')))
    val = st.number_input((T('Battery voltage (V)', 'بیٹری وولٹیج (وولٹ)')), min_value=0.0, max_value=20.0, value=12.6, step=0.1, format="%.1f", key="ns_bat_in")
    if st.button(SUBMIT, key="ns_bat_b", type="primary"):
        s.report_data['battery_voltage'] = val; s.step = 'ns6'
        if val < 11.0: s.risk = s.risk + 30; s.reasons.append("Battery voltage very low (" + str(val) + " V): +30 risk|بیٹری وولٹیج بہت کم (" + str(val) + " وولٹ): +30 رسک|30")
        elif val < 12.2: s.risk = s.risk + 15; s.reasons.append("Battery voltage low (" + str(val) + " V): +15 risk|بیٹری وولٹیج کم (" + str(val) + " وولٹ): +15 رسک|15")
        elif val > 15.0: s.risk = s.risk + 20; s.reasons.append("Battery voltage too high (" + str(val) + " V), charging system needs a check: +20 risk|بیٹری وولٹیج بہت زیادہ (" + str(val) + " وولٹ)، چارجنگ سسٹم چیک کروائیں: +20 رسک|20")
        st.rerun()
elif step == 'ns6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Is the battery more than 3 years old?', 'کیا بیٹری تین سال سے زیادہ پرانی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ns6y", type="primary"):
        s.patient_data['battery_old'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Battery older than 3 years: +10 risk|بیٹری تین سال سے پرانی ہے: +10 رسک|10")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ns6n"): s.patient_data['battery_old'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Overheating ----------
elif step == 'oh1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Is the temperature warning light on, or is the gauge in the red zone?', 'کیا درجہ حرارت کی وارننگ لائٹ جل رہی ہے یا گیج سرخ حصے میں ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh1y", type="primary"):
        s.patient_data['temp_warning'] = "Yes"; s.risk = s.risk + 25; s.reasons.append("Temperature warning light / red gauge: +25 risk|درجہ حرارت کی وارننگ لائٹ / سرخ گیج: +25 رسک|25")
        s.step = 'oh2'; st.rerun()
    if c2.button(NO, key="oh1n"): s.patient_data['temp_warning'] = "No"; s.step = 'oh2'; st.rerun()
elif step == 'oh2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is steam or smoke coming out from under the bonnet?', 'کیا بونٹ کے نیچے سے بھاپ یا دھواں نکل رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh2y", type="primary"):
        s.patient_data['steam_smoke'] = "Yes"; s.risk = max(s.risk + 40, 70); s.reasons.append("Steam / smoke from the bonnet: +40 risk (EMERGENCY sign)|بونٹ سے بھاپ یا دھواں: +40 رسک (ایمرجنسی کی علامت)|40")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="oh2n"): s.patient_data['steam_smoke'] = "No"; s.step = 'oh3'; st.rerun()
elif step == 'oh3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Is the coolant level low, or do you have to top it up often?', 'کیا کولنٹ کی سطح کم ہے یا بار بار ڈالنا پڑتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh3y", type="primary"):
        s.patient_data['coolant_low'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Coolant level low: +15 risk|کولنٹ کی سطح کم: +15 رسک|15")
        s.step = 'oh4'; st.rerun()
    if c2.button(NO, key="oh3n"): s.patient_data['coolant_low'] = "No"; s.step = 'oh4'; st.rerun()
elif step == 'oh4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Is the radiator fan not spinning, or is the AC not working?', 'کیا ریڈی ایٹر کا پنکھا نہیں چل رہا یا اے سی کام نہیں کر رہا؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh4y", type="primary"):
        s.patient_data['fan_not_working'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Radiator fan / AC not working: +10 risk|ریڈی ایٹر کا پنکھا / اے سی کام نہیں کر رہا: +10 رسک|10")
        s.step = 'oh5'; st.rerun()
    if c2.button(NO, key="oh4n"): s.patient_data['fan_not_working'] = "No"; s.step = 'oh5'; st.rerun()
elif step == 'oh5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Do you see coolant puddles under the car, or smell something sweet?', 'کیا گاڑی کے نیچے کولنٹ کے دھبے نظر آتے ہیں یا میٹھی بو آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh5y", type="primary"):
        s.patient_data['coolant_leak'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Coolant leak or sweet smell: +15 risk|کولنٹ لیک یا میٹھی بو: +15 رسک|15")
        s.step = 'oh_temp'; st.rerun()
    if c2.button(NO, key="oh5n"): s.patient_data['coolant_leak'] = "No"; s.step = 'oh_temp'; st.rerun()
elif step == 'oh_temp':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the engine temperature from the dashboard gauge (normal 85 - 105 °C)', '📄 ڈیش بورڈ گیج سے انجن کا درجہ حرارت درج کریں (نارمل 85 تا 105 ڈگری سینٹی گریڈ)')))
    val = st.number_input((T('Engine temperature (°C)', 'انجن کا درجہ حرارت (ڈگری سینٹی گریڈ)')), min_value=20, max_value=200, value=90, step=1, key="oh_temp_in")
    if st.button(SUBMIT, key="oh_temp_b", type="primary"):
        s.report_data['engine_temp'] = val; s.step = 'oh6'
        if val >= 120: s.risk = max(s.risk + 50, 70); s.reasons.append("Engine temperature dangerously high (" + str(val) + " °C): +50 risk (EMERGENCY sign)|انجن کا درجہ حرارت خطرناک حد تک زیادہ (" + str(val) + " ڈگری): +50 رسک (ایمرجنسی کی علامت)|50"); s.step = 'end'
        elif val > 105: s.risk = s.risk + 20; s.reasons.append("Engine temperature high (" + str(val) + " °C): +20 risk|انجن کا درجہ حرارت زیادہ (" + str(val) + " ڈگری): +20 رسک|20")
        elif val < 70: s.risk = s.risk + 5; s.reasons.append("Engine running cold (" + str(val) + " °C): +5 risk|انجن ٹھنڈا چل رہا ہے (" + str(val) + " ڈگری): +5 رسک|5")
        st.rerun()
elif step == 'oh6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Was the coolant last changed more than 2 years ago?', 'کیا کولنٹ آخری بار دو سال سے زیادہ پہلے تبدیل ہوا تھا؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="oh6y", type="primary"):
        s.patient_data['coolant_old'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Coolant not changed for over 2 years: +10 risk|کولنٹ دو سال سے زیادہ عرصے سے تبدیل نہیں ہوا: +10 رسک|10")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="oh6n"): s.patient_data['coolant_old'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Brake problem ----------
elif step == 'br1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Does the brake pedal feel very soft, or sink to the floor?', 'کیا بریک پیڈل بہت نرم محسوس ہوتا ہے یا فرش تک چلا جاتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br1y", type="primary"):
        s.patient_data['soft_pedal'] = "Yes"; s.risk = max(s.risk + 50, 70); s.reasons.append("Soft brake pedal: +50 risk (EMERGENCY sign)|بریک پیڈل نرم: +50 رسک (ایمرجنسی کی علامت)|50")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="br1n"): s.patient_data['soft_pedal'] = "No"; s.step = 'br2'; st.rerun()
elif step == 'br2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Do you hear grinding or loud squealing when you brake?', 'کیا بریک لگاتے وقت رگڑنے یا تیز چیخنے کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br2y", type="primary"):
        s.patient_data['brake_grinding'] = "Yes"; s.risk = max(s.risk + 20, 40); s.reasons.append("Grinding / squealing when braking: +20 risk (URGENT check needed)|بریک لگاتے وقت رگڑنے / چیخنے کی آواز: +20 رسک (فوری چیک ضروری)|20")
        s.step = 'br3'; st.rerun()
    if c2.button(NO, key="br2n"): s.patient_data['brake_grinding'] = "No"; s.step = 'br3'; st.rerun()
elif step == 'br3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Does the car pull to one side when you brake?', 'کیا بریک لگانے پر گاڑی ایک طرف کھنچتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br3y", type="primary"):
        s.patient_data['brake_pull'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Car pulls to one side when braking: +15 risk|بریک لگانے پر گاڑی ایک طرف کھنچتی ہے: +15 رسک|15")
        s.step = 'br4'; st.rerun()
    if c2.button(NO, key="br3n"): s.patient_data['brake_pull'] = "No"; s.step = 'br4'; st.rerun()
elif step == 'br4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Is the brake warning light on the dashboard?', 'کیا ڈیش بورڈ پر بریک کی وارننگ لائٹ جل رہی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br4y", type="primary"):
        s.patient_data['brake_light'] = "Yes"; s.risk = max(s.risk + 20, 40); s.reasons.append("Brake warning light on: +20 risk (URGENT check needed)|بریک کی وارننگ لائٹ جل رہی ہے: +20 رسک (فوری چیک ضروری)|20")
        s.step = 'br5'; st.rerun()
    if c2.button(NO, key="br4n"): s.patient_data['brake_light'] = "No"; s.step = 'br5'; st.rerun()
elif step == 'br5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Does the steering wheel or brake pedal shake when you brake?', 'کیا بریک لگانے پر اسٹیئرنگ یا بریک پیڈل ہلتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br5y", type="primary"):
        s.patient_data['brake_vibration'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Shaking when braking: +10 risk|بریک لگانے پر ہلنا: +10 رسک|10")
        s.step = 'br_km'; st.rerun()
    if c2.button(NO, key="br5n"): s.patient_data['brake_vibration'] = "No"; s.step = 'br_km'; st.rerun()
elif step == 'br_km':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the kilometres driven since the last service (normal: below 10000 km)', '📄 پچھلی سروس کے بعد چلائے گئے کلومیٹر درج کریں (نارمل: 10000 سے کم)')))
    val = st.number_input((T('Km since last service', 'پچھلی سروس کے بعد کلومیٹر')), min_value=0, max_value=100000, value=5000, step=500, key="br_km_in")
    if st.button(SUBMIT, key="br_km_b", type="primary"):
        s.report_data['km_since_service'] = val; s.step = 'br6'
        if val >= 20000: s.risk = s.risk + 20; s.reasons.append("Service overdue (" + str(val) + " km since last service): +20 risk|سروس کا وقت گزر چکا (" + str(val) + " کلومیٹر): +20 رسک|20")
        elif val >= 10000: s.risk = s.risk + 10; s.reasons.append("Service due soon (" + str(val) + " km since last service): +10 risk|سروس جلد درکار (" + str(val) + " کلومیٹر): +10 رسک|10")
        st.rerun()
elif step == 'br6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Is the brake fluid level low?', 'کیا بریک آئل (فلوئڈ) کی سطح کم ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="br6y", type="primary"):
        s.patient_data['brake_fluid_low'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Brake fluid low: +15 risk|بریک فلوئڈ کم ہے: +15 رسک|15")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="br6n"): s.patient_data['brake_fluid_low'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Strange noise or vibration ----------
elif step == 'nv1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Do you hear a knocking or tapping sound from the engine?', 'کیا انجن سے کھٹکھٹانے یا ٹک ٹک کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv1y", type="primary"):
        s.patient_data['engine_knock'] = "Yes"; s.risk = s.risk + 20; s.reasons.append("Knocking / tapping sound from the engine: +20 risk|انجن سے کھٹکھٹانے کی آواز: +20 رسک|20")
        s.step = 'nv2'; st.rerun()
    if c2.button(NO, key="nv1n"): s.patient_data['engine_knock'] = "No"; s.step = 'nv2'; st.rerun()
elif step == 'nv2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Do you hear a squealing sound when starting the car or turning the steering wheel?', 'کیا گاڑی اسٹارٹ کرتے یا اسٹیئرنگ گھماتے وقت چیخنے کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv2y", type="primary"):
        s.patient_data['belt_squeal'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Squealing noise (a belt may be loose or worn): +10 risk|چیخنے کی آواز (بیلٹ ڈھیلی یا گھسی ہو سکتی ہے): +10 رسک|10")
        s.step = 'nv3'; st.rerun()
    if c2.button(NO, key="nv2n"): s.patient_data['belt_squeal'] = "No"; s.step = 'nv3'; st.rerun()
elif step == 'nv3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Is there a humming or rumbling noise that gets louder as speed increases?', 'کیا ایسی گونجنے یا گڑگڑانے کی آواز ہے جو رفتار بڑھنے پر بڑھ جاتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv3y", type="primary"):
        s.patient_data['speed_hum'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Humming noise rising with speed (wheel bearing may need a check): +15 risk|رفتار کے ساتھ بڑھتی گونج (وہیل بیئرنگ چیک کروائیں): +15 رسک|15")
        s.step = 'nv4'; st.rerun()
    if c2.button(NO, key="nv3n"): s.patient_data['speed_hum'] = "No"; s.step = 'nv4'; st.rerun()
elif step == 'nv4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Do you hear a clunk when driving over bumps?', 'کیا اونچی نیچی سڑک پر ٹھک ٹھک کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv4y", type="primary"):
        s.patient_data['bump_clunk'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Clunking over bumps (suspension may need a check): +10 risk|اونچی نیچی سڑک پر ٹھک ٹھک (سسپنشن چیک کروائیں): +10 رسک|10")
        s.step = 'nv5'; st.rerun()
    if c2.button(NO, key="nv4n"): s.patient_data['bump_clunk'] = "No"; s.step = 'nv5'; st.rerun()
elif step == 'nv5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Does the steering wheel or seat vibrate at higher speeds?', 'کیا زیادہ رفتار پر اسٹیئرنگ یا سیٹ میں کپکپاہٹ ہوتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv5y", type="primary"):
        s.patient_data['speed_vibration'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Vibration at higher speeds: +10 risk|زیادہ رفتار پر کپکپاہٹ: +10 رسک|10")
        s.step = 'nv_oil'; st.rerun()
    if c2.button(NO, key="nv5n"): s.patient_data['speed_vibration'] = "No"; s.step = 'nv_oil'; st.rerun()
elif step == 'nv_oil':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the oil level from the dipstick as a percentage (normal 60 - 100 %)', '📄 ڈپ اسٹک سے آئل کی سطح فیصد میں درج کریں (نارمل 60 تا 100 فیصد)')))
    val = st.number_input((T('Oil level (%)', 'آئل کی سطح (فیصد)')), min_value=0, max_value=100, value=70, step=1, key="nv_oil_in")
    if st.button(SUBMIT, key="nv_oil_b", type="primary"):
        s.report_data['oil_level'] = val; s.step = 'nv6'
        if val < 15: s.risk = max(s.risk + 40, 70); s.reasons.append("Oil level critically low (" + str(val) + " %): +40 risk (EMERGENCY sign)|آئل کی سطح انتہائی کم (" + str(val) + " فیصد): +40 رسک (ایمرجنسی کی علامت)|40"); s.step = 'end'
        elif val < 30: s.risk = s.risk + 20; s.reasons.append("Oil level very low (" + str(val) + " %): +20 risk|آئل کی سطح بہت کم (" + str(val) + " فیصد): +20 رسک|20")
        elif val < 50: s.risk = s.risk + 10; s.reasons.append("Oil level low (" + str(val) + " %): +10 risk|آئل کی سطح کم (" + str(val) + " فیصد): +10 رسک|10")
        st.rerun()
elif step == 'nv6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Is the noise getting louder over time?', 'کیا آواز وقت کے ساتھ بڑھ رہی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="nv6y", type="primary"):
        s.patient_data['noise_increasing'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Noise is getting louder: +15 risk|آواز بڑھتی جا رہی ہے: +15 رسک|15")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="nv6n"): s.patient_data['noise_increasing'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Battery / electrical / lights ----------
elif step == 'el1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Are the headlights dim or flickering?', 'کیا ہیڈ لائٹس مدھم ہیں یا جھلملا رہی ہیں؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el1y", type="primary"):
        s.patient_data['dim_lights'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Dim or flickering headlights: +10 risk|ہیڈ لائٹس مدھم یا جھلملا رہی ہیں: +10 رسک|10")
        s.step = 'el2'; st.rerun()
    if c2.button(NO, key="el1n"): s.patient_data['dim_lights'] = "No"; s.step = 'el2'; st.rerun()
elif step == 'el2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is the battery warning light on the dashboard?', 'کیا ڈیش بورڈ پر بیٹری کی وارننگ لائٹ جل رہی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el2y", type="primary"):
        s.patient_data['battery_light'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Battery warning light on: +15 risk|بیٹری کی وارننگ لائٹ جل رہی ہے: +15 رسک|15")
        s.step = 'el3'; st.rerun()
    if c2.button(NO, key="el2n"): s.patient_data['battery_light'] = "No"; s.step = 'el3'; st.rerun()
elif step == 'el3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Do the power windows, wipers or radio work slowly or stop at random?', 'کیا پاور ونڈوز، وائپرز یا ریڈیو سست چلتے ہیں یا اچانک بند ہو جاتے ہیں؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el3y", type="primary"):
        s.patient_data['electrics_erratic'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Electrical parts working slowly or stopping: +10 risk|بجلی کے پرزے سست یا اچانک بند: +10 رسک|10")
        s.step = 'el4'; st.rerun()
    if c2.button(NO, key="el3n"): s.patient_data['electrics_erratic'] = "No"; s.step = 'el4'; st.rerun()
elif step == 'el4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Do you smell burning plastic, or see smoke from the wiring or fuse box?', 'کیا جلتے ہوئے پلاسٹک کی بو آ رہی ہے یا تاروں یا فیوز بکس سے دھواں نکل رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el4y", type="primary"):
        s.patient_data['burning_smell'] = "Yes"; s.risk = max(s.risk + 45, 70); s.reasons.append("Burning smell / smoke from wiring: +45 risk (EMERGENCY sign)|تاروں سے جلنے کی بو / دھواں: +45 رسک (ایمرجنسی کی علامت)|45")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="el4n"): s.patient_data['burning_smell'] = "No"; s.step = 'el5'; st.rerun()
elif step == 'el5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Does a fuse blow again and again?', 'کیا فیوز بار بار جل جاتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el5y", type="primary"):
        s.patient_data['fuse_blowing'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Fuse blowing repeatedly: +10 risk|فیوز بار بار جل رہا ہے: +10 رسک|10")
        s.step = 'el_bat'; st.rerun()
    if c2.button(NO, key="el5n"): s.patient_data['fuse_blowing'] = "No"; s.step = 'el_bat'; st.rerun()
elif step == 'el_bat':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the battery voltage from a multimeter or workshop report (normal 12.4 - 12.8 V)', '📄 ملٹی میٹر یا ورکشاپ کی رپورٹ سے بیٹری وولٹیج درج کریں (نارمل 12.4 تا 12.8 وولٹ)')))
    val = st.number_input((T('Battery voltage (V)', 'بیٹری وولٹیج (وولٹ)')), min_value=0.0, max_value=20.0, value=12.6, step=0.1, format="%.1f", key="el_bat_in")
    if st.button(SUBMIT, key="el_bat_b", type="primary"):
        s.report_data['battery_voltage'] = val; s.step = 'el6'
        if val < 11.0: s.risk = s.risk + 30; s.reasons.append("Battery voltage very low (" + str(val) + " V): +30 risk|بیٹری وولٹیج بہت کم (" + str(val) + " وولٹ): +30 رسک|30")
        elif val < 12.2: s.risk = s.risk + 15; s.reasons.append("Battery voltage low (" + str(val) + " V): +15 risk|بیٹری وولٹیج کم (" + str(val) + " وولٹ): +15 رسک|15")
        elif val > 15.0: s.risk = s.risk + 20; s.reasons.append("Battery voltage too high (" + str(val) + " V), charging system needs a check: +20 risk|بیٹری وولٹیج بہت زیادہ (" + str(val) + " وولٹ)، چارجنگ سسٹم چیک کروائیں: +20 رسک|20")
        st.rerun()
elif step == 'el6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Have extra accessories (audio system, extra lights) been fitted recently?', 'کیا حال ہی میں اضافی سامان (آڈیو سسٹم، اضافی لائٹس) لگوایا گیا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="el6y", type="primary"):
        s.patient_data['accessories_fitted'] = "Yes"; s.risk = s.risk + 5; s.reasons.append("Extra accessories fitted recently: +5 risk|حال ہی میں اضافی سامان لگوایا گیا: +5 رسک|5")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="el6n"): s.patient_data['accessories_fitted'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Tyre problem ----------
elif step == 'ty1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Does a tyre look flat or low on air?', 'کیا کوئی ٹائر پچکا ہوا یا ہوا میں کم لگتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty1y", type="primary"):
        s.patient_data['tyre_flat'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("A tyre looks flat / low: +15 risk|کوئی ٹائر پچکا ہوا / کم ہوا والا ہے: +15 رسک|15")
        s.step = 'ty2'; st.rerun()
    if c2.button(NO, key="ty1n"): s.patient_data['tyre_flat'] = "No"; s.step = 'ty2'; st.rerun()
elif step == 'ty2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is there a bulge or a deep cut on the side of a tyre?', 'کیا ٹائر کے سائیڈ پر ابھار یا گہرا کٹ ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty2y", type="primary"):
        s.patient_data['tyre_bulge'] = "Yes"; s.risk = max(s.risk + 40, 70); s.reasons.append("Bulge / deep cut on a tyre: +40 risk (EMERGENCY sign)|ٹائر پر ابھار / گہرا کٹ: +40 رسک (ایمرجنسی کی علامت)|40")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ty2n"): s.patient_data['tyre_bulge'] = "No"; s.step = 'ty3'; st.rerun()
elif step == 'ty3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Does the car pull to one side while driving straight?', 'کیا سیدھا چلاتے وقت گاڑی ایک طرف کھنچتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty3y", type="primary"):
        s.patient_data['tyre_pull'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Car pulls to one side: +10 risk|گاڑی ایک طرف کھنچتی ہے: +10 رسک|10")
        s.step = 'ty4'; st.rerun()
    if c2.button(NO, key="ty3n"): s.patient_data['tyre_pull'] = "No"; s.step = 'ty4'; st.rerun()
elif step == 'ty4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Is the tyre tread worn out or uneven?', 'کیا ٹائر کی گراری گھس چکی ہے یا ناہموار ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty4y", type="primary"):
        s.patient_data['tread_worn'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Worn or uneven tyre tread: +10 risk|ٹائر کی گراری گھسی ہوئی یا ناہموار: +10 رسک|10")
        s.step = 'ty5'; st.rerun()
    if c2.button(NO, key="ty4n"): s.patient_data['tread_worn'] = "No"; s.step = 'ty5'; st.rerun()
elif step == 'ty5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Does the steering wheel shake at higher speeds?', 'کیا زیادہ رفتار پر اسٹیئرنگ ہلتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty5y", type="primary"):
        s.patient_data['tyre_vibration'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Steering shakes at higher speeds: +10 risk|زیادہ رفتار پر اسٹیئرنگ ہلتا ہے: +10 رسک|10")
        s.step = 'ty_psi'; st.rerun()
    if c2.button(NO, key="ty5n"): s.patient_data['tyre_vibration'] = "No"; s.step = 'ty_psi'; st.rerun()
elif step == 'ty_psi':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the tyre pressure from a gauge (normal 30 - 35 PSI)', '📄 گیج سے ٹائر کا پریشر درج کریں (نارمل 30 تا 35 پی ایس آئی)')))
    val = st.number_input((T('Tyre pressure (PSI)', 'ٹائر کا پریشر (پی ایس آئی)')), min_value=0, max_value=80, value=32, step=1, key="ty_psi_in")
    if st.button(SUBMIT, key="ty_psi_b", type="primary"):
        s.report_data['tyre_pressure'] = val; s.step = 'ty6'
        if val < 20: s.risk = s.risk + 30; s.reasons.append("Tyre pressure very low (" + str(val) + " PSI): +30 risk|ٹائر کا پریشر بہت کم (" + str(val) + " پی ایس آئی): +30 رسک|30")
        elif val < 28: s.risk = s.risk + 15; s.reasons.append("Tyre pressure low (" + str(val) + " PSI): +15 risk|ٹائر کا پریشر کم (" + str(val) + " پی ایس آئی): +15 رسک|15")
        elif val > 40: s.risk = s.risk + 15; s.reasons.append("Tyre pressure too high (" + str(val) + " PSI): +15 risk|ٹائر کا پریشر بہت زیادہ (" + str(val) + " پی ایس آئی): +15 رسک|15")
        st.rerun()
elif step == 'ty6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Are the tyres older than 5 years, or not rotated in the last 10000 km?', 'کیا ٹائر پانچ سال سے پرانے ہیں یا پچھلے 10000 کلومیٹر میں ان کی جگہ تبدیل نہیں ہوئی؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ty6y", type="primary"):
        s.patient_data['tyre_old'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Old tyres / not rotated: +10 risk|پرانے ٹائر / جگہ تبدیل نہیں ہوئی: +10 رسک|10")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ty6n"): s.patient_data['tyre_old'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Oil leak or smoke ----------
elif step == 'ol1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Is the oil pressure or oil warning light on?', 'کیا آئل پریشر یا آئل کی وارننگ لائٹ جل رہی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol1y", type="primary"):
        s.patient_data['oil_light'] = "Yes"; s.risk = max(s.risk + 25, 40); s.reasons.append("Oil warning light on: +25 risk (URGENT check needed)|آئل کی وارننگ لائٹ جل رہی ہے: +25 رسک (فوری چیک ضروری)|25")
        s.step = 'ol2'; st.rerun()
    if c2.button(NO, key="ol1n"): s.patient_data['oil_light'] = "No"; s.step = 'ol2'; st.rerun()
elif step == 'ol2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is blue or grey smoke coming from the exhaust?', 'کیا ایگزاسٹ سے نیلا یا خاکستری دھواں نکل رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol2y", type="primary"):
        s.patient_data['blue_smoke'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Blue / grey exhaust smoke: +15 risk|ایگزاسٹ سے نیلا / خاکستری دھواں: +15 رسک|15")
        s.step = 'ol3'; st.rerun()
    if c2.button(NO, key="ol2n"): s.patient_data['blue_smoke'] = "No"; s.step = 'ol3'; st.rerun()
elif step == 'ol3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Is black smoke coming from the exhaust?', 'کیا ایگزاسٹ سے کالا دھواں نکل رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol3y", type="primary"):
        s.patient_data['black_smoke'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Black exhaust smoke: +10 risk|ایگزاسٹ سے کالا دھواں: +10 رسک|10")
        s.step = 'ol4'; st.rerun()
    if c2.button(NO, key="ol3n"): s.patient_data['black_smoke'] = "No"; s.step = 'ol4'; st.rerun()
elif step == 'ol4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Do you see oil spots or puddles under the car?', 'کیا گاڑی کے نیچے آئل کے دھبے یا چھینٹے نظر آتے ہیں؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol4y", type="primary"):
        s.patient_data['oil_leak'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Oil spots under the car: +15 risk|گاڑی کے نیچے آئل کے دھبے: +15 رسک|15")
        s.step = 'ol5'; st.rerun()
    if c2.button(NO, key="ol4n"): s.patient_data['oil_leak'] = "No"; s.step = 'ol5'; st.rerun()
elif step == 'ol5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Do you smell burning oil?', 'کیا جلتے ہوئے آئل کی بو آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol5y", type="primary"):
        s.patient_data['burning_oil_smell'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Burning oil smell: +15 risk|جلتے ہوئے آئل کی بو: +15 رسک|15")
        s.step = 'ol_oil'; st.rerun()
    if c2.button(NO, key="ol5n"): s.patient_data['burning_oil_smell'] = "No"; s.step = 'ol_oil'; st.rerun()
elif step == 'ol_oil':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the oil level from the dipstick as a percentage (normal 60 - 100 %)', '📄 ڈپ اسٹک سے آئل کی سطح فیصد میں درج کریں (نارمل 60 تا 100 فیصد)')))
    val = st.number_input((T('Oil level (%)', 'آئل کی سطح (فیصد)')), min_value=0, max_value=100, value=70, step=1, key="ol_oil_in")
    if st.button(SUBMIT, key="ol_oil_b", type="primary"):
        s.report_data['oil_level'] = val; s.step = 'ol6'
        if val < 15: s.risk = max(s.risk + 40, 70); s.reasons.append("Oil level critically low (" + str(val) + " %): +40 risk (EMERGENCY sign)|آئل کی سطح انتہائی کم (" + str(val) + " فیصد): +40 رسک (ایمرجنسی کی علامت)|40"); s.step = 'end'
        elif val < 30: s.risk = s.risk + 20; s.reasons.append("Oil level very low (" + str(val) + " %): +20 risk|آئل کی سطح بہت کم (" + str(val) + " فیصد): +20 رسک|20")
        elif val < 50: s.risk = s.risk + 10; s.reasons.append("Oil level low (" + str(val) + " %): +10 risk|آئل کی سطح کم (" + str(val) + " فیصد): +10 رسک|10")
        st.rerun()
elif step == 'ol6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Was the oil last changed more than 6 months or 5000 km ago?', 'کیا آئل آخری بار چھ ماہ یا 5000 کلومیٹر سے زیادہ پہلے تبدیل ہوا تھا؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ol6y", type="primary"):
        s.patient_data['oil_change_overdue'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Oil change overdue: +10 risk|آئل تبدیل کرنے کا وقت گزر چکا: +10 رسک|10")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ol6n"): s.patient_data['oil_change_overdue'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: AC not cooling ----------
elif step == 'ac1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Is the AC blowing warm or only slightly cool air?', 'کیا اے سی گرم یا ہلکی ٹھنڈی ہوا دے رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac1y", type="primary"):
        s.patient_data['ac_warm'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("AC blowing warm air: +10 risk|اے سی گرم ہوا دے رہا ہے: +10 رسک|10")
        s.step = 'ac2'; st.rerun()
    if c2.button(NO, key="ac1n"): s.patient_data['ac_warm'] = "No"; s.step = 'ac2'; st.rerun()
elif step == 'ac2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is the airflow weak even at the highest fan speed?', 'کیا پنکھے کی سب سے تیز رفتار پر بھی ہوا کم آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac2y", type="primary"):
        s.patient_data['weak_airflow'] = "Yes"; s.risk = s.risk + 5; s.reasons.append("Weak airflow (cabin filter may be blocked): +5 risk|ہوا کم آ رہی ہے (کیبن فلٹر بند ہو سکتا ہے): +5 رسک|5")
        s.step = 'ac3'; st.rerun()
    if c2.button(NO, key="ac2n"): s.patient_data['weak_airflow'] = "No"; s.step = 'ac3'; st.rerun()
elif step == 'ac3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Is there a musty or bad smell from the vents?', 'کیا ایئر وینٹس سے سیلن یا بدبو آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac3y", type="primary"):
        s.patient_data['vent_smell'] = "Yes"; s.risk = s.risk + 5; s.reasons.append("Bad smell from the vents: +5 risk|وینٹس سے بدبو: +5 رسک|5")
        s.step = 'ac4'; st.rerun()
    if c2.button(NO, key="ac3n"): s.patient_data['vent_smell'] = "No"; s.step = 'ac4'; st.rerun()
elif step == 'ac4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Do you hear a loud noise or clicking when the AC is on?', 'کیا اے سی چلانے پر تیز آواز یا ٹک ٹک سنائی دیتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac4y", type="primary"):
        s.patient_data['ac_noise'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Loud noise when AC is on: +10 risk|اے سی چلانے پر تیز آواز: +10 رسک|10")
        s.step = 'ac5'; st.rerun()
    if c2.button(NO, key="ac4n"): s.patient_data['ac_noise'] = "No"; s.step = 'ac5'; st.rerun()
elif step == 'ac5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Is water leaking inside the car (wet carpet)?', 'کیا گاڑی کے اندر پانی لیک ہو رہا ہے (گیلا قالین)؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac5y", type="primary"):
        s.patient_data['ac_water_leak'] = "Yes"; s.risk = s.risk + 5; s.reasons.append("Water leaking inside the car: +5 risk|گاڑی کے اندر پانی لیک: +5 رسک|5")
        s.step = 'ac_km'; st.rerun()
    if c2.button(NO, key="ac5n"): s.patient_data['ac_water_leak'] = "No"; s.step = 'ac_km'; st.rerun()
elif step == 'ac_km':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the kilometres driven since the last service (normal: below 10000 km)', '📄 پچھلی سروس کے بعد چلائے گئے کلومیٹر درج کریں (نارمل: 10000 سے کم)')))
    val = st.number_input((T('Km since last service', 'پچھلی سروس کے بعد کلومیٹر')), min_value=0, max_value=100000, value=5000, step=500, key="ac_km_in")
    if st.button(SUBMIT, key="ac_km_b", type="primary"):
        s.report_data['km_since_service'] = val; s.step = 'ac6'
        if val >= 20000: s.risk = s.risk + 20; s.reasons.append("Service overdue (" + str(val) + " km since last service): +20 risk|سروس کا وقت گزر چکا (" + str(val) + " کلومیٹر): +20 رسک|20")
        elif val >= 10000: s.risk = s.risk + 10; s.reasons.append("Service due soon (" + str(val) + " km since last service): +10 risk|سروس جلد درکار (" + str(val) + " کلومیٹر): +10 رسک|10")
        st.rerun()
elif step == 'ac6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Does the engine temperature rise when the AC is on?', 'کیا اے سی چلانے پر انجن کا درجہ حرارت بڑھ جاتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="ac6y", type="primary"):
        s.patient_data['ac_overheat'] = "Yes"; s.risk = s.risk + 20; s.reasons.append("Engine heats up when AC is on: +20 risk|اے سی چلانے پر انجن گرم ہو جاتا ہے: +20 رسک|20")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="ac6n"): s.patient_data['ac_overheat'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Steering problem ----------
elif step == 'sr1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Did the steering suddenly lock, or become impossible to control?', 'کیا اسٹیئرنگ اچانک جام ہو گیا یا قابو سے باہر ہو گیا؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr1y", type="primary"):
        s.patient_data['steering_lock'] = "Yes"; s.risk = max(s.risk + 50, 70); s.reasons.append("Steering suddenly locked / out of control: +50 risk (EMERGENCY sign)|اسٹیئرنگ اچانک جام / بے قابو: +50 رسک (ایمرجنسی کی علامت)|50")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="sr1n"): s.patient_data['steering_lock'] = "No"; s.step = 'sr2'; st.rerun()
elif step == 'sr2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is the steering wheel very heavy or hard to turn?', 'کیا اسٹیئرنگ بہت بھاری یا گھمانا مشکل ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr2y", type="primary"):
        s.patient_data['steering_heavy'] = "Yes"; s.risk = s.risk + 20; s.reasons.append("Heavy / hard steering: +20 risk|اسٹیئرنگ بھاری / سخت: +20 رسک|20")
        s.step = 'sr3'; st.rerun()
    if c2.button(NO, key="sr2n"): s.patient_data['steering_heavy'] = "No"; s.step = 'sr3'; st.rerun()
elif step == 'sr3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Does the car drift to one side on a straight road?', 'کیا سیدھی سڑک پر گاڑی ایک طرف بھٹکتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr3y", type="primary"):
        s.patient_data['steering_drift'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Car drifts to one side: +10 risk|گاڑی ایک طرف بھٹکتی ہے: +10 رسک|10")
        s.step = 'sr4'; st.rerun()
    if c2.button(NO, key="sr3n"): s.patient_data['steering_drift'] = "No"; s.step = 'sr4'; st.rerun()
elif step == 'sr4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Is there extra play (looseness) in the steering wheel?', 'کیا اسٹیئرنگ میں ضرورت سے زیادہ ڈھیلاپن ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr4y", type="primary"):
        s.patient_data['steering_play'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Loose steering: +15 risk|اسٹیئرنگ ڈھیلا ہے: +15 رسک|15")
        s.step = 'sr5'; st.rerun()
    if c2.button(NO, key="sr4n"): s.patient_data['steering_play'] = "No"; s.step = 'sr5'; st.rerun()
elif step == 'sr5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Do you hear a whining sound when turning the steering wheel?', 'کیا اسٹیئرنگ گھماتے وقت سیٹی جیسی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr5y", type="primary"):
        s.patient_data['steering_whine'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Whining sound when turning: +10 risk|اسٹیئرنگ گھماتے وقت سیٹی جیسی آواز: +10 رسک|10")
        s.step = 'sr_psi'; st.rerun()
    if c2.button(NO, key="sr5n"): s.patient_data['steering_whine'] = "No"; s.step = 'sr_psi'; st.rerun()
elif step == 'sr_psi':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the tyre pressure from a gauge (normal 30 - 35 PSI)', '📄 گیج سے ٹائر کا پریشر درج کریں (نارمل 30 تا 35 پی ایس آئی)')))
    val = st.number_input((T('Tyre pressure (PSI)', 'ٹائر کا پریشر (پی ایس آئی)')), min_value=0, max_value=80, value=32, step=1, key="sr_psi_in")
    if st.button(SUBMIT, key="sr_psi_b", type="primary"):
        s.report_data['tyre_pressure'] = val; s.step = 'sr6'
        if val < 20: s.risk = s.risk + 30; s.reasons.append("Tyre pressure very low (" + str(val) + " PSI): +30 risk|ٹائر کا پریشر بہت کم (" + str(val) + " پی ایس آئی): +30 رسک|30")
        elif val < 28: s.risk = s.risk + 15; s.reasons.append("Tyre pressure low (" + str(val) + " PSI): +15 risk|ٹائر کا پریشر کم (" + str(val) + " پی ایس آئی): +15 رسک|15")
        elif val > 40: s.risk = s.risk + 15; s.reasons.append("Tyre pressure too high (" + str(val) + " PSI): +15 risk|ٹائر کا پریشر بہت زیادہ (" + str(val) + " پی ایس آئی): +15 رسک|15")
        st.rerun()
elif step == 'sr6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Is the power steering fluid low, or is there a leak under the car?', 'کیا پاور اسٹیئرنگ فلوئڈ کم ہے یا گاڑی کے نیچے لیک ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="sr6y", type="primary"):
        s.patient_data['steering_fluid'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Steering fluid low / leak: +15 risk|اسٹیئرنگ فلوئڈ کم / لیک: +15 رسک|15")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="sr6n"): s.patient_data['steering_fluid'] = "No"; s.step = 'end'; st.rerun()

# ---------- PROBLEM: Gear or clutch problem ----------
elif step == 'gc1':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "1 / 6</span><div class='qbar'><span style='width:14%'></span></div></div><div class='qtext'>" + (T('Does the gear slip or pop out by itself?', 'کیا گیئر خود بخود پھسل جاتا ہے یا نکل جاتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc1y", type="primary"):
        s.patient_data['gear_slip'] = "Yes"; s.risk = s.risk + 20; s.reasons.append("Gear slipping / popping out: +20 risk|گیئر پھسلتا / نکل جاتا ہے: +20 رسک|20")
        s.step = 'gc2'; st.rerun()
    if c2.button(NO, key="gc1n"): s.patient_data['gear_slip'] = "No"; s.step = 'gc2'; st.rerun()
elif step == 'gc2':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "2 / 6</span><div class='qbar'><span style='width:29%'></span></div></div><div class='qtext'>" + (T('Is it hard to shift gears, or do you hear grinding while shifting?', 'کیا گیئر بدلنا مشکل ہے یا بدلتے وقت رگڑنے کی آواز آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc2y", type="primary"):
        s.patient_data['hard_shift'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Hard shifting / grinding: +15 risk|گیئر بدلنے میں مشکل / رگڑ کی آواز: +15 رسک|15")
        s.step = 'gc3'; st.rerun()
    if c2.button(NO, key="gc2n"): s.patient_data['hard_shift'] = "No"; s.step = 'gc3'; st.rerun()
elif step == 'gc3':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "3 / 6</span><div class='qbar'><span style='width:43%'></span></div></div><div class='qtext'>" + (T('Does the clutch pedal feel soft, stuck or too high?', 'کیا کلچ پیڈل نرم، پھنسا ہوا یا بہت اونچا محسوس ہوتا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc3y", type="primary"):
        s.patient_data['clutch_feel'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Clutch pedal feels wrong: +10 risk|کلچ پیڈل میں خرابی محسوس ہوتی ہے: +10 رسک|10")
        s.step = 'gc4'; st.rerun()
    if c2.button(NO, key="gc3n"): s.patient_data['clutch_feel'] = "No"; s.step = 'gc4'; st.rerun()
elif step == 'gc4':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "4 / 6</span><div class='qbar'><span style='width:57%'></span></div></div><div class='qtext'>" + (T('Do you smell burning when driving uphill or in traffic?', 'کیا چڑھائی یا ٹریفک میں چلاتے وقت جلنے کی بو آتی ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc4y", type="primary"):
        s.patient_data['clutch_burning'] = "Yes"; s.risk = s.risk + 10; s.reasons.append("Burning smell (clutch may be overheating): +10 risk|جلنے کی بو (کلچ گرم ہو سکتا ہے): +10 رسک|10")
        s.step = 'gc5'; st.rerun()
    if c2.button(NO, key="gc4n"): s.patient_data['clutch_burning'] = "No"; s.step = 'gc5'; st.rerun()
elif step == 'gc5':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "5 / 6</span><div class='qbar'><span style='width:71%'></span></div></div><div class='qtext'>" + (T('Does the engine rev high but the car does not speed up?', 'کیا انجن کی آواز تیز ہو جاتی ہے مگر گاڑی کی رفتار نہیں بڑھتی؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc5y", type="primary"):
        s.patient_data['revs_no_speed'] = "Yes"; s.risk = s.risk + 25; s.reasons.append("Engine revs high but car does not speed up: +25 risk|انجن تیز چلتا ہے مگر رفتار نہیں بڑھتی: +25 رسک|25")
        s.step = 'gc_km'; st.rerun()
    if c2.button(NO, key="gc5n"): s.patient_data['revs_no_speed'] = "No"; s.step = 'gc_km'; st.rerun()
elif step == 'gc_km':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + RPT + "</span><div class='qbar'><span style='width:86%'></span></div></div></div>", unsafe_allow_html=True)
    st.info((T('📄 Enter the kilometres driven since the last service (normal: below 10000 km)', '📄 پچھلی سروس کے بعد چلائے گئے کلومیٹر درج کریں (نارمل: 10000 سے کم)')))
    val = st.number_input((T('Km since last service', 'پچھلی سروس کے بعد کلومیٹر')), min_value=0, max_value=100000, value=5000, step=500, key="gc_km_in")
    if st.button(SUBMIT, key="gc_km_b", type="primary"):
        s.report_data['km_since_service'] = val; s.step = 'gc6'
        if val >= 20000: s.risk = s.risk + 20; s.reasons.append("Service overdue (" + str(val) + " km since last service): +20 risk|سروس کا وقت گزر چکا (" + str(val) + " کلومیٹر): +20 رسک|20")
        elif val >= 10000: s.risk = s.risk + 10; s.reasons.append("Service due soon (" + str(val) + " km since last service): +10 risk|سروس جلد درکار (" + str(val) + " کلومیٹر): +10 رسک|10")
        st.rerun()
elif step == 'gc6':
    st.markdown("<div class='qcard'><div class='qtop'><span class='qno'>" + QN + "6 / 6</span><div class='qbar'><span style='width:100%'></span></div></div><div class='qtext'>" + (T('Do you see red or brown fluid leaking under the car?', 'کیا گاڑی کے نیچے سے سرخ یا بھورا سیال لیک ہو رہا ہے؟')) + "</div></div>", unsafe_allow_html=True); c1, c2 = st.columns(2)
    if c1.button(YES, key="gc6y", type="primary"):
        s.patient_data['gearbox_leak'] = "Yes"; s.risk = s.risk + 15; s.reasons.append("Red / brown fluid leak: +15 risk|سرخ / بھورے سیال کا لیک: +15 رسک|15")
        s.step = 'end'; st.rerun()
    if c2.button(NO, key="gc6n"): s.patient_data['gearbox_leak'] = "No"; s.step = 'end'; st.rerun()

# ================== FINAL STEP : DECISION + DEFENCE + SUPPORT ==================
elif step == 'end':
    if s.risk > 100: s.risk = 100
    st.write(T('### 📋 Final Result (Decision Support)', '### 📋 حتمی نتیجہ (فیصلہ سازی میں مدد)'))
    # ---- 1) DECISION MAKING: the urgency level is decided from the risk score ----
    if s.risk >= 70:
        lvl = "emergency"; urg_en = "EMERGENCY"; urg_ur = "ایمرجنسی"; lo_t = 70; hi_t = 100
        st.error(T('🚨 EMERGENCY: Stop the car safely and call a tow truck!', '🚨 ایمرجنسی: گاڑی کو محفوظ طریقے سے روکیں اور ٹو ٹرک بلائیں!'))
        sug_en = "Stop the car in a safe place and call a tow truck. Please get it checked by a qualified mechanic before driving again."
        sug_ur = "گاڑی کو محفوظ جگہ پر روکیں اور ٹو ٹرک بلائیں۔ دوبارہ چلانے سے پہلے کسی مستند مکینک سے چیک کروائیں۔"
        drive_en = "🚫 DO NOT DRIVE the car. Stop in a safe place and call a tow truck."
        drive_ur = "🚫 گاڑی نہ چلائیں۔ محفوظ جگہ پر رکیں اور ٹو ٹرک بلائیں۔"
        plan1 = T('Switch on the hazard lights, slow down and stop in a safe place away from traffic.', 'ہیزرڈ لائٹس آن کریں، رفتار کم کریں اور ٹریفک سے دور محفوظ جگہ پر گاڑی روک دیں۔')
        plan2 = T('Switch off the engine and do not drive the car again.', 'انجن بند کر دیں اور گاڑی دوبارہ نہ چلائیں۔')
        plan3 = T('Call a tow truck or roadside help and show the mechanic report below.', 'ٹو ٹرک یا روڈ سائیڈ مدد کو بلائیں اور نیچے دی گئی مکینک رپورٹ دکھائیں۔')
    elif s.risk >= 40:
        lvl = "urgent"; urg_en = "URGENT"; urg_ur = "فوری"; lo_t = 40; hi_t = 70
        st.warning(T('⚠️ URGENT: See a mechanic today', '⚠️ فوری: آج ہی مکینک کو دکھائیں'))
        sug_en = "Please see a qualified mechanic today. Avoid long drives until it is checked."
        sug_ur = "براہ کرم آج ہی کسی مستند مکینک کو دکھائیں۔ چیک ہونے تک لمبے سفر سے پرہیز کریں۔"
        drive_en = "⚠️ Avoid driving. If you must, drive slowly and directly to a mechanic, away from highways."
        drive_ur = "⚠️ گاڑی چلانے سے پرہیز کریں۔ مجبوری ہو تو ہائی وے سے دور رہ کر آہستہ اور سیدھا مکینک تک جائیں۔"
        plan1 = T('Avoid highways, high speed and long trips.', 'ہائی وے، تیز رفتاری اور لمبے سفر سے بچیں۔')
        plan2 = T('Go to a qualified mechanic today.', 'آج ہی کسی مستند مکینک کے پاس جائیں۔')
        plan3 = T('Show the mechanic report below so the check is faster.', 'نیچے دی گئی مکینک رپورٹ دکھائیں تاکہ چیکنگ جلدی ہو۔')
    elif s.risk >= 20:
        lvl = "routine"; urg_en = "ROUTINE"; urg_ur = "معمول"; lo_t = 20; hi_t = 40
        st.info(T('📅 ROUTINE: Book a service this week', '📅 معمول: اس ہفتے سروس بُک کروائیں'))
        sug_en = "Book a service this week and ask a qualified mechanic to check the car."
        sug_ur = "اس ہفتے سروس بُک کروائیں اور کسی مستند مکینک سے گاڑی چیک کروائیں۔"
        drive_en = "🟡 It looks fine to drive carefully until the service. Do not ignore new warning lights or noises."
        drive_ur = "🟡 سروس تک احتیاط سے گاڑی چلانا ٹھیک لگتا ہے۔ نئی وارننگ لائٹس یا آوازوں کو نظر انداز نہ کریں۔"
        plan1 = T('Book a service this week.', 'اس ہفتے سروس بُک کروائیں۔')
        plan2 = T('Watch for new warning lights, noises or smells.', 'نئی وارننگ لائٹس، آوازوں یا بو پر نظر رکھیں۔')
        plan3 = T('Show the mechanic report below at the service.', 'سروس کے وقت نیچے دی گئی مکینک رپورٹ دکھائیں۔')
    else:
        lvl = "selfcare"; urg_en = "SELF-CARE"; urg_ur = "خود نگہداشت"; lo_t = 0; hi_t = 20
        st.success(T('🏠 SELF-CARE: Simple fix you can do yourself', '🏠 خود نگہداشت: آسان مسئلہ جو آپ خود حل کر سکتے ہیں'))
        sug_en = "This looks minor. Do the simple checks yourself (fuel, tyre air, fluids) and see a qualified mechanic if the problem continues."
        sug_ur = "یہ معمولی لگتا ہے۔ آسان چیکس خود کریں (فیول، ٹائر کی ہوا، فلوئڈز) اور مسئلہ جاری رہے تو مستند مکینک سے رجوع کریں۔"
        drive_en = "🟢 It looks fine to drive carefully. Do the simple checks and keep watching the car."
        drive_ur = "🟢 احتیاط سے گاڑی چلانا ٹھیک لگتا ہے۔ آسان چیکس کریں اور گاڑی پر نظر رکھیں۔"
        plan1 = T('Check fuel, tyre air, fluid levels and battery terminals yourself.', 'فیول، ٹائر کی ہوا، فلوئڈ کی سطح اور بیٹری ٹرمینل خود چیک کریں۔')
        plan2 = T('Watch whether the problem comes back.', 'دیکھیں کہ مسئلہ دوبارہ تو نہیں آتا۔')
        plan3 = T('See a qualified mechanic if it continues.', 'مسئلہ جاری رہے تو مستند مکینک سے رجوع کریں۔')
    # ---- 2) SUGGESTION + possible area + DRIVE-OR-STOP decision ----
    ap = s.area.split("|")   # possible area to check (English | Urdu)
    area_txt = ap[1] if (L == 'ur' and len(ap) > 1) else ap[0]
    sug = sug_en if L == 'en' else sug_ur
    urg = urg_en if L == 'en' else urg_ur
    drive = drive_en if L == 'en' else drive_ur
    st.info("💡 " + sug)
    st.write((T('🔍 Possible area to check: ', '🔍 چیک کرنے کا ممکنہ حصہ: ')) + area_txt)
    st.markdown("<div class='drive v-" + lvl + "'>" + (T('🚦 Can I drive? ', '🚦 کیا میں گاڑی چلا سکتا ہوں؟ ')) + drive + "</div>", unsafe_allow_html=True)
    st.write((T('Risk Score: ', 'رسک اسکور: ')) + str(s.risk) + "/100"); st.progress(s.risk)
    st.markdown("<div class='meter'><div class='sg s1'></div><div class='sg s2'></div><div class='sg s3'></div><div class='sg s4'></div><div class='pointer' style='--p:" + str(s.risk) + "%'><span>" + str(s.risk) + "</span></div></div>"
                + (T("<div class='legend'><span style='--c:#22C55E'>SELF-CARE 0-19</span><span style='--c:#F4C430'>ROUTINE 20-39</span><span style='--c:#F08A24'>URGENT 40-69</span><span style='--c:#D62828'>EMERGENCY 70-100</span></div>", "<div class='legend'><span style='--c:#22C55E'>خود نگہداشت 0-19</span><span style='--c:#F4C430'>معمول 20-39</span><span style='--c:#F08A24'>فوری 40-69</span><span style='--c:#D62828'>ایمرجنسی 70-100</span></div>")), unsafe_allow_html=True)
    # mechanic handover report (a text file the owner can download and show to the mechanic)
    hr = (T('CAR CHECK REPORT (decision support - NOT a diagnosis)', 'گاڑی کی چیکنگ رپورٹ (فیصلہ سازی میں مدد - تشخیص نہیں)')) + "\n"
    hr = hr + (T('Date: ', 'تاریخ: ')) + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
    hr = hr + (T('Possible area to check: ', 'چیک کرنے کا ممکنہ حصہ: ')) + area_txt + "\n"
    hr = hr + (T('Urgency: ', 'فوری سطح: ')) + urg + "   " + (T('Risk score: ', 'رسک اسکور: ')) + str(s.risk) + "/100\n"
    hr = hr + (T('Drive decision: ', 'گاڑی چلانے کا فیصلہ: ')) + drive + "\n\n"
    hr = hr + (T('Reasons:', 'وجوہات:')) + "\n"
    # ---- 3) WHY THIS DECISION: every reason with its risk points ----
    st.write(T('**🧠 Why this decision?**', '**🧠 یہ فیصلہ کیوں؟**'))
    sum_pts = 0; top_pts = 0; top_en = ""; top_ur = ""
    if len(s.reasons) == 0: st.write(T('• No major red flags found from your answers.', '• آپ کے جوابات سے کوئی بڑی خطرے کی علامت نہیں ملی۔'))
    for r in s.reasons:
        parts = r.split("|"); pts = int(parts[2]); sum_pts = sum_pts + pts
        if pts > top_pts: top_pts = pts; top_en = parts[0]; top_ur = parts[1]
        rt = parts[1] if L == 'ur' else parts[0]
        st.write("• " + rt); hr = hr + "- " + rt + "\n"
    # ---- 4) DEFENDING THE SUGGESTION (explainability) ----
    st.write(T('**🛡️ Defending this suggestion**', '**🛡️ اس مشورے کی وضاحت اور دفاع**'))
    yes_n = 0
    for k in s.patient_data:
        if s.patient_data[k] == "Yes": yes_n = yes_n + 1
    total_q = len(s.patient_data) - 1
    if top_pts > 0:
        share = (100 * top_pts) // s.risk
        st.write(T("• Strongest factor: " + top_en + " (" + str(share) + "% of your " + str(s.risk) + "-point risk score).",
                   "• سب سے مضبوط وجہ: " + top_ur + " (آپ کے " + str(s.risk) + " پوائنٹ کے رسک اسکور کا " + str(share) + " فیصد)۔"))
    else:
        st.write(T('• No single strong factor: your answers added few or no risk points.', '• کوئی ایک مضبوط وجہ نہیں: آپ کے جوابات سے بہت کم یا کوئی رسک پوائنٹس نہیں بنے۔'))
    if s.risk > sum_pts:
        st.write(T("• Safety minimum: serious warning signs added " + str(s.risk - sum_pts) + " extra point(s), so the score is never too low for a risky situation.",
                   "• حفاظتی کم از کم حد: خطرناک علامات کی وجہ سے " + str(s.risk - sum_pts) + " اضافی پوائنٹ شامل ہوئے تاکہ خطرناک صورتحال میں اسکور کبھی کم نہ رہے۔"))
    st.write(T("• Warning signs reported: " + str(yes_n) + " of " + str(total_q) + " questions were answered Yes.",
               "• رپورٹ کی گئی علامات: " + str(total_q) + " میں سے " + str(yes_n) + " سوالوں کا جواب جی ہاں تھا۔"))
    if s.risk >= 70:
        st.write(T('• Why the highest level? The score reached 70 or an emergency warning sign was reported, so safety comes first.', '• سب سے اونچی سطح کیوں؟ اسکور 70 تک پہنچ گیا یا ایمرجنسی کی علامت ملی، اس لیے حفاظت سب سے پہلے ہے۔'))
    else:
        st.write(T("• Why not a higher level? The score (" + str(s.risk) + ") is " + str(hi_t - s.risk) + " point(s) below " + str(hi_t) + ", and no emergency warning sign was answered Yes.",
                   "• اونچی سطح کیوں نہیں؟ اسکور (" + str(s.risk) + ") حد " + str(hi_t) + " سے " + str(hi_t - s.risk) + " پوائنٹ کم ہے اور کسی ایمرجنسی علامت کا جواب جی ہاں نہیں تھا۔"))
    if urg_en != "SELF-CARE":
        st.write(T("• Why not a lower level? The score (" + str(s.risk) + ") is at or above " + str(lo_t) + ". It would need to fall by " + str(s.risk - lo_t + 1) + " point(s) to move down.",
                   "• نچلی سطح کیوں نہیں؟ اسکور (" + str(s.risk) + ") حد " + str(lo_t) + " یا اس سے اوپر ہے۔ نیچے آنے کے لیے اسے " + str(s.risk - lo_t + 1) + " پوائنٹ کم ہونا ہوگا۔"))
    else:
        st.write(T('• This is already the lowest level.', '• یہ پہلے ہی سب سے نچلی سطح ہے۔'))
    border = False   # confidence: is the score close to a level boundary?
    if urg_en != "EMERGENCY" and hi_t - s.risk <= 5: border = True
    if urg_en != "EMERGENCY" and urg_en != "SELF-CARE" and s.risk - lo_t < 5: border = True
    if border:
        st.write(T('• Confidence: BORDERLINE - the score is close to a level boundary, so please follow the more careful advice if you are unsure.', '• اعتماد: سرحدی کیس - اسکور سطح کی حد کے قریب ہے، اس لیے شک ہو تو زیادہ احتیاط والا مشورہ مانیں۔'))
    else:
        st.write(T('• Confidence: CLEAR - the score is well inside this level.', '• اعتماد: واضح - اسکور اس سطح کے اندر کافی دور ہے۔'))
    # ---- 5) DECISION SUPPORT: what to do now ----
    st.write(T('**✅ What to do now**', '**✅ اب کیا کریں**'))
    st.markdown("<div class='stepc'><b>1</b><span>" + plan1 + "</span></div><div class='stepc' style='animation-delay:.12s'><b>2</b><span>" + plan2 + "</span></div><div class='stepc' style='animation-delay:.24s'><b>3</b><span>" + plan3 + "</span></div>", unsafe_allow_html=True)
    if len(s.report_data) > 0:
        st.write(T('**🗂️ Your report values**', '**🗂️ آپ کی درج کردہ رپورٹ قدریں**'))
        hr = hr + "\n" + (T('Report values entered:', 'درج کی گئی رپورٹ قدریں:')) + "\n"
    for k in s.report_data:
        if k == 'battery_voltage': nm = T('Battery voltage (V)', 'بیٹری وولٹیج (وولٹ)')
        elif k == 'engine_temp': nm = T('Engine temperature', 'انجن کا درجہ حرارت')
        elif k == 'tyre_pressure': nm = T('Tyre pressure (PSI)', 'ٹائر کا پریشر (پی ایس آئی)')
        elif k == 'oil_level': nm = T('Oil level (%)', 'آئل کی سطح (فیصد)')
        else: nm = T('Km since last service', 'پچھلی سروس کے بعد کلومیٹر')
        st.write("• " + nm + ": " + str(s.report_data[k])); hr = hr + "- " + nm + ": " + str(s.report_data[k]) + "\n"
    hr = hr + "\n" + (T('Note: this report is decision support only. Please ask a qualified mechanic to confirm.', 'نوٹ: یہ رپورٹ صرف فیصلہ سازی میں مدد کے لیے ہے۔ براہ کرم مستند مکینک سے تصدیق کروائیں۔')) + "\n"
    st.download_button(T('📄 Download Mechanic Report', '📄 مکینک رپورٹ ڈاؤن لوڈ کریں'), data=hr, file_name="mechanic_report.txt", mime="text/plain", key="dl")
    st.write(T('This is NOT a final diagnosis. Always get the car checked by a qualified mechanic.', 'یہ حتمی تشخیص نہیں ہے۔ گاڑی ہمیشہ کسی مستند مکینک سے چیک کروائیں۔'))
    if lvl == "selfcare" and s.balloons_done == False:   # small celebration, once per consultation
        st.balloons(); s.balloons_done = True
    if st.button(NEW, key="new", type="primary"):
        reset_system(); st.rerun()
else:
    s.step = 'start'; st.rerun()

# Total if/else count: 273  (if + elif + else statements)
# Total questions: 70  (60 Yes/No symptom questions + 10 report inputs; 10 car problems)
