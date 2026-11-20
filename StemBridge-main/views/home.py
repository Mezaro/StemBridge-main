from datetime import date
from html import escape
import streamlit as st
from ui import theme, logic
from ui.common import TYPES, TOTALS, go, role_toggle, type_toggle


def render():
    ss = st.session_state
    sb = ss.sb
    key = sb["type"]
    name, blurb, items = TYPES[key]
    pct = logic.percent(sb, key, TOTALS[key])

    if ss.pop("just_onboarded", False):
        st.toast(f"Welcome aboard{', ' + logic.first_name(sb) if logic.first_name(sb) else ''}! 💙", icon="🎉")

    sub = ("Here is a calm place to learn, one step at a time." if sb["role"] == "patient"
           else "Here is a calm place to learn how to support your loved one.")
    theme.hero(logic.hello(sb), sub, "YOUR STEMBRIDGE")
    theme.mascot(logic.mascot_line(sb, pct))

    with st.container(border=True):
        c1, c2 = st.columns([1, 2], vertical_alignment="center")
        with c1:
            theme.ring(pct)
        with c2:
            st.markdown(f"**{name} journey**  \n{len(set(sb['done'][key]))} of {TOTALS[key]} phases read")
            st.caption(f"{blurb}. Reading progress only, not medical progress.")
        label = "Start my journey →" if not any(sb["visited"][key]) else "Continue my journey →"
        if st.button(label, type="primary", use_container_width=True, key="home_continue"):
            ss.stage = {**ss.get("stage", {}), key: logic.next_stage(sb, key, TOTALS[key])}
            go("journey")
            st.rerun()

    st.markdown("#### Picked for you")
    for gid, icon, text, page in logic.suggested_actions(sb):
        if st.button(f"{icon}  {text}", use_container_width=True, key=f"pick_{gid}"):
            go(page); st.rerun()

    term, definition = logic.daily_term(items, date.today())
    st.markdown(f'<div class="sb-term"><b>💡 Word of the day: {escape(term)}</b><br>{escape(definition)}</div>',
                unsafe_allow_html=True)

    st.markdown("#### Your badges")
    st.caption("Collect them as you explore. They're just for fun!")
    theme.badges(logic.BADGES, logic.earned(sb, TOTALS))

    with st.expander("Switch who or what this is for"):
        role_toggle()
        type_toggle()
    theme.note("StemBridge is educational only. Your transplant team decides which care is right for you. "
               "For urgent symptoms, follow your team's emergency instructions or call emergency services.")
