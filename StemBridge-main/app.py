"""StemBridge: mobile-first educational transplant navigator (Streamlit).

Run: python -m streamlit run app.py
Educational prototype only. Not a medical device or clinical decision-support system.
"""
import streamlit as st

st.set_page_config(page_title="StemBridge", page_icon="💙", layout="centered", initial_sidebar_state="collapsed")

from ui import storage, theme  # noqa: E402
from views import home, journey, ask, resources, more  # noqa: E402

PAGES = {
    "home": ("🏠", "Home", home.render),
    "journey": ("🧭", "Journey", journey.render),
    "ask": ("💬", "Ask", ask.render),
    "resources": ("📚", "Support", resources.render),
    "more": ("➕", "More", more.render),
}


def _nav(page):
    st.session_state.page = page


st.session_state.setdefault("page", "home")
storage.init()
theme.inject()

PAGES[st.session_state.page][2]()

with st.container(key="bottomnav"):
    cols = st.columns(len(PAGES))
    for col, (pid, (icon, label, _)) in zip(cols, PAGES.items()):
        with col:
            st.button(f"{icon}\n{label}", key=f"nav_{pid}", use_container_width=True,
                      type="primary" if st.session_state.page == pid else "secondary",
                      on_click=_nav, args=(pid,))

storage.persist()
