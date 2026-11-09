# -*- coding: utf-8 -*-
# app.py - Streamlit user interface for the Vehicle Diagnosis DSS
#
# The UI only draws what api.py returns. Decision-making lives in api.py
# and knowledge_base/. Themes: dark (black/red) and light, toggled by a button.
# Languages: English / Urdu, toggled by a button.

import streamlit as st
from datetime import datetime
import api

st.set_page_config(page_title="Vehicle Diagnosis DSS", page_icon="car", layout="centered")
s = st.session_state

# ------------------------------------------------------------------
# Themes (CSS injected once per run, chosen by s.theme)
# ------------------------------------------------------------------
DARK_CSS = """
<style>
:root { --bg:#0d0d0f; --card:#1a1a1d; --card2:#222226; --line:#2c2c31; --txt:#f2f2f2;
        --mut:#9a9aa3; --red:#e63946; --red2:#ff4d5e; }
.stApp { background: var(--bg) !important; color: var(--txt); }
.block-container { max-width: 860px; padding-top: 1.4rem; }
h1,h2,h3,h4,p,span,div,label { color: var(--txt); }
[data-testid="stSidebar"] { background:#111114 !important; }
.qcard,.mcard,.rcard { background:var(--card); border:1px solid var(--line); border-radius:14px;
        padding:16px 18px; margin:10px 0; }
.mcard:hover { border-color:var(--red); }
.mcard h3 { margin-top:0; }
h1,h2,h3,h4 { border-bottom:3px solid var(--red); padding-bottom:6px; display:inline-block; }
.sub { color:var(--mut); }
hr { border-color:var(--line); }
.stButton>button, [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {
        background:var(--card2) !important; color:var(--txt) !important;
        border:1px solid var(--line) !important; border-radius:10px !important;
        font-weight:600; min-height:2.9rem; }
.stButton>button:hover, [data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
        border-color:var(--red) !important; box-shadow:0 0 0 1px var(--red), 0 4px 14px rgba(230,57,70,.25) !important;
        color:var(--txt) !important; }
[data-testid="stProgress"]>div>div { background:var(--red); }
.stInfo,.stWarning,.stError,.stSuccess { border-radius:12px; }
.prog { height:8px; background:var(--card2); border-radius:6px; overflow:hidden; }
.prog>div { height:8px; background:var(--red); }
.pill { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.8rem;
        background:var(--card2); border:1px solid var(--line); }
.pill.urgent { background:var(--red); color:#fff; }
@media (max-width:640px){
  .block-container {padding:.8rem .7rem 3rem;}
  [data-testid="stHorizontalBlock"] {flex-direction:column !important; align-items:stretch !important;}
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"],
  [data-testid="stHorizontalBlock"] [data-testid="column"] {width:100% !important; min-width:0 !important;}
  .stButton>button {min-height:3rem; font-size:.95rem;}
}
</style>"""

LIGHT_CSS = """
<style>
:root { --bg:#f6f6f7; --card:#ffffff; --card2:#ececee; --line:#dcdce0; --txt:#1c1c1e;
        --mut:#6b6b70; --red:#d62828; --red2:#e63946; }
.stApp { background: var(--bg) !important; color: var(--txt); }
.block-container { max-width: 860px; padding-top: 1.4rem; }
h1,h2,h3,h4,p,span,div,label { color: var(--txt); }
[data-testid="stSidebar"] { background:#ffffff !important; }
.qcard,.mcard,.rcard { background:var(--card); border:1px solid var(--line); border-radius:14px;
        padding:16px 18px; margin:10px 0; box-shadow:0 2px 8px rgba(0,0,0,.05); }
.mcard:hover { border-color:var(--red); }
.mcard h3 { margin-top:0; }
h1,h2,h3,h4 { border-bottom:3px solid var(--red); padding-bottom:6px; display:inline-block; }
.sub { color:var(--mut); }
hr { border-color:var(--line); }
.stButton>button, [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {
        background:var(--card2) !important; color:var(--txt) !important;
        border:1px solid var(--line) !important; border-radius:10px !important;
        font-weight:600; min-height:2.9rem; }
.stButton>button:hover, [data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
        border-color:var(--red) !important; box-shadow:0 0 0 1px var(--red), 0 4px 14px rgba(214,40,40,.18) !important;
        color:var(--txt) !important; }
[data-testid="stProgress"]>div>div { background:var(--red); }
.prog { height:8px; background:var(--card2); border-radius:6px; overflow:hidden; }
.prog>div { height:8px; background:var(--red); }
.pill { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.8rem;
        background:var(--card2); border:1px solid var(--line); }
.pill.urgent { background:var(--red); color:#fff; }
@media (max-width:640px){
  .block-container {padding:.8rem .7rem 3rem;}
  [data-testid="stHorizontalBlock"] {flex-direction:column !important; align-items:stretch !important;}
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"],
  [data-testid="stHorizontalBlock"] [data-testid="column"] {width:100% !important; min-width:0 !important;}
  .stButton>button {min-height:3rem; font-size:.95rem;}
}
</style>"""

