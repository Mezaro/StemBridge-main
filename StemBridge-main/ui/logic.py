"""Pure logic (no Streamlit): terms, quiz, badges, personalization. Unit-testable."""
import random
import re
from datetime import date

TERM_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.+)$")

BADGES = [
    ("first", "🌟", "First Step", "Open any journey phase"),
    ("explorer", "🧭", "Explorer", "Visit every phase of your journey"),
    ("asker", "❓", "Question Keeper", "Tick 5 questions for your care team"),
    ("quiz", "🧠", "Word Wizard", "Answer 3 word quizzes correctly"),
    ("finisher", "🏁", "Journey Finisher", "Mark every phase as read"),
    ("saver", "⭐", "Resource Saver", "Save a resource"),
]
BADGE_NAMES = {b[0]: f"{b[1]} {b[2]}" for b in BADGES}

GOALS = {
    "journey": "Understand the transplant journey",
    "questions": "Prepare questions for the care team",
    "support": "Find support and resources",
    "money": "Learn about costs and financial help",
    "caregiving": "Learn how to support someone",
}
GOAL_ACTIONS = {
    "journey": ("🧭", "Explore my journey", "journey"),
    "questions": ("❓", "Build my question list", "journey"),
    "support": ("📚", "Find support", "resources"),
    "money": ("💚", "Money questions", "more"),
    "caregiving": ("🤝", "Caregiver guide", "more"),
}
DEFAULT_ACTIONS = ["journey", "support", "questions"]


def clean_name(raw):
    """Nickname only: letters, spaces, hyphen, apostrophe; max 20 chars."""
    if not isinstance(raw, str):
        return ""
    return re.sub(r"[^A-Za-z\u00C0-\u024F '\-]", "", raw).strip()[:20]


def parse_list(text):
    return [ln.strip()[2:].strip() for ln in text.strip().splitlines() if ln.strip().startswith("- ")]


def parse_terms(text):
    out = []
    for ln in text.strip().splitlines():
        m = TERM_RE.match(ln.strip())
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def all_terms(stages):
    seen, out = set(), []
    for s in stages:
        for t, d in parse_terms(s["terms"]):
            if t.lower() not in seen:
                seen.add(t.lower())
                out.append((t, d))
    return out


def make_quiz(stages, idx, seed=0):
    own = parse_terms(stages[idx]["terms"])
    if not own:
        return None
    term, definition = own[0]
    pool = [t for t, _ in all_terms(stages) if t.lower() != term.lower()]
    rng = random.Random(f"{seed}-{idx}")
    options = rng.sample(pool, min(3, len(pool))) + [term]
    rng.shuffle(options)
    return {"definition": definition, "answer": term, "options": options}


def daily_term(stages, today=None):
    terms = all_terms(stages)
    today = today or date.today()
    return terms[today.toordinal() % len(terms)]


def earned(sb, totals):
    ids = set()
    if any(sb["visited"].values()):
        ids.add("first")
    if any(len(set(sb["visited"][k])) >= n for k, n in totals.items()):
        ids.add("explorer")
    if len(sb["checked"]) >= 5:
        ids.add("asker")
    if len(sb["quiz"]) >= 3:
        ids.add("quiz")
    if any(len(set(sb["done"][k])) >= n for k, n in totals.items()):
        ids.add("finisher")
    if sb["bookmarks"]:
        ids.add("saver")
    return ids


def new_badges(sb, totals):
    """Badges earned but not yet celebrated (ordered as in BADGES)."""
    got = earned(sb, totals)
    return [b[0] for b in BADGES if b[0] in got and b[0] not in sb["seen_badges"]]


def percent(sb, key, total):
    return round(100 * len(set(sb["done"][key])) / total) if total else 0


def next_stage(sb, key, total):
    done = set(sb["done"][key])
    for i in range(total):
        if i not in done:
            return i
    return total - 1


# ---------- personalization ----------
def first_name(sb):
    return clean_name(sb.get("name", ""))


def hello(sb):
    n = first_name(sb)
    return f"Hi, {n}!" if n else "Hi there!"


def mascot_line(sb, pct=0):
    n = first_name(sb)
    who = "your loved one" if sb["role"] == "caregiver" else "you"
    if pct >= 100:
        return f"Amazing work{', ' + n if n else ''}! You have read every phase. Come back anytime to review."
    if pct > 0:
        return f"Welcome back{', ' + n if n else ''}! You are {pct}% through the guide. Ready for the next phase?"
    return (f"I'm Bridgie{', ' + n if n else ''}! I'll walk through each step with {who}, nice and slowly. "
            "There is no rush and no wrong place to start.")


def suggested_actions(sb):
    goals = [g for g in sb.get("goals", []) if g in GOAL_ACTIONS]
    if sb["role"] == "caregiver" and "caregiving" not in goals:
        goals.append("caregiving")
    for g in DEFAULT_ACTIONS:
        if len(goals) >= 3:
            break
        if g not in goals:
            goals.append(g)
    return [(g,) + GOAL_ACTIONS[g] for g in goals[:3]]


COPY = {
    "patient": {
        "ask": "Tick the questions you would like to bring to your care team. Nothing here is saved anywhere except this browser.",
        "tip": "It can help to write down answers during appointments, or ask someone to join you.",
    },
    "caregiver": {
        "ask": "Tick the questions you would like to ask the care team on their behalf.",
        "tip": "Taking notes and keeping this checklist handy can really help. Always confirm instructions with the care team.",
    },
}
