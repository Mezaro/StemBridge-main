"""Uses real Streamlit if installed; otherwise a permissive stub so logic/smoke tests still run."""
import os, sys, types
from unittest.mock import MagicMock
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import streamlit  # noqa: F401
except ImportError:
    class SS(dict):
        __getattr__ = lambda s, k: s[k] if k in s else (_ for _ in ()).throw(AttributeError(k))
        __setattr__ = dict.__setitem__

    st = MagicMock(name="streamlit")
    st.session_state = SS()
    st.columns.side_effect = lambda spec, **k: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
    st.tabs.side_effect = lambda labels: [MagicMock() for _ in labels]
    st.button.return_value = False
    st.text_input.return_value = ""
    st.checkbox.return_value = False
    st.radio.return_value = None
    st.pills.return_value = None
    sys.modules["streamlit"] = st
    comps = types.ModuleType("streamlit.components"); v1 = MagicMock()
    sys.modules["streamlit.components"] = comps; sys.modules["streamlit.components.v1"] = v1; comps.v1 = v1; st.components = comps
    sys.modules["streamlit_js_eval"] = MagicMock(streamlit_js_eval=MagicMock(return_value=None))
