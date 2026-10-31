# Dream Day Planner

A Gradio app that creates a personalized dream day from mood, budget, setting, group, food, and music preferences.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Open `http://localhost:7860`.

## Project structure

- `app.py` — application entry point
- `dream_day_planner/app.py` — Gradio interface
- `dream_day_planner/data.py` — foods, activities, songs, twists, and themes
- `dream_day_planner/logic.py` — filtering, matching, and selection logic
- `dream_day_planner/rendering.py` — HTML and text rendering
- `tests/` — focused logic and rendering tests
