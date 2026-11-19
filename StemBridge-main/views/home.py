from datetime import date
import streamlit as st
from ui import theme, logic
from ui.common import TYPES, TOTALS, go, role_toggle, type_toggle


def render():
    sb = st.session_state.sb
    key = sb["type"]
    name, blurb, items = TYPES[key]
    pts = logic.sparks(sb)
    lvl, nxt = logic.level(pts)
    pct = logic.percent(sb, key, TOTALS[key])

    theme.hero("Welcome to StemBridge", "Friendly, plain-language transplant education.", "PATIENTS • CAREGIVERS")
    theme.mascot(logic.COPY[sb["role"]]["hello"])
    role_toggle()
    type_toggle()
    st.caption(f"{name} transplant: {blurb.lower()}. {TOTALS[key]} phases.")

    with st.container(border=True):
        c1, c2 = st.columns([1, 2], vertical_alignment="center")
        with c1:
            theme.ring(pct)
        with c2:
            st.markdown(f"**Your reading journey**  \n{len(set(sb['done'][key]))} of {TOTALS[key]} phases read")
            st.caption(f"⚡ {pts} sparks • Level: {lvl}" + (f" • next level at {nxt}" if nxt else " • top level!"))
        st.caption("Progress tracks what you have read in this guide, not medical treatment or recovery.")
        label = "Start my journey →" if not any(sb["visited"][key]) else "Continue my journey →"
        if st.button(label, type="primary", use_container_width=True, key="home_continue"):
            st.session_state.stage = {**st.session_state.get("stage", {}), key: logic.next_stage(sb, key, TOTALS[key])}
            go("journey")
            st.rerun()

    term, definition = logic.daily_term(items, date.today())
    st.markdown(f'<div class="sb-term"><b>💡 Word of the day: {term}</b><br>{definition}</div>', unsafe_allow_html=True)

    st.markdown("#### Your badges")
    theme.badges(logic.BADGES, logic.earned(sb, TOTALS))

    st.markdown("#### Quick actions")
    a, b = st.columns(2)
    with a:
        if st.button("💬 Ask a question", use_container_width=True, key="qa_ask"):
            go("ask"); st.rerun()
    with b:
        if st.button("📚 Find support", use_container_width=True, key="qa_res"):
            go("resources"); st.rerun()
    theme.note("StemBridge is educational only. Your transplant team decides which care is right for you. "
               "For urgent symptoms, follow your team's emergency instructions or call emergency services.")
