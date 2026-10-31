from dream_day_planner.rendering import render_day_card, render_error


def test_error_message_escapes_html():
    output = render_error("<script>alert('bad')</script>")
    assert "<script>" not in output
    assert "&lt;script&gt;" in output


def test_day_card_includes_selected_setting_and_song_link():
    plan = {
        "food": {"name": "Fresh fruit"},
        "activity": {"name": "Photo walk"},
        "song": {"title": "As It Was", "artist": "Harry Styles"},
        "twist": {"name": "Write a note"},
    }
    output = render_day_card("chill", "creative", "solo", "outdoors", plan)
    assert "outdoors" in output
    assert "youtube.com/results?search_query=As+It+Was+Harry+Styles" in output
