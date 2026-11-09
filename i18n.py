# i18n.py - language picker: every text is written as T('English', 'Urdu')
import streamlit as st


def T(en, ur):
    # Pick UI text for the active language (English or Urdu)
    return en if st.session_state.lang == 'en' else ur


def lang():
    # Return the active language code: 'en' or 'ur'
    return st.session_state.lang
