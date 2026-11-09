# Car Mechanic Expert System — Project Report

> Paste this file into Claude (or any AI) to help write your university report.
> Sections marked with `[ADD ...]` are places where you add your own screenshots, names, etc.

---

## 1. Title

[ADD YOUR TITLE — e.g. "Car Mechanic Expert System: A Rule-Based Decision Support Tool"]

## 2. Introduction

[ADD 1 paragraph: why car problems are confusing for normal people, why a decision support tool helps, and what your project does.]

## 3. Project Overview / Explanation of the Project

This project is a **rule-based expert system** built with Python and the Streamlit library.
A user answers a few Yes/No questions about their car problem. The system:

- asks questions through a **decision tree** (one of 10 car problem categories),
- collects **risk points** for every serious answer,
- calculates a **risk score (0–100)**,
- decides an **urgency level**:
  - 0–19 → SELF-CARE (fix it yourself)
  - 20–39 → ROUTINE (book a service this week)
  - 40–69 → URGENT (see a mechanic today)
  - 70–100 → EMERGENCY (stop and call a tow truck)
- shows a **"Can I drive?"** decision, an explanation of *why* the decision was made,
  an action plan, and a downloadable **mechanic report**.

The app supports **English and Urdu** (one button switches language).
It is a **decision support tool only — it never gives a final diagnosis**.

## 4. Features

- 10 problem categories: engine won't start, overheating, brakes, strange noise/vibration,
  battery/electrical/lights, tyres, oil leak/smoke, AC, steering, gear/clutch.
- 6 guided questions per category (60 Yes/No questions total).
- 10 optional report-value inputs (battery voltage, engine temperature, oil level,
  tyre pressure, km since service).
- Risk scoring with emergency minimums (`max(risk + points, 70)`).
- Bilingual UI: every text is stored as "English|Urdu".
- Downloadable mechanic handover report (.txt file).
- "Why this decision?" and "Defending this suggestion" explainability sections.

## 5. Code Explanation (in easy English)

The whole app lives in ONE file, `car_ai.py`. Only two outside libraries are used:
`streamlit` (the web UI) and `datetime` (the report date).

| File | What it does |
|---|---|
| `car_ai.py` | Everything: page setup, CSS styling, language picker, session reset, the whole `if / elif` decision tree (all questions, rules, risk scoring) and the final report screen. Run with `streamlit run car_ai.py`. |
| `requirements.txt` | Contains only `streamlit` — tells Streamlit Cloud what to install. |

### 5.1 Session state and helpers

`st.session_state` (short name `s`) remembers data between page reloads, because
Streamlit reruns the whole script every time a button is clicked.

```python
s = st.session_state
```

`reset_system()` puts everything back to the start screen:

```python
def reset_system():
    s.step = 'start'
    s.patient_data = {}
    s.report_data = {}
    s.risk = 0
    s.reasons = []
    s.area = "-|-"
```

### 5.2 Language system

`T(en, ur)` returns English or Urdu depending on `s.lang`:

```python
L = s.lang

def T(en, ur):
    return en if L == 'en' else ur
```

Every screen text is written as `T('English text', 'اردو متن')`.
The language button only switches `'en' <-> 'ur'`.

### 5.3 Question helper

```python
def q(text, num, pct):
    st.progress(pct / 100)
    st.write(str(num) + "  —  " + text)
```

This draws the progress bar, the question number (e.g. "Q 2 / 6") and the question text.

### 5.4 The decision tree

The app is one big `if / elif` chain on `s.step`. Each `step` value is one screen.

```python
if step == 'start':
    # show 10 category buttons; each button sets s.step to the first question
elif step == 'ns1':
    # question 1 for "engine will not start"
    # YES button -> add risk points, save a reason, go to next step
elif step == 'end':
    # final decision screen
```

Example of one question:

```python
elif step == 'ns1':
    q(T('When you turn the key, do the dashboard lights stay completely off?',
        'چابی گھمانے پر کیا ڈیش بورڈ کی لائٹس بالکل بند رہتی ہیں؟'), QN + "1 / 6", 14)
    c1, c2 = st.columns(2)
    if c1.button(YES, key="ns1y", type="primary"):
        s.patient_data['dash_lights_off'] = "Yes"
        s.risk = s.risk + 15
        s.reasons.append("Dashboard lights completely off: +15 risk|ڈیش بورڈ کی لائٹس بالکل بند: +15 رسک|15")
        s.step = 'ns2'; st.rerun()
    if c2.button(NO, key="ns1n"):
        s.patient_data['dash_lights_off'] = "No"
        s.step = 'ns2'; st.rerun()
```

