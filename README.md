# Car Mechanic Expert System (IAI Project)

A rule-based expert system that does decision making and decision support for car problems.
It gives a suggestion, explains and defends it, and can be switched between English and Urdu
with one button. Beautiful animated interface, works on phones.

## Files
- `car_ai.py`                the complete Streamlit app (built-in SQLite, no other libraries)
- `requirements.txt`         contains `streamlit` (used when you deploy online)
- `.streamlit/config.toml`   light theme colours (upload this folder too when you deploy)
- `car_ai.db`                created automatically on the first run (SQLite database)

## Run on your computer
1. Install Python 3.9+ (tick "Add Python to PATH" on Windows).
2. Open a terminal in this folder and run:  pip install streamlit
3. Run:  streamlit run car_ai.py
4. Open http://localhost:8501 if the browser does not open by itself. Stop with Ctrl + C.
   If `streamlit` is not recognised, use:  python -m streamlit run car_ai.py
5. To test the phone layout: open the page and press F12, then the device toolbar (or open the
   live link on your phone).

## Get the live (WAN) link - Streamlit Community Cloud, free
1. Create a free GitHub account and a new PUBLIC repository (for example `car-mechanic-ai`).
2. Upload `car_ai.py`, `requirements.txt` and the `.streamlit` folder to the repository
   (Add file -> Upload files; drag the whole folder content).
3. Go to https://share.streamlit.io , sign in with GitHub and click "Create app".
4. Choose the repository, branch `main`, main file path `car_ai.py`, then click Deploy.
5. After 1-3 minutes you get a public link like https://your-app-name.streamlit.app
Note: on the free cloud the SQLite file is reset whenever the app restarts or sleeps.
Use your own computer when you need the saved records to stay permanently.

## What it does
- 10 car problems: engine won't start, overheating, brakes, strange noise/vibration,
  battery/electrical, tyres, oil leak/smoke, AC, steering, gear/clutch
- 60 Yes/No questions + 10 report inputs (battery voltage, engine temperature, tyre pressure,
  oil level, km since last service) with rules that branch on the values
- DECISION MAKING: risk score 0-100 -> urgency level (EMERGENCY / URGENT / ROUTINE /
  SELF-CARE) -> a clear "Can I drive?" decision
- DECISION SUPPORT: suggestion, possible area to check, "why this decision" list with points,
  "Defending this suggestion" panel (strongest factor, why not a higher or lower level,
  confidence), action plan
- EXTRA FEATURES: (1) the defence panel with confidence / decision margin,
  (2) a downloadable "Mechanic Report" text file the owner can show to the mechanic
- UI: animated gradient hero with a driving car, question cards with progress bar, animated
  risk meter, pulsing emergency card, balloons for a good result, mobile responsive layout
  (Yes/No buttons stay side by side on phones), full English/Urdu switch with right-to-left layout
- Every final result is saved in SQLite (table `consultations`);
  the sidebar button "View Saved Data" shows all rows
- Safe wording: it never gives a final diagnosis; it always says to get the car checked
  by a qualified mechanic (or to stop the car and call a tow truck in an emergency)
