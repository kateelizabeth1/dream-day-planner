from dream_day_planner.logic import build_day, passes_filters


def test_outdoor_setting_filters_indoor_activity():
    item = {"name": "Blanket fort", "setting": "indoors"}
    answers = {
        "budget": "free",
        "group": "solo",
        "setting": "outdoors",
    }
    assert not passes_filters(item, answers)


def test_both_setting_accepts_any_activity():
    for setting in ("indoors", "outdoors"):
        item = {"name": "An activity", "setting": setting}
        answers = {"budget": "free", "group": "solo", "setting": "both"}
        assert passes_filters(item, answers)


def test_budget_does_not_allow_more_expensive_items():
    item = {"name": "Restaurant meal", "budget": "treat"}
    answers = {"budget": "free", "group": "solo", "setting": "indoors"}
    assert not passes_filters(item, answers)


def test_build_day_returns_plan_for_valid_answers():
    plan, error = build_day("chill", "cozy", "outdoors", "fresh", "solo", "free", "90s")
    assert error is None
    assert plan["activity"]["setting"] == "outdoors"
    assert plan["song"]["decade"] == "90s"


def test_build_day_rejects_missing_answers():
    plan, error = build_day(None, "cozy", "both", "sweet", "solo", "free", "80s")
    assert plan is None
    assert "answer every question" in error
