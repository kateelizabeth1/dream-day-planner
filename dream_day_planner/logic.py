import random

from .data import ACTIVITIES, BUDGET_ORDER, FOODS, SONGS, TWISTS


def score(item, answers):
    """Give one point for each answer that matches an item's tags."""
    points = 0
    for key, value in answers.items():
        tag = item.get(key)
        if tag is None:
            continue

        if key == "setting" and value == "both":
            continue
        if isinstance(tag, list):
            if value in tag:
                points += 1
        elif tag == value:
            points += 1
    return points


def passes_filters(item, answers):
    """Apply hard constraints that must not be violated by a recommendation."""
    item_cost = item.get("budget")
    if item_cost is not None:
        item_cost_rank = BUDGET_ORDER.get(item_cost)
        answer_cost_rank = BUDGET_ORDER.get(answers["budget"])
        if item_cost_rank is None or answer_cost_rank is None:
            return False
        if item_cost_rank > answer_cost_rank:
            return False

    item_group = item.get("group")
    if item_group is not None and answers["group"] not in item_group:
        return False

    item_setting = item.get("setting")
    if item_setting is not None:
        if answers["setting"] != "both" and answers["setting"] != item_setting:
            return False

    return True


def pick(items, answers, top_n=3, exclude=None):
    """Filter, rank, then randomly choose from the strongest candidates."""
    pool = [item for item in items if passes_filters(item, answers)]

    if exclude is not None:
        pool_without_exclusion = [
            item for item in pool
            if item.get("name", item.get("title")) != exclude
        ]
        if pool_without_exclusion:
            pool = pool_without_exclusion

    if not pool:
        return None

    ranked = sorted(pool, key=lambda item: score(item, answers), reverse=True)
    return random.choice(ranked[:top_n])


def pick_twist(twists_list, answers, activity_name=""):
    """Choose a twist that does not duplicate the chosen activity too closely."""
    activity_words = {word.lower() for word in activity_name.split() if len(word) > 4}

    for _ in range(10):
        twist = pick(twists_list, answers)
        if twist is None:
            return None

        twist_words = {word.lower() for word in twist["name"].split() if len(word) > 4}
        if not (activity_words & twist_words):
            return twist

    return twist


def build_day(energy, vibe, setting, flavor, group, budget, decade):
    values = (energy, vibe, setting, flavor, group, budget, decade)
    if any(value is None or value == "" for value in values):
        return None, "Please answer every question first. 🙂"

    answers = {
        "energy": energy,
        "vibe": vibe,
        "setting": setting,
        "flavor": flavor,
        "group": group,
        "budget": budget,
        "decade": decade,
    }

    food = pick(FOODS, answers)
    activity = pick(ACTIVITIES, answers)
    songs = [song for song in SONGS if song["decade"] == decade]
    song = pick(songs or SONGS, answers)
    twist = pick_twist(TWISTS, answers, activity["name"] if activity else "")

    if None in (food, activity, song, twist):
        return None, "We couldn't find a matching plan. Please try a different budget or setting."

    return {
        "food": food,
        "activity": activity,
        "song": song,
        "twist": twist,
    }, None
