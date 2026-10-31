import html
from urllib.parse import quote_plus

from .data import THEMES


def render_error(message):
    escaped = html.escape(message)
    return f"""
    <div style="font-family:Arial,sans-serif;padding:16px;border-radius:12px;
                background:#ffe8e8;color:#222">
      {escaped}
    </div>"""


def render_day_card(energy, vibe, group, setting, plan):
    song = plan["song"]
    query = quote_plus(f"{song['title']} {song['artist']}")
    song_link = f"https://www.youtube.com/results?search_query={query}"

    theme = THEMES.get(vibe, {"bg": "#fff6e5", "accent": "#d9480f"})
    bg_color = theme["bg"]
    accent_color = theme["accent"]
    escaped = html.escape

    return f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:10px auto;
                padding:24px;border-radius:20px;background:{bg_color};color:#222;
                box-shadow:0 4px 14px rgba(0,0,0,0.12)">
      <h2 style="margin:0 0 4px 0;text-align:center;color:{accent_color}">✨ Your Dream Day ✨</h2>
      <p style="text-align:center;margin:0 0 18px 0;color:#777;font-size:14px">
        {escaped(energy)} · {escaped(vibe)} · {escaped(setting)} · {escaped(group)}
      </p>

      <div style="background:#fff;border-radius:12px;padding:12px 16px;margin-bottom:10px">
        <div style="font-size:13px;color:#999">🍽️ FOOD</div>
        <div style="font-size:17px">{escaped(plan['food']['name'])}</div>
      </div>

      <div style="background:#fff;border-radius:12px;padding:12px 16px;margin-bottom:10px">
        <div style="font-size:13px;color:#999">🎈 ACTIVITY</div>
        <div style="font-size:17px">{escaped(plan['activity']['name'])}</div>
      </div>

      <div style="background:#fff;border-radius:12px;padding:12px 16px;margin-bottom:10px">
        <div style="font-size:13px;color:#999">🎵 SONG</div>
        <div style="font-size:17px">{escaped(song['title'])} by {escaped(song['artist'])}</div>
        <a href="{song_link}" target="_blank" rel="noopener noreferrer"
           style="font-size:13px;color:{accent_color};font-weight:bold">
          ▶ Listen on YouTube
        </a>
      </div>

      <div style="background:#ffe066;border-radius:12px;padding:12px 16px">
        <div style="font-size:13px;color:#7a5c00">🎲 SURPRISE TWIST</div>
        <div style="font-size:17px">{escaped(plan['twist']['name'])}</div>
      </div>
    </div>"""


def day_as_text(title, plan, why=""):
    return (
        f"{title}\n\n"
        f"Food: {plan['food']['name']}\n"
        f"Activity: {plan['activity']['name']}\n"
        f"Song: {plan['song']['title']} by {plan['song']['artist']}\n"
        f"Surprise twist: {plan['twist']['name']}\n\n"
        f"{why}".rstrip()
    )
