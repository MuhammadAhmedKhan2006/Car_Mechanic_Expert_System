# Vehicle Diagnosis Decision Support System (DSS)

## 1. Project Title

**Vehicle Diagnosis Decision Support System (DSS) — Interactive Car Problem Identifier**

## 2. Introduction

This project is an interactive, web-based decision support system that helps ordinary vehicle
owners identify possible problems with their car without needing any technical automotive
knowledge.

The system asks the user a series of simple questions (in everyday language, not technical
jargon) and then uses rule-based decision-making logic to:

- identify the **most likely vehicle problem**,
- show the **supporting evidence** (which answers pointed to that problem),
- list **alternative possible causes**,
- give **recommended actions** with an explanation of *why* each action is suggested,
- assign a **priority level** (Low / Medium / High / Urgent-Safety Critical), and
- show a clear **disclaimer** that the result is a preliminary assessment, not a final diagnosis.

The application is built with **Python** only — Streamlit for the interface and plain
`if / elif / else` conditional logic for the decision engine. No advanced frameworks or
external databases are used.

## 3. Explanation of the System

### Two diagnosis modes

When the app opens, the user chooses between two modes:

- **Mode 1 — "I have an idea about the problem":** the user picks a suspected problem from a
  visual card list (engine won't start, overheating, brakes, strange noise, battery/electrics,
  tyres, oil leak/smoke, AC, steering, gear/clutch, poor performance, exhaust smoke). The system
  then asks 5 targeted Yes/No questions plus one numeric report input (e.g. battery voltage,
  engine temperature, tyre pressure, oil level, kilometres since service).

- **Mode 2 — "I don't know what's wrong":** designed for users with no idea what is wrong.
  - **Step 1:** 12 simple general questions about driving behaviour, sounds, lights and changes.
  - **Step 2:** the answers are scored to produce a shortlist of possible problems shown in
    plain language.
  - **Step 3:** the user confirms or rejects individual symptoms with **Yes / No / Not Sure**.
  - **Step 4:** conditional follow-up questions are asked based on the strongest candidate.
  - **Step 5:** a final result is produced — or, if the answers are unclear, the system honestly
    reports "not enough information" instead of guessing.

### Decision-making logic

Every answer updates a score for each vehicle system inside `knowledge_base/decision_rules.py`.
The file contains **more than 50 meaningful `if / elif / else` branches** (one per question plus
range checks for the numeric inputs). Different answer combinations produce different question
paths and different final diagnoses — the logic is dynamic, not a fixed script.

### Question bank

The knowledge base contains **100 questions** in total:

- 12 general questions (Mode 2)
- 60 direct questions — 5 per problem card (Mode 1)
- 12 numeric report inputs (Mode 1)
- 16 symptom-confirmation statements (Mode 2)

Only the relevant questions are shown in each session; questions are never repeated because
every answer is stored by question ID.

### Recommendations and reasoning

For every diagnosis the system shows recommended actions **and the reason for each one**
(e.g. "Check coolant level — low coolant or a leak is the most common cause of overheating").
Safety-critical results (brake failure risk, severe overheating, loss of steering control)
trigger an urgent warning recommending the driver to stop safely and call a tow truck.

### Languages and themes

- Full **English / Urdu** interface — one button switches the entire app, including all
  questions, results and recommendations.
- **Dark theme** (premium black + red accent, the default) and **Light theme**, switched by a
  single button.
- Responsive layout that works on **desktop, tablet and mobile**.

## 4. Market Use Case

- **Vehicle owners / drivers:** a free first-line check before visiting a workshop — saves time
  and avoids unnecessary repair costs.
- **Driving schools and fleet managers:** quick triage of reported vehicle issues across a fleet.
- **Used-car buyers:** a preliminary health check of a vehicle before purchase.
- **Workshops and mechanics:** the result page can be shown to a mechanic so the inspection
  starts from the most likely cause instead of from zero.
- **Academic / training use:** demonstrates a real rule-based expert system — knowledge base,
  inference rules, explainable output — using only beginner-friendly Python.

Because the system never claims a final diagnosis and always recommends professional
verification, it is safe to deploy as a public-facing advisory tool.

## 5. Technology

- **Python 3** (basic concepts only: dictionaries, lists, loops, functions, `if/elif/else`)
- **Streamlit** — web UI
- No database, no JavaScript, no external services — everything runs locally in the browser.

## 6. Live Application

> **Streamlit link:** `[PASTE YOUR STREAMLIT APP LINK HERE]`
>
> Example format: `https://<your-app-name>.streamlit.app`

## 7. Screenshots

> Place the screenshots of the project below (replace these placeholders with your own images).

**Screenshot 1 — Start screen (two diagnosis modes):**
`[SCREENSHOT 1: start screen showing "I have an idea" and "I don't know" mode cards]`

**Screenshot 2 — Question screen:**
`[SCREENSHOT 2: a question with Yes / No / Not Sure buttons and progress bar]`

**Screenshot 3 — Final diagnosis result:**
`[SCREENSHOT 3: result page showing most likely problem, evidence, alternatives, recommendations and priority]`

**Screenshot 4 — Urdu / light theme (optional):**
`[SCREENSHOT 4: the same app in Urdu and/or light theme]`
