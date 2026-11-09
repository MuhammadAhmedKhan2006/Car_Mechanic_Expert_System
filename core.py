# core.py - session state helpers
import streamlit as st

s = st.session_state


def reset_system():
    # Start a new consultation (the language choice is kept)
    s.step = 'start'; s.patient_data = {}; s.report_data = {}
    s.risk = 0; s.reasons = []; s.balloons_done = False; s.area = "-|-"
