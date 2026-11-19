import streamlit as st
from ui import theme, logic
from ui.common import TYPES, TOTALS, role_toggle, type_toggle


def _stage_state():
    st.session_state.setdefault("stage", {})
    return st.session_state.stage


def _move(key, delta, total):
    s = _stage_state()
    s[key] = max(0, min(total - 1, s.get(key, 0) + delta))


def _pick(key, widget):
    v = st.session_state.get(widget)
    if v is not None:
        _stage_state()[key] = v


def _complete(key, idx):
    sb = st.session_state.sb
    if idx not in sb["done"][key]:
        sb["done"][key].append(idx)
        st.session_state.just_done = (key, idx)


def _tick(qid, wkey):
    checked = st.session_state.sb["checked"]
    if st.session_state.get(wkey):
        if qid not in checked:
            checked.append(qid)
    elif qid in checked:
        checked.remove(qid)


def render():
    sb = st.session_state.sb
    key = sb["type"]
    name, _, items = TYPES[key]
    total = TOTALS[key]
    stages = _stage_state()
    cur = max(0, min(total - 1, stages.get(key, 0)))
    stages[key] = cur
    stage = items[cur]

    theme.hero("My journey", f"{name} transplant • {total} phases", "TAP A PHASE TO EXPLORE")
    type_toggle()

    visited = set(sb["visited"][key]); visited.add(cur)
    sb["visited"][key] = sorted(visited)
    done = set(sb["done"][key])
    theme.stepper(total, cur, visited, done)

    wkey = f"pills_{key}"
    st.session_state[wkey] = cur
    st.pills("Phase", list(range(total)), key=wkey, selection_mode="single", label_visibility="collapsed",
             format_func=lambda i: f"{'✅' if i in done else items[i]['icon']} {i + 1}",
             on_change=_pick, args=(key, wkey))

    st.markdown(f'<div class="sb-card"><span class="sb-stage-icon">{stage["icon"]}</span> '
                f'<b>Phase {cur + 1} of {total}: {stage["name"]}</b><h4>{stage["heading"]}</h4></div>',
                unsafe_allow_html=True)

    t_what, t_tests, t_ask, t_words, t_quiz = st.tabs(["📖 What", "🧪 Tests", "❓ Ask", "🔤 Words", "🎮 Quiz"])
    with t_what:
        st.markdown(stage["description"].strip())
        theme.note("Caregiver tip: " + logic.COPY[sb["role"]]["tip"] if sb["role"] == "caregiver"
                   else "Tip: " + logic.COPY[sb["role"]]["tip"])
    with t_tests:
        st.caption("Tests and activities that may happen. Your team decides what applies to you.")
        for x in logic.parse_list(stage["tests"]):
            st.markdown(f"- {x}")
    with t_ask:
        st.caption(logic.COPY[sb["role"]]["ask"])
        for qi, q in enumerate(logic.parse_list(stage["questions"])):
            qid = f"{key}:{cur}:{qi}"
            wk = f"q_{qid}"
            st.session_state[wk] = qid in sb["checked"]
            st.checkbox(q, key=wk, on_change=_tick, args=(qid, wk))
    with t_words:
        for term, definition in logic.parse_terms(stage["terms"]):
            st.markdown(f"**{term}**: {definition}")
    with t_quiz:
        quiz = logic.make_quiz(items, cur, seed=1)
        qid = f"{key}:{cur}"
        if not quiz:
            st.info("No quiz for this phase.")
        else:
            st.markdown(f"Which word matches this meaning?\n\n> {quiz['definition']}")
            choice = st.radio("Pick one", quiz["options"], index=None, key=f"quiz_{qid}", label_visibility="collapsed")
            if st.button("Check my answer", key=f"chk_{qid}", use_container_width=True):
                if choice is None:
                    st.warning("Pick an answer first.")
                elif choice == quiz["answer"]:
                    if qid not in sb["quiz"]:
                        sb["quiz"].append(qid)
                    st.success("🎉 Correct! +10 sparks")
                else:
                    st.info(f"Not quite. The answer is **{quiz['answer']}**. Check the Words tab and try another phase!")

    p, d, n = st.columns([1, 2, 1], vertical_alignment="center")
    with p:
        st.button("←", key="prev", on_click=_move, args=(key, -1, total), disabled=cur == 0, use_container_width=True)
    with d:
        if cur in done:
            st.button("✅ Read", disabled=True, use_container_width=True, key="done_btn")
        else:
            st.button("Mark as read ✓", type="primary", on_click=_complete, args=(key, cur),
                      use_container_width=True, key="done_btn")
    with n:
        st.button("→", key="next", on_click=_move, args=(key, 1, total), disabled=cur == total - 1, use_container_width=True)

    jd = st.session_state.pop("just_done", None)
    if jd:
        if len(set(sb["done"][key])) >= total:
            st.balloons()
            st.toast("You finished every phase! 🏁", icon="🎉")
        else:
            st.toast("Phase complete! +15 sparks", icon="⚡")
    theme.note("Urgent symptoms? Contact your transplant team using their emergency instructions, or call emergency "
               "services. This guide cannot assess symptoms.")
