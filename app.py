import base64
import io
import json
from datetime import date
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageOps

# ---- Edit these ----
NAME = "Raman"
BIRTHDAY = date(2026, 11, 2)
MESSAGE = "Wishing you a year full of laughter, good food and everything you love."
# --------------------

BASE = Path(__file__).parent


def ordinal(n):
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


st.set_page_config(page_title=f"Happy Birthday {NAME}", page_icon="🎂", layout="centered")
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    .stApp {background: #150a2b;}
    iframe {border: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_photos():
    out = []
    folder = BASE / "photos"
    if not folder.exists():
        return out
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            img.thumbnail((640, 640))
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=80)
            out.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
    return out


@st.cache_data
def load_song():
    f = BASE / "song.mp3"
    if f.exists():
        return "data:audio/mpeg;base64," + base64.b64encode(f.read_bytes()).decode()
    return None


data = {
    "name": NAME,
    "message": MESSAGE,
    "dateLong": f"{BIRTHDAY.day} {BIRTHDAY:%B %Y}",
    "dateShort": f"{ordinal(BIRTHDAY.day)} {BIRTHDAY:%B}",
    "photos": load_photos(),
    "song": load_song(),
}
html = (BASE / "birthday.html").read_text(encoding="utf-8").replace("__DATA__", json.dumps(data))
components.html(html, height=760, scrolling=False)