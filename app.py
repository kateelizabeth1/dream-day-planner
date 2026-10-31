from dream_day_planner.app import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
