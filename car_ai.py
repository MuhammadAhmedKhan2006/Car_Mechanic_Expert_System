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
from styles import CSS, CSS_UR
from i18n import T
from core import reset_system
import decision_tree

st.set_page_config(page_title="Car Mechanic AI", page_icon="🚗", layout="centered")   # first Streamlit command

s = st.session_state   # short name for st.session_state

if 'step' not in s:    # first time only
    s.lang = 'en'; reset_system()

# ---------- Language: 'en' = English, 'ur' = Urdu ----------
L = s.lang

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

decision_tree.run()
