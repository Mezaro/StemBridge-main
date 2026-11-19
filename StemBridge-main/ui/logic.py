"""Pure logic (no Streamlit): terms, quiz, gamification, copy. Unit-testable."""
import random
import re
from datetime import date

TERM_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.+)$")
LEVELS = [(0, "Seedling"), (40, "Explorer"), (110, "Navigator"), (200, "Bridge Builder")]

BADGES = [
    ("first", "🌟", "First Step", "Open any journey phase"),
    ("explorer", "🧭", "Explorer", "Visit every phase of your journey"),
    ("asker", "❓", "Question Keeper", "Tick 5 questions for your team"),
    ("quiz", "🧠", "Word Wizard", "Answer 3 word quizzes correctly"),
    ("finisher", "🏁", "Journey Finisher", "Mark every phase as read"),
    ("saver", "⭐", "Resource Saver", "Save a resource"),
]


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


def sparks(sb):
    v = sum(len(x) for x in sb["visited"].values())
    d = sum(len(x) for x in sb["done"].values())
    return 5 * v + 15 * d + 10 * len(sb["quiz"]) + 2 * len(sb["checked"]) + 5 * len(sb["bookmarks"])


def level(points):
    name, nxt = LEVELS[0][1], None
    for i, (thr, nm) in enumerate(LEVELS):
        if points >= thr:
            name = nm
            nxt = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    return name, nxt


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


def percent(sb, key, total):
    return round(100 * len(set(sb["done"][key])) / total) if total else 0


def next_stage(sb, key, total):
    done = set(sb["done"][key])
    for i in range(total):
        if i not in done:
            return i
    return total - 1


COPY = {
    "patient": {
        "hello": "Hi, I'm Bridgie! Let's learn about your transplant journey, one step at a time.",
        "ask": "Tick the questions you want to bring to your care team.",
        "tip": "Write down your answers during appointments, or ask someone to help you.",
    },
    "caregiver": {
        "hello": "Hi, I'm Bridgie! Let's help you understand the journey so you can support your loved one.",
        "ask": "Tick the questions you want to ask the care team on their behalf.",
        "tip": "Take notes, keep this checklist handy, and confirm every instruction with the care team.",
    },
}
