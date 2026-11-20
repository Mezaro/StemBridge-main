import streamlit as st
from ui import theme, storage
from views import landing

CENTERS = [
    ("MD Anderson Cancer Center", "Houston", "TX", "https://www.mdanderson.org/"),
    ("UT Southwestern Medical Center", "Dallas", "TX", "https://utswmed.org/"),
    ("Baylor University Medical Center", "Dallas", "TX", "https://www.bswhealth.com/"),
    ("Mayo Clinic", "Rochester", "MN", "https://www.mayoclinic.org/"),
    ("Memorial Sloan Kettering Cancer Center", "New York", "NY", "https://www.mskcc.org/"),
    ("Dana-Farber Cancer Institute", "Boston", "MA", "https://www.dana-farber.org/"),
    ("Fred Hutchinson Cancer Center", "Seattle", "WA", "https://www.fredhutch.org/"),
    ("City of Hope", "Duarte", "CA", "https://www.cityofhope.org/"),
    ("Stanford Health Care", "Stanford", "CA", "https://stanfordhealthcare.org/"),
    ("Johns Hopkins Medicine", "Baltimore", "MD", "https://www.hopkinsmedicine.org/"),
]

FIN_Q = [
    "What does my insurance cover, including evaluation and follow-up?",
    "Do I need prior authorization or a referral?",
    "What travel, lodging, or caregiver costs should I plan for?",
    "Are there grants or assistance programs I may qualify for?",
    "Who can help with appeals or denied insurance claims?",
]

CARE = {
    "Before transplant": ["Ask the center what help is expected from a caregiver.",
                          "Plan transportation, temporary housing, and time away from work.",
                          "Learn infection-prevention guidance and emergency contact procedures.",
                          "Discuss backup caregiving arrangements."],
    "During treatment": ["Follow the center's visitor and hygiene instructions.",
                         "Help communicate questions to the care team when requested.",
                         "Ask about food, hydration, and activity guidance.",
                         "Support practical daily needs."],
    "After discharge": ["Review discharge instructions with the transplant team.",
                        "Understand which symptoms require immediate medical contact.",
                        "Help organize appointments and transportation.",
                        "Do not change medicines or interpret test results independently."],
    "Caring for the caregiver": ["Arrange backup caregivers or respite support.",
                                 "Discuss emotional and practical concerns with a social worker.",
                                 "Explore counseling and peer support.",
                                 "Plan time for rest and personal needs."],
}

SECOND = [
    ("Talk with your current care team", "Ask whether another specialist can review the recommendation and how urgent the decision is."),
    ("Find another transplant program", "Use center directories and confirm the center evaluates your condition and transplant type."),
    ("Ask which records are needed", "Centers may request pathology, treatment history, imaging, blood tests, and HLA results. Share them through secure channels."),
    ("Check insurance and scheduling", "Ask about referrals, authorization, consultation costs, and timing."),
    ("Compare recommendations", "Discuss benefits, risks, alternatives, and donor options (when relevant) with your treating clinicians."),
]
SECOND_Q = [
    "Do you agree with the recommended transplant type and timing?",
    "What are the main benefits, risks, and alternatives?",
    "What experience does your program have with this condition?",
    "For an allogeneic transplant, what donor options would you consider?",
    "What support is available for caregivers, housing, and costs?",
]


def _checklist(prefix, items):
    sb = st.session_state.sb
    for i, q in enumerate(items):
        qid = f"{prefix}:{i}"
        wk = f"c_{qid}"
        st.session_state[wk] = qid in sb["checked"]

        def _cb(qid=qid, wk=wk):
            c = st.session_state.sb["checked"]
            if st.session_state[wk] and qid not in c:
                c.append(qid)
            elif not st.session_state[wk] and qid in c:
                c.remove(qid)
        st.checkbox(q, key=wk, on_change=_cb)


def render():
    theme.hero("More ways I can help", "Centers, second opinions, caregiver tips, and money questions.", "TOOLS & GUIDES")
    t1, t2, t3, t4, t5 = st.tabs(["🏥 Centers", "🩺 2nd opinion", "🤝 Caregivers", "💚 Money", "⚙️ Me"])
    with t1:
        theme.note("This is an illustrative list, not complete, ranked, or verified. Please confirm services and insurance with each center.")
        q = st.text_input("Search center, city, or state", placeholder="Dallas, Mayo, CA…").strip().casefold()
        hits = [c for c in CENTERS if q in " ".join(c[:3]).casefold()]
        st.caption(f"{len(hits)} centers")
        for name, city, state, url in hits:
            with st.container(border=True):
                st.markdown(f"**🏥 {name}**  \n📍 {city}, {state}")
                st.link_button("Official website ↗", url, use_container_width=True)
        if not hits:
            st.info("No match yet. Try an official directory below.")
        st.link_button("NCI Cancer Centers ↗", "https://www.cancer.gov/research/infrastructure/cancer-centers/find", use_container_width=True)
        st.link_button("NMDP Patient Resources ↗", "https://www.nmdp.org/patients", use_container_width=True)
    with t2:
        theme.note("StemBridge does not schedule appointments or send records. Please don't delay urgent treatment without talking to your team.")
        for i, (t, d) in enumerate(SECOND, 1):
            with st.expander(f"{i}. {t}", expanded=i == 1):
                st.write(d)
        st.markdown("**Questions for the second specialist**")
        _checklist("second", SECOND_Q)
    with t3:
        theme.note("Responsibilities vary. Please follow the instructions of the patient's clinical team.")
        for i, (title, items) in enumerate(CARE.items()):
            with st.expander(title, expanded=i == 0):
                _checklist(f"care{i}", items)
    with t4:
        theme.note("Assistance varies by diagnosis, insurance, location, and eligibility. StemBridge does not submit applications.")
        st.markdown("**Questions for a financial counselor**")
        _checklist("fin", FIN_Q)
        st.caption("You can find organizations under Support, then Financial Help.")
    with t5:
        sb = st.session_state.sb
        n = sb["name"] or "friend"
        st.markdown(f"**Hi, {n}!** 💙 You're using StemBridge as a **{sb['role']}**.")
        st.button("✏️ Update my profile", use_container_width=True, on_click=landing._replay, key="me_edit")
        st.markdown("**Add me to your phone:** open this site in Chrome or Safari, then choose *Add to Home Screen*.")
        st.caption("Your nickname, progress, and badges are saved only in this browser. There are no accounts and no "
                   "server database. Please don't enter personal health information.")
        st.markdown("StemBridge is a classroom educational prototype for SDG 3. It is not a medical device and does not "
                    "replace professional care. Content needs clinical review before real patient use.")
        if st.button("Reset everything", use_container_width=True):
            storage.reset()
            st.toast("All saved info cleared.", icon="🧹")
            st.rerun()