# ------------------------------------------------------------------
# session + language state
# ------------------------------------------------------------------
if "sess" not in s:
    s.sess = None
if "lang" not in s:
    s.lang = "en"
if "theme" not in s:
    s.theme = "dark"

L = s.lang

def T(en, ur):
    return en if L == "en" else ur

st.markdown(DARK_CSS if s.theme == "dark" else LIGHT_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# header: title + theme toggle + language toggle
# ------------------------------------------------------------------
st.title(T("Vehicle Diagnosis System", "گاڑی کی تشخیص کا نظام"))
st.markdown("<div class='sub'>" + T("Decision Support System - answer a few questions and get an explained, evidence-based result.",
                                  "فیصلہ سازی میں مدد کا نظام - چند سوالوں کے جواب دیں اور وضاحت کے ساتھ نتیجہ پائیں۔") + "</div>",
            unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button(T("Light theme", "ہلکا تھیم") if s.theme == "dark" else T("Dark theme", "گہرا تھیم"),
                 key="theme_btn", use_container_width=True):
        s.theme = "light" if s.theme == "dark" else "dark"
        st.rerun()
with c3:
    if st.button(T("اردو", "English"), key="lang_btn", use_container_width=True):
        s.lang = "ur" if L == "en" else "en"
        st.rerun()

st.write(T("Questions in bank: ", "مجموع سوالات: ") + str(api.total_questions()) +
         " | " + T("Decision branches: ", "فیصلہ کاری شاخیں: ") + str(api.count_branches()))

# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------
def qtext(q):
    return q.get("en" if L == "en" else "ur", q.get("en", ""))

def progress_html(sess, total_hint):
    done = len(sess["answers"])
    pct = min(100, int(100 * done / max(1, total_hint)))
    return ("<div class='sub'>" + T("Progress: ", "پیش رفت: ") + str(done) + "/" + str(total_hint) +
            "</div><div class='prog'><div style='width:" + str(pct) + "%'></div></div>")

def render_question(sess, q):
    # Draw one question with the right controls for its kind.
    is_report = q.get("kind") == "number"
    if is_report:
        st.markdown("<div class='qcard'><div class='qtext'>" + qtext(q) + "</div></div>", unsafe_allow_html=True)
        val = st.number_input(qtext(q), min_value=q["min"], max_value=q["max"],
                              value=(q["min"] + q["max"]) / 2, step=q["step"], format=q["fmt"], key="num_" + q["id"])
        if st.button(T("Submit", "جمع کریں"), type="primary", key="sub_" + q["id"], use_container_width=True):
            api.submit_answer(sess, q["id"], val)
            st.rerun()
    else:
        st.markdown("<div class='qcard'><div class='qtext'>" + qtext(q) + "</div></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button(T("Yes", "ہاں"), key="y_" + q["id"], type="primary", use_container_width=True):
            api.submit_answer(sess, q["id"], "yes"); st.rerun()
        if c2.button(T("No", "نہیں"), key="n_" + q["id"], use_container_width=True):
            api.submit_answer(sess, q["id"], "no"); st.rerun()
        if c3.button(T("Not sure", "یقین نہیں"), key="u_" + q["id"], use_container_width=True):
            api.submit_answer(sess, q["id"], "not_sure"); st.rerun()
    # Back button
    if sess["order"]:
        if st.button(T("Back", "پیچھے"), key="back_" + str(len(sess["order"])), use_container_width=True):
            api.go_back(sess); st.rerun()

def build_report_text(res):
    # Plain-text diagnosis report the user can download and show to a mechanic
    en = L == "en"
    lines = []
    lines.append("VEHICLE DIAGNOSIS REPORT" if en else "گاڑی کی تشخیص رپورٹ")
    lines.append("=" * 46)
    lines.append(("Date: " if en else "تاریخ: ") + datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append(("Mode: " if en else "طریقہ: ") + str(res.get("mode", "-")))
    lines.append("")
    lines.append(("Most likely problem: " if en else "سب سے ممکنہ مسئلہ: ") +
                 res["problem_en" if en else "problem_ur"])
    lines.append(res["simple_en" if en else "simple_ur"])
    lines.append(("Priority: " if en else "ترجیحی سطح: ") + res["priority"].upper())
    lines.append("")
    lines.append("EVIDENCE / supporting answers:")
    for ev in res["evidence"]:
        mark = "YES" if ev["value"] == "yes" else ("not sure" if ev["value"] == "not_sure" else ev["value"])
        lines.append("  - [" + mark + "] " + ev["en" if en else "ur"])
    lines.append("")
    if res["alternatives"]:
        lines.append("ALTERNATIVE POSSIBILITIES:")
        for a in res["alternatives"]:
            lines.append("  - " + a["en" if en else "ur"] + ": " + a["simple_en" if en else "simple_ur"])
        lines.append("")
    lines.append("RECOMMENDED ACTIONS:")
    for r in res["recommendations"]:
        lines.append("  - " + r["en" if en else "ur"])
        lines.append("    why: " + (r["why_en" if en else "why_ur"]))
    lines.append("")
    if res.get("urgent_warning"):
        lines.append(res["urgent_warning"]["en" if en else "ur"])
        lines.append("")
    d = res["disclaimer"]
    lines.append(d["en" if en else "ur"])
    return "\n".join(lines)

def render_result(sess):
    res = sess["result"] or api.build_result(sess)
    if not res.get("enough"):
        st.warning(res.get("en" if L == "en" else "ur", ""))
    else:
        pr = res["priority"]
        pr_label = {"low": T("Low priority", "کم ترجیحی"), "medium": T("Medium priority", "درمیانی ترجیحی"),
                    "high": T("High priority", "زیادہ ترجیحی"), "urgent": T("Urgent / safety critical", "فوری / حفاظتی-critical")}[pr]
        if res["critical"] or pr == "urgent":
            st.markdown("<div class='pill urgent'>" + pr_label + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='pill'>" + pr_label + "</div>", unsafe_allow_html=True)
        if res.get("urgent_warning"):
            st.error(res["urgent_warning"]["en" if L == "en" else "ur"])
        st.markdown("<div class='rcard'><h3>" + T("Most likely problem", "سب سے ممکنہ مسئلہ") + "</h3>"
                    "<p><b>" + res["problem_en" if L == "en" else "problem_ur"] + "</b></p>"
                    "<p>" + res["simple_en" if L == "en" else "simple_ur"] + "</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='rcard'><h3>" + T("Supporting evidence", "معاون شواہد") + "</h3>", unsafe_allow_html=True)
        yes_n = 0
        for ev in res["evidence"]:
            if ev["value"] == "yes":
                yes_n += 1
                st.write("- " + ev["en" if L == "en" else "ur"])
            elif ev["value"] == "not_sure":
                st.write("- (" + T("not sure", "یقین نہیں") + ") " + ev["en" if L == "en" else "ur"])
        if yes_n == 0:
            st.write(T("No symptom was fully confirmed - the result is based on partial signs only.",
                       "کوئی علامت مکمل طور پر تصدیق نہیں ہوئی - نتیجہ جزوی علامات پر مبنی ہے۔"))
        if res["alternatives"]:
            st.markdown("<div class='rcard'><h3>" + T("Alternative possibilities", "متبادل امکانات") + "</h3>", unsafe_allow_html=True)
            for a in res["alternatives"]:
                st.write("- **" + a["en" if L == "en" else "ur"] + "** - " +
                         a["simple_en" if L == "en" else "simple_ur"])
            st.caption(T("These are possibilities, not confirmed diagnoses.", "یہ امکانات ہیں، تصدیق شدہ تشخیص نہیں۔"))
        st.markdown("<div class='rcard'><h3>" + T("Recommended actions", "تجویز کردہ اقدامات") + "</h3>", unsafe_allow_html=True)
        for r in res["recommendations"]:
            st.write("- " + r["en" if L == "en" else "ur"])
            st.caption(("  " + T("Why: ", "کیوں: ") + (r["why_en" if L == "en" else "why_ur"])))
        st.warning(res["disclaimer"]["en" if L == "en" else "ur"])
        # ---- downloadable report ----
        st.download_button(T("Download diagnosis report", "تشخیص کی رپورٹ ڈاؤن لوڈ کریں"),
                           data=build_report_text(res), file_name="diagnosis_report.txt",
                           mime="text/plain", key="dl_report", use_container_width=True)
    if st.button(T("Start a new diagnosis", "نئی تشخیص شروع کریں"), type="primary", use_container_width=True):
        s.sess = None
        st.rerun()

# ------------------------------------------------------------------
# main flow
# ------------------------------------------------------------------
if s.sess is None:
    # ---------- START SCREEN: two diagnosis modes ----------
    st.markdown("<div class='sub'>" + T("How would you like to start?", "کیسے شروع کرنا چاہتے ہیں؟") + "</div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("<div class='mcard'><h3>" + T("I have an idea about the problem", "مجھے مسئلے کا اندازہ ہے") + "</h3>"
                    "<p>" + T("Pick your suspected problem from a list, answer a few targeted questions, and get a decision with evidence.",
                              "فہرست سے اپنا اندازہ مسئلہ منتخب کریں، چند سوالات کے جواب دیں اور شواہد کے ساتھ نتیجہ پائیں۔") + "</p></div>",
                    unsafe_allow_html=True)
        if st.button(T("Start guided diagnosis", "تشخیص شروع کریں"), key="mode_direct", use_container_width=True):
            s.sess = api.new_session("direct", L)
            st.rerun()
    with m2:
        st.markdown("<div class='mcard'><h3>" + T("I don't know what's wrong", "مجھے نہیں معلوم گاڑی میں کیا مسئلہ ہے") + "</h3>"
                    "<p>" + T("Answer simple everyday questions - the system finds possible causes, asks you to confirm symptoms, then narrows it down.",
                              "سادہ سوالات کے جواب دیں - نظام ممکنہ وجوہات ڈھونڈے گا، علامات کی تصدیق کروائے گا پھر مسئلہ تنگ کرے گا۔") + "</p></div>",
                    unsafe_allow_html=True)
        if st.button(T("Start unknown-problem diagnosis", "نامعلوم مسئلہ تشخیص شروع کریں"), key="mode_guided", use_container_width=True):
            s.sess = api.new_session("guided", L)
            st.rerun()

else:
    sess = s.sess
    sess["lang"] = L

    # ---------- MODE 1: pick a problem card ----------
    if sess["mode"] == "direct" and sess["stage"] == "pick":
        st.markdown("<div class='sub'>" + T("What problem is your vehicle having?", "آپ کی گاڑی میں کیا مسئلہ ہے؟") + "</div>", unsafe_allow_html=True)
        from knowledge_base.vehicle_problems import CARDS
        items = list(CARDS.items())
        for i in range(0, len(items), 2):
            c1, c2 = st.columns(2)
            for col, (cid, cdata) in zip([c1, c2], items[i:i + 2]):
                with col:
                    st.markdown("<div class='mcard'><h3>" + cdata["en" if L == "en" else "ur"] + "</h3></div>", unsafe_allow_html=True)
                    if st.button(T("Select", "منتخب کریں"), key="card_" + cid, use_container_width=True):
                        api.pick_card(sess, cid)
                        st.rerun()
        if st.button(T("Back to start", "شروع پر واپس"), key="back_start1"):
            s.sess = None; st.rerun()

    # ---------- ask the current question ----------
    else:
        q = api.next_question(sess)
        if q is not None:
            # progress estimate
            if sess["mode"] == "direct":
                total = len(api.DIRECT_QUESTIONS.get(sess["card"], [])) + (1 if sess["card"] in api.REPORT_QUESTIONS else 0)
            else:
                total = len(api.GENERAL_QUESTIONS) + len(sess.get("sym_pool", [])) + 6
            st.markdown(progress_html(sess, total), unsafe_allow_html=True)
            # stage label for guided mode
            if sess["mode"] == "guided":
                stage_names = {"general": T("Step 1: General questions", "مرحلہ 1: عمومی سوالات"),
                               "confirm": T("Step 3: Confirm symptoms", "مرحلہ 3: علامات کی تصدیق"),
                               "follow": T("Step 4: Follow-up questions", "مرحلہ 4: اضافی سوالات")}
                st.caption("**" + stage_names.get(sess["stage"], "") + "**")
            render_question(sess, q)
        else:
            if sess["stage"] != "result":
                sess["stage"] = "result"
            render_result(sess)
