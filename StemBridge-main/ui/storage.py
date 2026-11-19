"""Browser-side persistence (localStorage) via streamlit-js-eval. Falls back to session-only."""
import copy
import json
import streamlit as st

try:
    from streamlit_js_eval import streamlit_js_eval
except ImportError:  # session-only fallback
    streamlit_js_eval = None

LS_KEY = "stembridge_v1"
DEFAULT = {
    "type": "auto", "role": "patient",
    "visited": {"auto": [], "allo": []}, "done": {"auto": [], "allo": []},
    "checked": [], "quiz": [], "bookmarks": [], "seen_badges": [],
}


def _merge(data):
    base = copy.deepcopy(DEFAULT)
    if not isinstance(data, dict):
        return base
    for k, v in data.items():
        if k in ("visited", "done") and isinstance(v, dict):
            for t in ("auto", "allo"):
                base[k][t] = [int(i) for i in v.get(t, []) if isinstance(i, int)]
        elif k in ("checked", "quiz", "bookmarks", "seen_badges") and isinstance(v, list):
            base[k] = [x for x in v if isinstance(x, str)]
        elif k == "type" and v in ("auto", "allo"):
            base[k] = v
        elif k == "role" and v in ("patient", "caregiver"):
            base[k] = v
    return base


def init():
    ss = st.session_state
    if "sb" not in ss:
        ss.sb = copy.deepcopy(DEFAULT)
        ss.sb_hydrated = streamlit_js_eval is None
        ss.sb_last = None
        ss.sb_saves = 0
        ss.sb_saved_resources = set()
    if not ss.sb_hydrated:
        raw = streamlit_js_eval(js_expressions=f"localStorage.getItem('{LS_KEY}') || '{{}}'", key="sb_ls_get")
        if raw is not None:
            try:
                ss.sb = _merge(json.loads(raw))
            except (ValueError, TypeError):
                ss.sb = _merge({})
            ss.sb_saved_resources = set(ss.sb["bookmarks"])
            ss.sb_hydrated = True
            ss.sb_last = json.dumps(ss.sb, sort_keys=True)
    return ss.sb


def persist():
    ss = st.session_state
    ss.sb["bookmarks"] = sorted(ss.get("sb_saved_resources", set()))
    if streamlit_js_eval is None or not ss.sb_hydrated:
        return
    payload = json.dumps(ss.sb, sort_keys=True)
    if payload != ss.sb_last:
        ss.sb_last = payload
        ss.sb_saves += 1
        streamlit_js_eval(js_expressions=f"localStorage.setItem('{LS_KEY}', {json.dumps(payload)})",
                          key=f"sb_ls_set_{ss.sb_saves}")


def reset():
    st.session_state.sb = copy.deepcopy(DEFAULT)
    st.session_state.sb_saved_resources = set()
