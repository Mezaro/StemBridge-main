"""Executes every view against Streamlit (real or stub) to catch NameError/TypeError/KeyError."""
import streamlit as st
from ui import storage, theme


def _boot(role="patient", typ="auto", **kw):
    st.session_state.clear()
    st.session_state.page = "home"
    storage.init()
    st.session_state.sb.update(role=role, type=typ, **kw)


def test_all_views_render_for_all_modes():
    from views import home, journey, ask, more, landing
    for role in ("patient", "caregiver"):
        for typ in ("auto", "allo"):
            _boot(role, typ, name="Sam", goals=["money"], onboarded=True)
            for v in (home, journey, ask, more):
                v.render()
            st.session_state.stage = {typ: 99}
            journey.render()
            assert st.session_state.stage[typ] <= 7
            storage.persist()


def test_landing_flow_new_user():
    from views import landing
    _boot()
    assert landing.show_landing()
    for step in (0, 1, 2):
        st.session_state.onboard_step = step
        landing.render()
    st.session_state.draft = {"name": "Sam", "role": "caregiver", "type": "auto", "goals": []}
    st.session_state.ob_name = "  Sam<3 "; st.session_state.ob_role = "caregiver"
    landing._save_step1()
    assert st.session_state.draft["name"] == "Sam" and st.session_state.onboard_step == 2
    st.session_state.ob_type = "allo"; st.session_state.ob_goals = ["money", "bogus"]
    landing._finish()
    sb = st.session_state.sb
    assert (sb["name"], sb["role"], sb["type"], sb["goals"], sb["onboarded"]) == ("Sam", "caregiver", "allo", ["money"], True)
    assert st.session_state.page == "home" and not landing.show_landing()


def test_landing_skip_returning_and_replay():
    from views import landing
    _boot(); landing._finish(skip=True)
    assert st.session_state.sb["onboarded"] and not landing.show_landing()
    st.session_state.welcomed = False
    assert landing.show_landing(); landing.render()
    landing._continue(); assert not landing.show_landing()
    landing._replay(); assert landing.show_landing() and st.session_state.onboard_step == 1
    landing.render()


def test_journey_marks_visited_and_complete():
    from views import journey
    _boot()
    journey.render()
    assert 0 in st.session_state.sb["visited"]["auto"]
    journey._complete("auto", 0); journey._complete("auto", 0)
    assert st.session_state.sb["done"]["auto"] == [0]
    journey._move("auto", 1, 7); journey._move("auto", -5, 7)
    assert st.session_state.stage["auto"] == 0


def test_chat_flow_and_urgent():
    from views import ask
    _boot()
    st.session_state.chat = []
    ask._reply("What is GVHD?"); ask._reply("I have chest pain")
    assert len(st.session_state.chat) == 4
    assert st.session_state.chat[3][1].startswith("Symptoms after transplant may need urgent care")
