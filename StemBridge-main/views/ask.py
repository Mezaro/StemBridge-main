import streamlit as st
from chat_knowledge import FAQ, NCI, ACS, answer
from ui import theme


def _reply(question):
    response, sources = answer(question)
    st.session_state.chat.extend([("user", question, []), ("assistant", response, sources)])


def _chip():
    q = st.session_state.get("chip")
    if q:
        _reply(q)


def _submit():
    q = st.session_state.get("ask_box", "").strip()
    if q:
        _reply(q)
    st.session_state.ask_box = ""


def render():
    st.session_state.setdefault("chat", [])
    sb = st.session_state.sb
    theme.hero("Ask Bridgie", "Tap a question or type your own. I'll share reviewed, general answers.", "FAQ • NOT MEDICAL ADVICE")
    theme.note("I'm a fixed, keyword-based FAQ, not AI. Please don't type names or medical details. "
               "I can't assess symptoms or advise on treatment.")

    titles = [f[0] for f in FAQ]
    if sb["role"] == "caregiver" and "What can caregivers do?" in titles:
        titles.remove("What can caregivers do?")
        titles.insert(0, "What can caregivers do?")
    st.caption("Popular questions:")
    st.session_state.chip = None
    st.pills("Popular questions", titles, key="chip", selection_mode="single",
             label_visibility="collapsed", on_change=_chip)

    with st.form("ask_form", clear_on_submit=False):
        st.text_input("Or type a general question", key="ask_box", placeholder="e.g. What is engraftment?")
        st.form_submit_button("Send ➤", on_click=_submit, use_container_width=True, type="primary")

    if not st.session_state.chat:
        theme.mascot("Not sure where to begin? Try one of the questions above. I'll point you to trusted sources too.")
    pairs = [st.session_state.chat[i:i + 2] for i in range(0, len(st.session_state.chat), 2)]
    for q, a in reversed(pairs):
        with st.chat_message("user"):
            st.write(q[1])
        with st.chat_message("assistant", avatar="💠"):
            if a[1].startswith("Symptoms after transplant may need urgent care"):
                st.error(a[1])
            else:
                st.write(a[1])
            for label, url in a[2]:
                st.link_button(f"{label} source ↗", url)
    if st.session_state.chat and st.button("Clear conversation", use_container_width=True):
        st.session_state.chat = []
        st.rerun()
    c1, c2 = st.columns(2)
    c1.link_button("NCI ↗", NCI, use_container_width=True)
    c2.link_button("ACS ↗", ACS, use_container_width=True)
