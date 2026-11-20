"""Animated landing + 2-step friendly onboarding. Also the 'welcome back' screen."""
import streamlit as st
from ui import theme, logic
from ui.common import TOTALS


def show_landing():
    ss = st.session_state
    return (not ss.sb["onboarded"]) or (not ss.get("welcomed", False)) or ss.get("replay", False)


def _draft():
    ss = st.session_state
    if "draft" not in ss:
        sb = ss.sb
        ss.draft = {"name": sb["name"], "role": sb["role"], "type": sb["type"], "goals": list(sb["goals"])}
    return ss.draft


def _step(n):
    st.session_state.onboard_step = n


def _save_step1():
    ss = st.session_state
    d = _draft()
    d["name"] = logic.clean_name(ss.get("ob_name", ""))
    d["role"] = ss.get("ob_role") or d["role"]
    ss.onboard_step = 2


def _finish(skip=False):
    ss = st.session_state
    sb = ss.sb
    d = _draft()
    if not skip:
        d["type"] = ss.get("ob_type") or d["type"]
        d["goals"] = [g for g in (ss.get("ob_goals") or []) if g in logic.GOALS]
        sb.update(name=d["name"], role=d["role"], type=d["type"], goals=d["goals"])
    sb["onboarded"] = True
    ss.welcomed = True
    ss.replay = False
    ss.onboard_step = 0
    ss.page = "home"
    ss.just_onboarded = True
    for k in ("draft", "ob_name", "ob_role", "ob_type", "ob_goals"):
        ss.pop(k, None)


def _continue():
    st.session_state.welcomed = True
    st.session_state.page = "home"


def _replay():
    ss = st.session_state
    for k in ("draft", "ob_name", "ob_role", "ob_type", "ob_goals"):
        ss.pop(k, None)
    ss.replay = True
    ss.onboard_step = 1


def render():
    ss = st.session_state
    sb = ss.sb
    step = ss.get("onboard_step", 0)

    if sb["onboarded"] and not ss.get("replay", False):
        n = logic.first_name(sb)
        key = sb["type"]
        pct = logic.percent(sb, key, TOTALS[key])
        line = (f"You are {pct}% through the guide. Let's keep going!" if pct else "Ready when you are. No rush at all.")
        theme.landing(f"Welcome back{', ' + n if n else ''}!", "It is so good to see you again.", line)
        st.button("Continue →", type="primary", use_container_width=True, on_click=_continue, key="wb_continue")
        st.button("✏️ Update my profile", use_container_width=True, on_click=_replay, key="wb_edit")
        return

    d = _draft()
    if step == 0:
        theme.landing("Welcome to StemBridge",
                      "A friendly guide to stem cell transplants, made for patients and caregivers.",
                      "I'm Bridgie, and I'd love to get to know you first.", step=0)
        st.button("Hi Bridgie! Let's start →", type="primary", use_container_width=True, on_click=_step, args=(1,), key="ob_start")
        st.button("Skip for now", use_container_width=True, on_click=_finish, args=(True,), key="ob_skip")
        st.caption("No account needed. Anything you share stays in this browser only.")
    elif step == 1:
        theme.dots(0)
        theme.mascot("First things first: what should I call you? A nickname is perfect! "
                     "Please skip last names and health details.")
        ss.setdefault("ob_name", d["name"])
        ss.setdefault("ob_role", d["role"])
        st.text_input("Your nickname (optional)", key="ob_name", max_chars=20, placeholder="e.g. Sam")
        st.segmented_control("I'm using StemBridge as a…", ["patient", "caregiver"], key="ob_role", selection_mode="single",
                             format_func=lambda v: {"patient": "🧑 Patient", "caregiver": "🤝 Caregiver"}[v])
        a, b = st.columns(2)
        a.button("← Back", use_container_width=True, on_click=_step, args=(0,), key="ob_back1")
        b.button("Next →", type="primary", use_container_width=True, on_click=_save_step1, key="ob_next1")
    else:
        n = d["name"]
        theme.dots(1)
        theme.mascot(f"Lovely to meet you{', ' + n if n else ''}! Two quick things so I can tailor this for you.")
        ss.setdefault("ob_type", d["type"])
        ss.setdefault("ob_goals", d["goals"])
        st.segmented_control("Which transplant type are you learning about?", ["auto", "allo"], key="ob_type",
                             selection_mode="single",
                             format_func=lambda v: {"auto": "🧬 Autologous", "allo": "🤲 Allogeneic"}[v])
        st.caption("Not sure yet? Just pick one. You can switch on the Journey page whenever you like.")
        st.pills("What would you like help with? Pick as many as you like.", list(logic.GOALS), key="ob_goals",
                 selection_mode="multi", format_func=lambda g: logic.GOALS[g])
        a, b = st.columns(2)
        a.button("← Back", use_container_width=True, on_click=_step, args=(1,), key="ob_back2")
        b.button("Take me in! 🎉", type="primary", use_container_width=True, on_click=_finish, key="ob_done")
