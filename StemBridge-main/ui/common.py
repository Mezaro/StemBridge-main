import streamlit as st
from journey_visuals import AUTO, ALLO

TYPES = {"auto": ("Autologous", "Your own stem cells", AUTO), "allo": ("Allogeneic", "Donor stem cells", ALLO)}
TOTALS = {k: len(v[2]) for k, v in TYPES.items()}


def go(page):
    st.session_state.page = page


def _set(field, widget_key):
    val = st.session_state.get(widget_key)
    if val is not None:
        st.session_state.sb[field] = val


def role_toggle(key="w_role"):
    st.session_state[key] = st.session_state.sb["role"]
    st.segmented_control("I am a…", ["patient", "caregiver"], key=key, selection_mode="single",
                         format_func=lambda v: {"patient": "🧑 Patient", "caregiver": "🤝 Caregiver"}[v],
                         on_change=_set, args=("role", key))


def type_toggle(key="w_type"):
    st.session_state[key] = st.session_state.sb["type"]
    st.segmented_control("Transplant type", ["auto", "allo"], key=key, selection_mode="single",
                         format_func=lambda v: {"auto": "🧬 Autologous", "allo": "🤲 Allogeneic"}[v],
                         on_change=_set, args=("type", key))