Important points:

- `st.rerun()` reloads the app so the next question appears.
- Serious answers add points: `s.risk = s.risk + 15`.
- Emergency signs force a high score: `s.risk = max(s.risk + 40, 70)`.
- Reasons are saved as `"English|Urdu|points"` so any language can be shown later.

### 5.5 Report-value inputs

Some steps ask for a number (battery voltage, temperature, oil level, tyre pressure, km).
`st.number_input` collects the value and the code adds risk depending on the range:

```python
elif step == 'ns_bat':
    report_input()
    st.info(T('📄 Enter the battery voltage ...', '📄 ...'))
    val = st.number_input(T('Battery voltage (V)', 'بیٹری وولٹیج (وولٹ)'),
                          min_value=0.0, max_value=20.0, value=12.6, step=0.1,
                          format="%.1f", key="ns_bat_in")
    if st.button(SUBMIT, key="ns_bat_b", type="primary"):
        s.report_data['battery_voltage'] = val
        s.step = 'ns6'
        if val < 11.0:
            s.risk = s.risk + 30
            s.reasons.append("Battery voltage very low ...|30")
        elif val < 12.2:
            s.risk = s.risk + 15
            s.reasons.append("Battery voltage low ...|15")
        st.rerun()
```

### 5.6 Final decision (`step == 'end'`)

The score is turned into a level with simple `if / elif`:

```python
if s.risk >= 70:
    lvl = "emergency"   # stop the car, call a tow truck
elif s.risk >= 40:
    lvl = "urgent"      # see a mechanic today
elif s.risk >= 20:
    lvl = "routine"     # book a service this week
else:
    lvl = "selfcare"    # simple fix you can do yourself
```

Then the screen shows:

- the urgency banner (`st.error` / `st.warning` / `st.info` / `st.success`),
- the suggestion (`st.info`),
- the possible area to check,
- the **"Can I drive?"** decision,
- the risk score and a `st.progress` bar,
- **"Why this decision?"** — every stored reason is printed,
- **"Defending this suggestion"** — strongest factor, why not higher/lower,
  warning-sign count, and a confidence note (BORDERLINE / CLEAR),
- **"What to do now"** — a numbered action plan,
- the entered report values,
- a **downloadable mechanic report** built as plain text (`hr`),
- the disclaimer and the **Start New Consultation** button.

The report is just a text string:

```python
hr = T('CAR CHECK REPORT ...', '...') + "\n"
hr = hr + T('Date: ', 'تاریخ: ') + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
# ... more lines ...
st.download_button('📄 Download Mechanic Report', data=hr,
                   file_name="mechanic_report.txt", mime="text/plain")
```

### 5.7 Design ideas used

- **Decision tree** instead of a flat questionnaire — each answer leads to the next question.
- **Weighted scoring** — different symptoms add different risk points.
- **Safety minimum** — `max(risk + points, 70)` means one dangerous sign can never give a low score.
- **Explainability** — the app shows its reasons and even argues for/against its own suggestion.
- **Bilingual storage** — texts are stored once as "English|Urdu|points".

## 6. Market Use Case

[ADD your own paragraph, e.g.: everyday drivers do not know car mechanics; this tool
triages symptoms before a workshop visit, saves time and money, reduces panic,
and helps mechanics by giving them a structured handover report. Possible users:
car owners, driving schools, fleet managers, roadside help services.]

## 7. Limitations and Future Work

[ADD: it is rule-based (not AI/ML), it does not replace a mechanic, covers only
10 problem categories, could be extended with a real diagnosis knowledge base,
voice input, more languages, or a mobile app.]

## 8. Screenshots

[ADD SCREENSHOT 1 — welcome screen with 10 categories]
[ADD SCREENSHOT 2 — a Yes/No question with progress bar]
[ADD SCREENSHOT 3 — final result with risk score and "Can I drive?"]
[ADD SCREENSHOT 4 — mechanic report download / Urdu language view]

## 9. How to Run

```bash
pip install streamlit
streamlit run car_ai.py
```

Live demo: [ADD YOUR NEW STREAMLIT CLOUD LINK HERE]
