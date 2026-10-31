import gradio as gr

from .logic import build_day
from .rendering import render_day_card, render_error

CUSTOM_CSS = """
.dream-app { background: linear-gradient(135deg, #fffaf4 0%, #fff0f5 30%, #f2f4ff 100%); min-height: 100vh; font-family: 'Inter', 'Segoe UI', sans-serif; }
.hero { padding: 20px 20px 8px; text-align: center; }
.hero h1 { margin: 0; font-size: 2.7rem; line-height: 1.1; font-weight: 800; color: #2d1b69; }
.hero p { margin: 10px auto 0; color: #5a5576; max-width: 680px; font-size: 1.05rem; }
.panel { background: rgba(255,255,255,0.72); border: 1px solid rgba(120, 134, 171, 0.18); border-radius: 22px; box-shadow: 0 18px 45px rgba(80, 58, 120, 0.08); backdrop-filter: blur(12px); }
.question-panel { padding: 18px 18px 8px; }
.result-panel { padding: 18px; }
.gradio-container { max-width: 1200px !important; }
.form-label { font-weight: 700 !important; color: #2d1b69 !important; }
.gr-button-primary { background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important; border: none !important; box-shadow: 0 10px 20px rgba(159, 91, 252, 0.25) !important; color: white !important; font-weight: 700 !important; }
.gr-button-secondary { background: white !important; border: 1px solid rgba(130, 140, 174, 0.4) !important; color: #2d1b69 !important; font-weight: 600 !important; }
@media (max-width: 768px) { .hero h1 { font-size: 2rem; } }
"""

PLACEHOLDER = """
<div class="panel result-panel" style="min-height:600px;display:flex;align-items:center;justify-content:center;color:#5a5576;font-size:1rem">
  Your dream day will appear here.
</div>
"""


def generate_output(energy, vibe, setting, flavor, group, budget, decade):
    plan, error = build_day(energy, vibe, setting, flavor, group, budget, decade)
    if error:
        return render_error(error)
    return render_day_card(energy, vibe, group, setting, plan)


def reset_inputs():
    return [None] * 7 + [PLACEHOLDER]


def create_app():
    with gr.Blocks(title="Dream Day Planner", css=CUSTOM_CSS, theme=gr.themes.Soft(), elem_classes=["dream-app"]) as app:
        gr.HTML("""
        <div class="hero">
            <h1>🌈 Dream Day Planner</h1>
            <p>Pick your vibe, budget, and mood — and we'll build a perfectly dreamy day with food, activity, music, and a fun surprise twist.</p>
        </div>
        """)

        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                with gr.Column(elem_classes=["panel", "question-panel"]):
                    gr.HTML('<h3 style="margin:0 0 16px;color:#2d1b69">Your mood check-in</h3>')
                    energy = gr.Radio(["sleepy", "chill", "pumped", "chaotic"], label="1. What's your energy today?")
                    vibe = gr.Radio(["cozy", "adventurous", "social", "creative"], label="2. Pick a vibe")
                    setting = gr.Radio(["indoors", "outdoors", "both"], label="3. Indoors or outdoors?")
                    flavor = gr.Radio(["sweet", "salty", "spicy", "fresh"], label="4. Pick a flavor")
                    group = gr.Radio(["solo", "one person", "group"], label="5. Solo or with people?")
                    budget = gr.Radio(["free", "cheap", "treat"], label="6. Budget")
                    decade = gr.Radio(["80s", "90s", "2000s", "now"], label="7. Pick a decade for your soundtrack")

                    inputs = [energy, vibe, setting, flavor, group, budget, decade]
                    with gr.Row():
                        build_btn = gr.Button("✨ Build my day", variant="primary")
                        reroll_btn = gr.Button("🔄 Reroll", variant="secondary")
                        reset_btn = gr.Button("↩️ Start over", variant="secondary")

            with gr.Column(scale=1):
                output = gr.HTML(value=PLACEHOLDER)

        build_btn.click(generate_output, inputs, output)
        reroll_btn.click(generate_output, inputs, output)
        reset_btn.click(reset_inputs, None, inputs + [output])

    return app
