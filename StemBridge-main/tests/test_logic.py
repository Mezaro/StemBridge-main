import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import date
from journey_visuals import AUTO, ALLO
from chat_knowledge import FAQ, answer
from resource_center import RESOURCES, CATEGORIES
from ui import logic
from ui.storage import _merge, DEFAULT

TOTALS = {"auto": 7, "allo": 8}


def sb_new(**kw):
    s = copy.deepcopy(DEFAULT); s.update(kw); return s


def test_stage_content_parses():
    assert (len(AUTO), len(ALLO)) == (7, 8)
    for items in (AUTO, ALLO):
        for s in items:
            assert len(logic.parse_list(s["tests"])) >= 3
            assert len(logic.parse_list(s["questions"])) >= 3
            assert len(logic.parse_terms(s["terms"])) >= 1


def test_quiz_valid_and_deterministic():
    for items in (AUTO, ALLO):
        for i in range(len(items)):
            q = logic.make_quiz(items, i, seed=1)
            assert q["answer"] in q["options"]
            assert len(set(q["options"])) == len(q["options"]) >= 4
            assert q == logic.make_quiz(items, i, seed=1)


def test_daily_term_stable():
    assert logic.daily_term(AUTO, date(2026, 11, 17)) == logic.daily_term(AUTO, date(2026, 11, 17))


def test_badges_only_no_points():
    assert not hasattr(logic, "sparks") and not hasattr(logic, "level")
    sb = sb_new()
    assert logic.earned(sb, TOTALS) == set()
    sb["visited"]["auto"] = list(range(7)); sb["done"]["auto"] = list(range(7))
    assert {"first", "explorer", "finisher"} <= logic.earned(sb, TOTALS)
    assert logic.percent(sb, "auto", 7) == 100 and logic.next_stage(sb, "allo", 8) == 0


def test_new_badges_celebrated_once():
    sb = sb_new(); sb["visited"]["auto"] = [0]
    assert logic.new_badges(sb, TOTALS) == ["first"]
    sb["seen_badges"].append("first")
    assert logic.new_badges(sb, TOTALS) == []


def test_name_sanitising_blocks_markup_and_length():
    assert logic.clean_name("<b>Sam</b>") == "bSamb"
    assert "<" not in logic.clean_name("<script>alert(1)</script>")
    assert logic.clean_name("Mary-Ann O'Neil Johnson Smithsonian") == "Mary-Ann O'Neil John"
    assert logic.clean_name(123) == "" and logic.clean_name("José") == "José"


def test_personalization_text():
    assert logic.hello(sb_new(name="Sam")) == "Hi, Sam!" and logic.hello(sb_new()) == "Hi there!"
    assert "Sam" in logic.mascot_line(sb_new(name="Sam"), 0)
    assert "loved one" in logic.mascot_line(sb_new(role="caregiver"), 0)
    assert "40%" in logic.mascot_line(sb_new(name="Sam"), 40)


def test_suggested_actions():
    a = logic.suggested_actions(sb_new(goals=["money"]))
    assert a[0][0] == "money" and len(a) == 3 and len({x[0] for x in a}) == 3
    assert "caregiving" in [x[0] for x in logic.suggested_actions(sb_new(role="caregiver"))]
    assert len(logic.suggested_actions(sb_new())) == 3


def test_storage_merge_rejects_bad_data():
    assert _merge("junk") == DEFAULT
    m = _merge({"type": "evil", "role": "caregiver", "done": {"auto": [1, "x", 2, True]}, "checked": ["a", 3],
                "name": "<i>Al</i>", "goals": ["money", "hack"], "onboarded": "yes"})
    assert m["type"] == "auto" and m["role"] == "caregiver" and m["done"]["auto"] == [1, 2]
    assert m["checked"] == ["a"] and m["name"] == "iAli" and m["goals"] == ["money"] and m["onboarded"] is False


def test_chatbot_safety():
    assert "urgent care" in answer("I have a fever and chest pain")[0]
    assert "do not have a reviewed answer" in answer("what stock should I buy")[0]
    for f in FAQ:
        assert answer(f[1][0])[0], f[0]


def test_resources_integrity():
    ids = [r["id"] for r in RESOURCES]
    assert len(ids) == len(set(ids))
    assert all(r["category"] in CATEGORIES and r["url"].startswith("https://") for r in RESOURCES)
