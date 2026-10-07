# Virtual_Tour

Immersive 360° VR tours of Sri Lanka's most breathtaking destinations. Built with **Flask**, **A-Frame**, and **FFmpeg**, with optional AI-generated destination content via **Google Gemini**.

Users browse destinations, build a custom tour order (A → B → C → D), then watch an intro video followed by their selected 360° segments with pause, progress, fullscreen, and VR (Cardboard-style) support.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [How to Run](#how-to-run)
7. [Video Processing Pipeline](#video-processing-pipeline)
8. [Generating Destination Content (Gemini AI)](#generating-destination-content-gemini-ai)
9. [Adding a New Destination](#adding-a-new-destination)
10. [All Source Code](#all-source-code)
    - [app.py](#apppy)
    - [generate_content.py](#generate_contentpy)
    - [compress_videos.py](#compress_videospy)
    - [check_durations.py](#check_durationspy)
    - [run.bat](#runbat)
    - [Commands guide.txt](#commands-guidetxt)
    - [templates/index.html](#templatesindexhtml)
    - [templates/destination.html](#templatesdestinationhtml)
    - [static/style.css](#staticstylecss)
    - [destination_content.json](#destination_contentjson)
11. [Troubleshooting](#troubleshooting)
12. [Deployment Notes](#deployment-notes)
13. [Browser / VR Support](#browser--vr-support)

---

## Overview

Virtual_Tour is a Flask-based web application that lets users explore Sri Lanka through immersive 360° videos. Users can:

- Browse destination cards (Colombo is live; Galle, Sigiriya, Ella, Kandy are "Coming soon")
- Pick a **custom tour order** of 4 locations (A/B/C/D buttons, numbered steps)
- Watch an intro video first, then their selected segments in the chosen order
- Use fullscreen, VR (split-screen WebXR) mode, pause/play, and a live progress bar
- Save destinations to a wishlist (`localStorage`) and share links (Web Share API)
- Fall back to the default segment order if no custom order is picked

The server runs over **HTTPS** using locally generated mkcert certificates (`10.159.155.140+2.pem`), which is required for WebXR/VR features on headsets over LAN.

---

## Project Structure

```
VirtualTour 2/
├── app.py                        # Flask server (routes + destination data)
├── generate_content.py           # Gemini AI content generator
├── compress_videos.py            # FFmpeg 360° video compressor (4K, CRF 18)
├── check_durations.py            # Verify raw vs compressed video durations
├── run.bat                       # Windows one-click launcher
├── Commands guide.txt            # Manual run guide (local + ngrok)
├── destination_content.json      # Generated tourism content (Gemini output)
├── mkcert.exe                    # Local HTTPS certificate tool
├── 10.159.155.140+2.pem          # SSL certificate (mkcert generated)
├── 10.159.155.140+2-key.pem      # SSL private key (mkcert generated)
├── raw_footage/                  # Original 360° videos (equirectangular)
│   ├── intro.mp4
│   ├── independence_square.mp4
│   ├── planetarium.mp4
│   ├── port_city.mp4
│   └── viharamahadevi_park.mp4
├── static/                       # Served assets
│   ├── style.css
│   ├── intro_compressed.mp4
│   ├── independence_square_compressed.mp4
│   ├── planetarium_compressed.mp4
│   ├── port_city_compressed.mp4
│   ├── viharamahadevi_park_compressed.mp4
│   └── photos/
│       ├── colombo.jpg
│       ├── galle.jpg
│       ├── sigiriya.png
│       ├── ella.png
│       └── kandy.png
└── templates/
    ├── index.html                # Home / destination grid
    └── destination.html          # 360° player + order builder
```

---

## Features

- **360° Video Playback** via A-Frame `<a-videosphere>` with A-Frame 1.5.0
- **Custom Tour Builder** — pick locations A/B/C/D in your preferred order
- **Intro-first playback** — the intro video plays before your chosen segments
- **Fallback order** — if no order is picked, all locations play in default order
- **Player controls** — pause/play, live progress bar, fullscreen, VR toggle
- **Wishlist** via `localStorage` (heart button persists between visits)
- **Share** via Web Share API with clipboard fallback
- **Glassmorphism UI** — Montserrat + Inter fonts, teal accent (`#00dbe7`)
- **Responsive** — tablet and mobile breakpoints (768px, 480px)
- **Accessibility** — skip link, ARIA label on nav, focus-visible outlines, 44px touch targets
- **HTTPS with mkcert** for VR headset access on LAN

---

## Requirements

- Python 3.11
- Flask
- google-genai (only for `generate_content.py`)
- imageio-ffmpeg (only for `check_durations.py`)
- FFmpeg on system PATH (used by `compress_videos.py`)
- A modern browser (Chrome/Edge recommended for WebXR)

```powershell
pip install flask google-genai imageio-ffmpeg
```

---

## Installation

```powershell
cd "C:\Users\induw\Desktop\VirtualTour 2"
pip install flask google-genai imageio-ffmpeg
```

---

## How to Run

### Option 1 — Batch file (easiest on Windows)

Double-click `run.bat`. It runs `py -3.11 app.py` and pauses on exit.

### Option 2 — Local (same PC)

```powershell
py -3.11 app.py
```

Then open: `https://localhost:5000`

> The app serves **HTTPS only** because `ssl_context` is set in `app.py`. Your browser will warn about the self-signed certificate — accept/continue to proceed.

### Option 3 — Network / VR headset (ngrok)

1. Terminal 1:
   ```powershell
   py -3.11 app.py
   ```
2. Terminal 2:
   ```powershell
   ngrok http 5000
   ```
3. Open the ngrok URL on your headset or phone.

The original walkthrough (see `Commands guide.txt`):

```
Normal Run in Same PC:
    1. cd Documents\VirtualTour 2
    2. py -3.11 app.py
    3. open browser and paste this link: http://localhost:5000

Run using virtual server:
    1. First open CMD and run: cd Documents\VirtuTour
    2. py -3.11 app.py
    3. open new CMD and run: cd Documents\VirtuTour
    4. .\ngrok http 5000
    5. open this link: https://revenge-expend-degreases.ngrok-free.dev

if user give not answer continue video segments according to the order we give.
```

---

## Video Processing Pipeline

360° footage must be **equirectangular** (2:1 aspect ratio) for `<a-videosphere>` to render correctly.

1. Put raw 360° videos in `raw_footage/` (`.mp4`, `.mov`, or `.mkv`).
2. Run the compressor:

   ```powershell
   py -3.11 compress_videos.py
   ```

3. Compressed files land in `static/` as `<name>_compressed.mp4` with:
   - Resolution: `3840:1920` (4K 360°)
   - Codec: `libx264`, CRF 18 (visually lossless), preset `medium`
   - Audio: AAC 128k
   - `+faststart` for progressive web streaming
4. Verify durations match:

   ```powershell
   py -3.11 check_durations.py
   ```

Expected output example:

```
intro.mp4: original=30.0s, compressed=30.0s
port_city.mp4: original=45.2s, compressed=45.2s
...
```

---

## Generating Destination Content (Gemini AI)

`generate_content.py` uses the Gemini API to write `about`, `history`, `weather`, and `tips` for each place, saving everything to `destination_content.json`.

1. Get an API key from Google AI Studio.
2. Set it and run:

   ```powershell
   $env:GEMINI_API_KEY="your_key_here"
   py -3.11 generate_content.py
   ```

3. Output is saved to `destination_content.json`. Copy the generated fields into the `DESTINATIONS` dict in `app.py` as needed.

The prompt forces strict JSON output; if parsing fails, raw text is stored under a `"raw"` key instead.

---

## Adding a New Destination

1. Add an entry to `DESTINATIONS` in `app.py`:

   ```python
   "galle": {
       "name": "Galle Fort",
       "location": "Galle, Sri Lanka",
       "duration": "12 min",
       "temperature": "26-30°C",
       "region": "Southern Province",
       "type": "Heritage",
       "entry_fee": "Free",
       "image": "/static/photos/galle.jpg",
       "video": "/static/intro_compressed.mp4",
       "intro_video": "/static/intro_compressed.mp4",
       "segments": [ ... ],
       "about": "...",
       "history": "...",
       "weather": "...",
       "tips": "...",
       "active": True
   }
   ```

2. The card automatically appears on the home page (`templates/index.html` loops over `DESTINATIONS`).
3. For a custom segment list, update the `allLocations` array in `templates/destination.html` (or template it from the destination's `segments`).

---

## All Source Code

### app.py

```python
import os
from flask import Flask, render_template

app = Flask(__name__)

DESTINATIONS = {
    "colombo": {
        "name": "Colombo City",
        "location": "Colombo, Sri Lanka",
        "duration": "10 min",
        "temperature": "27-32°C",
        "region": "Western Province",
        "type": "Urban",
        "entry_fee": "Free",
        "image": "/static/photos/colombo.jpg",
        "video": "/static/intro_compressed.mp4",
        "intro_video": "/static/intro_compressed.mp4",
        "segments": [
            {
                "id": "port_city",
                "option": "A",
                "category": "SEAFRONT",
                "name": "Port City",
                "keywords": ["port city", "port"],
                "video": "/static/port_city_compressed.mp4"
            },
            {
                "id": "independence_square",
                "option": "B",
                "category": "COLOMBO",
                "name": "Independence Square",
                "keywords": ["independence square", "independence", "square"],
                "video": "/static/independence_square_compressed.mp4"
            },
            {
                "id": "planetarium",
                "option": "C",
                "category": "SCIENCE",
                "name": "Planetarium",
                "keywords": ["planetarium"],
                "video": "/static/planetarium_compressed.mp4"
            },
            {
                "id": "viharamahadevi_park",
                "option": "D",
                "category": "GREEN SPACE",
                "name": "Viharamahadevi Park",
                "keywords": ["viharamahadevi park", "viharamahadevi", "park"],
                "video": "/static/viharamahadevi_park_compressed.mp4"
            }
        ],
        "about": "A modern waterfront development redefining Colombo's skyline, blending futuristic architecture with the Indian Ocean coastline.",
        "history": "One of the largest urban development projects in South Asia, transforming reclaimed land into a new financial and residential hub.",
        "weather": "Tropical coastal climate, 27-32°C. Evenings are cooler with sea breeze.",
        "tips": "Visit in the evening for skyline lighting. Great for photography enthusiasts.",
        "active": True
    },
}

PLACEHOLDER_CARDS = [
    {"name": "Galle Fort", "location": "Sri Lanka", "duration": "12 min", "image": "/static/photos/galle.jpg"},
    {"name": "Sigiriya Rock Fortress", "location": "Sri Lanka", "duration": "12 min", "image": "/static/photos/sigiriya.png"},
    {"name": "Ella", "location": "Sri Lanka", "duration": "15 min", "image": "/static/photos/ella.png"},
    {"name": "Kandy Lake", "location": "Sri Lanka", "duration": "10 min", "image": "/static/photos/kandy.png"},
]

@app.route("/")
def index():
    return render_template("index.html", destinations=DESTINATIONS, placeholders=PLACEHOLDER_CARDS)

@app.route("/destination/<slug>")
def destination(slug):
    dest = DESTINATIONS.get(slug)
    if not dest:
        return "Destination not found", 404
    return render_template("destination.html", dest=dest, slug=slug)

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
        host="0.0.0.0",
        ssl_context=("10.159.155.140+2.pem", "10.159.155.140+2-key.pem")
    )
```

**Routes**

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page with destination + placeholder cards |
| `/destination/<slug>` | GET | 360° player page for a destination (404 if unknown) |
| `/static/*` | GET | Compressed videos, CSS, photos |

**Environment variables**

| Variable | Default | Description |
|---|---|---|
| `FLASK_DEBUG` | `0` | Set to `1` to enable Flask debug mode |
| `GEMINI_API_KEY` | — | Required only by `generate_content.py` |

---

### generate_content.py

```python
from google import genai
import json
import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY is not set. See README 5.5.")

client = genai.Client(api_key=api_key)

PLACES = {
    "colombo": "Colombo Port City, Sri Lanka",
    "galle-fort": "Galle Fort, Sri Lanka",
    "sigiriya": "Sigiriya Rock Fortress, Sri Lanka",
    "ella": "Ella, Sri Lanka",
    "kandy-lake": "Kandy Lake, Sri Lanka",
}


def generate_info(place_name):
    prompt = f"""Write short tourism information about {place_name}.
Respond ONLY with valid JSON in this exact format, no other text, no markdown formatting:
{{
  "about": "2-3 sentences about what this place is",
  "history": "2-3 sentences about its history or culture",
  "weather": "1-2 sentences about typical weather/climate there",
  "tips": "1-2 sentences of practical visitor tips"
}}"""

    response = client.models.generate_content(
               model="gemini-3.5-flash-lite",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


results = {}
for slug, place_name in PLACES.items():
    print(f"Generating content for {place_name}...")
    text = generate_info(place_name)
    try:
        results[slug] = json.loads(text)
    except json.JSONDecodeError:
        print(f"Could not parse response for {place_name}, raw text saved instead.")
        results[slug] = {"raw": text}

with open("destination_content.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nDone! Saved to destination_content.json")
```

---

### compress_videos.py

```python
import os
import subprocess

INPUT_FOLDER = "raw_footage"
OUTPUT_FOLDER = "static"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.exists(INPUT_FOLDER):
    print(f"Error: Input folder '{INPUT_FOLDER}' not found.")
    exit()

video_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith((".mp4", ".mov", ".mkv"))]

if not video_files:
    print(f"No video files found in '{INPUT_FOLDER}'.")
    exit()

print(f"Found {len(video_files)} video(s) to compress (HIGH QUALITY).\n")

for filename in video_files:
    input_path = os.path.join(INPUT_FOLDER, filename)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_compressed.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # HIGH QUALITY settings:
    # - scale=3840:1920 (4K 360°, good balance)
    #   OR scale=-2:1920 (if you want to keep original aspect ratio, height=1920)
    # - crf 18 (visually lossless for most content)
    # - preset medium (better compression than 'fast')
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale=3840:1920",   # 4K 360° resolution
        "-c:v", "libx264",
        "-crf", "18",               # Higher quality (lower = better)
        "-preset", "medium",        # Better quality/size trade-off
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-y",
        output_path
    ]

    print(f"Compressing: {filename} -> {output_filename} (4K, CRF 18)")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Success: {output_path}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compressing {filename}: {e}\n")

print("All done!")
```

---

### check_durations.py

```python
import imageio_ffmpeg
import subprocess
import os
import re

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

def get_duration(path):
    cmd = [ffmpeg_path, "-i", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        h, m, s = match.groups()
        total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
        return f"{total_seconds:.1f}"
    return "unknown"

pairs = [
    ("raw_footage/intro.mp4", "static/intro_compressed.mp4"),
    ("raw_footage/port_city.mp4", "static/port_city_compressed.mp4"),
    ("raw_footage/independence_square.mp4", "static/independence_square_compressed.mp4"),
    ("raw_footage/planetarium.mp4", "static/planetarium_compressed.mp4"),
    ("raw_footage/viharamahadevi_park.mp4", "static/viharamahadevi_park_compressed.mp4"),
]

for original, compressed in pairs:
    if os.path.exists(original) and os.path.exists(compressed):
        orig_dur = get_duration(original)
        comp_dur = get_duration(compressed)
        print(f"{os.path.basename(original)}: original={orig_dur}s, compressed={comp_dur}s")
    else:
        print(f"Missing file(s) for: {original} / {compressed}")
```

---

### run.bat

```bat
@echo off
cd /d "%~dp0"
echo Starting VirtualTour...
py -3.11 app.py
pause
```

---

### Commands guide.txt

```text
Normal Run in Same PC:

	1.  cd Documents\VirtualTour 2
	2.  py -3.11 app.py
	3. open browser and paste this link : http://localhost:5000

Run using virtual server :
	
	1. Frist Open CMD and run : cd Documents\VirtuTour
	2. py -3.11 app.py
	3. open new CMD and run : cd Documents\VirtuTour
	4. .\ngrok http 5000
	5. open this link : https://revenge-expend-degreases.ngrok-free.dev


if user give not answer continue video segments according to the order we give.
```

---

### templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Virtual_Tour</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to content</a>
    <header>
        <div class="logo">🌐 Virtual_<span>Tour</span></div>
        <nav aria-label="Main navigation">
            <a href="/" class="glass-btn glass-btn-sm">Explore</a>
            <a href="#" class="glass-btn glass-btn-sm">Popular</a>
            <a href="#" class="glass-btn glass-btn-sm">About</a>
        </nav>
    </header>

    <main id="main-content">
        <h1>Explore Sri Lanka in VR</h1>
        <p class="subtitle">Immersive 360° tours of Sri Lanka's most breathtaking destinations</p>

        <div class="grid">
            {% for slug, dest in destinations.items() %}
            <a href="/destination/{{ slug }}" class="card">
                 <img src="{{ dest.image }}" alt="{{ dest.name }}" loading="lazy" width="400" height="220">
                <div class="hover-play">&#9654;</div>
                <div class="badge">{{ dest.duration }}</div>
                <div class="card-body">
                    <h3>{{ dest.name }}</h3>
                    <p>{{ dest.location }}</p>
                </div>
            </a>
            {% endfor %}

            {% for p in placeholders %}
            <div class="card disabled">
                <img src="{{ p.image }}" alt="{{ p.name }}" loading="lazy" width="400" height="220">
                <div class="badge">{{ p.duration }}</div>
                <div class="card-body">
                    <h3>{{ p.name }}</h3>
                    <p>Coming soon</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </main>

    <footer>© 2026 Virtual_Tour. Explore responsibly.</footer>
</body>
</html>
```

---

### templates/destination.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ dest.name }} - Virtual_Tour</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
    <style>
        /* ---- Order builder UI ---- */
        .order-builder {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            margin: 14px 0 10px;
            padding: 0 10px;
        }
        .order-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            width: 100%;
            max-width: 600px;
        }
        .order-btn {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 30px;
            padding: 10px 22px;
            color: #e2e2e8;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            backdrop-filter: blur(4px);
            flex: 1 0 auto;
            min-width: 100px;
        }
        .order-btn:hover {
            background: rgba(20,184,166,0.2);
            border-color: #14b8a6;
            transform: translateY(-2px);
        }
        .order-btn:active {
            transform: scale(0.97);
        }
        .order-btn .letter {
            color: #14b8a6;
            font-weight: 700;
            margin-right: 6px;
        }
        .order-btn.picked {
            opacity: 0.3;
            pointer-events: none;
            transform: none;
            border-color: rgba(255,255,255,0.05);
            text-decoration: line-through;
        }
        .order-btn.picked .letter {
            color: #849495;
        }
        .order-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            min-height: 32px;
            padding: 8px 14px;
            background: rgba(255,255,255,0.04);
            border-radius: 16px;
            border: 1px dashed rgba(255,255,255,0.1);
            width: 100%;
            max-width: 600px;
            color: #e2e2e8;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
        }
        .order-list .step {
            background: rgba(20,184,166,0.15);
            border: 1px solid rgba(20,184,166,0.3);
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 13px;
            color: #5eead4;
        }
        .order-list .step .num {
            color: #14b8a6;
            font-weight: 700;
            margin-right: 4px;
        }
        .order-hint {
            text-align: center;
            color: #849495;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
        }
        .order-hint .highlight {
            color: #14b8a6;
        }
        .start-tour-btn {
            background: #14b8a6;
            color: #0A0C10;
            border: none;
            border-radius: 30px;
            padding: 12px 32px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            margin-top: 4px;
        }
        .start-tour-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(20,184,166,0.3);
        }
        .start-tour-btn:disabled {
            opacity: 0.3;
            pointer-events: none;
            transform: none;
        }
        .reset-btn {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 8px 18px;
            color: #a3a3a3;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }
        .reset-btn:hover {
            border-color: #14b8a6;
            color: #e2e2e8;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">Virtual_<span>Tour</span></div>
        <nav>
            <a href="/" class="glass-btn glass-btn-sm">Explore</a>
            <a href="#" class="glass-btn glass-btn-sm">Popular</a>
            <a href="#" class="glass-btn glass-btn-sm">About</a>
        </nav>
    </header>

    <main>
        <a href="/" class="back-link">&larr; Back to Destinations</a>

        <div class="video-wrapper">
            <!-- Play overlay (intro) -->
            <div class="play-overlay" id="playOverlay" onclick="startIntro()">
                <div class="play-circle">▶</div>
                <div>Click to start from intro</div>
            </div>

            <!-- A-Frame scene -->
            <a-scene embedded
                     vr-mode-ui="enabled: false"
                     renderer="antialias: true; colorManagement: true; highRefreshRate: true"
                     loading-screen="dotsColor: #00dbe7; backgroundColor: #0A0C10">
                <a-assets>
                    <video id="video360" playsinline webkit-playsinline preload="auto" src="{{ dest.intro_video or dest.video }}"></video>
                </a-assets>
                <a-videosphere rotation="0 -90 0" src="#video360"></a-videosphere>
            </a-scene>

            <!-- Player bar -->
            <div class="player-bar">
                <button id="pauseBtn" class="mini-btn" onclick="togglePause()">⏸</button>
                <div class="now-viewing">
                    <div class="now-viewing-label">NOW VIEWING</div>
                    <div class="now-viewing-name" id="nowViewingName">{{ dest.name }}, 360°</div>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <button class="mini-btn" onclick="toggleFullscreen()">⛶</button>
                <button class="mini-btn vr-btn" id="vrBtn" onclick="toggleVR()">🥽</button>
            </div>
        </div>

        <!-- ===== ORDER BUILDER ===== -->
        <div class="order-builder">
            <div class="order-grid" id="orderGrid"></div>
            <div class="order-list" id="orderList">Tap locations below to build your tour order</div>
            <div class="order-hint">
                <span id="orderHint">Choose <span class="highlight">4 locations</span> in the order you want to watch</span>
            </div>
            <div>
                <button class="start-tour-btn" id="startTourBtn" disabled onclick="startCustomTour()">▶ Start Tour</button>
                <button class="reset-btn" onclick="resetOrder()">↺ Reset</button>
            </div>
        </div>

        <h2 class="dest-title">{{ dest.name }}</h2>
        <p class="dest-location">{{ dest.location }}</p>

        <!-- Save/Share, facts, info cards... -->
        <div class="action-row">
            <button class="glass-btn glass-btn-icon" id="saveBtn" onclick="toggleSave('{{ slug }}')">
                <span id="heartIcon">♥</span>
            </button>
            <button class="glass-btn glass-btn-sm" onclick="shareDestination('{{ dest.name }}', window.location.href)">
                🔗 Share
            </button>
        </div>
        <div class="toast" id="toast"></div>

        <div class="quick-facts">
            <div class="fact-card"><div class="fact-icon">⏱</div><div class="fact-label">Duration</div><div class="fact-value">{{ dest.duration }}</div></div>
            <div class="fact-card"><div class="fact-icon">🌡</div><div class="fact-label">Temperature</div><div class="fact-value">{{ dest.temperature }}</div></div>
            <div class="fact-card"><div class="fact-icon">📍</div><div class="fact-label">Location</div><div class="fact-value">{{ dest.region }}</div></div>
            <div class="fact-card"><div class="fact-icon">🏛</div><div class="fact-label">Type</div><div class="fact-value">{{ dest.type }}</div></div>
            <div class="fact-card"><div class="fact-icon">🎫</div><div class="fact-label">Entry</div><div class="fact-value">{{ dest.entry_fee }}</div></div>
        </div>

        <div class="info-grid">
            <div>
                <div class="info-box" onclick="this.classList.toggle('collapsed')">
                    <h4>About <span class="chevron">▼</span></h4>
                    <div class="content"><p>{{ dest.about }}</p></div>
                </div>
                <div class="info-box" onclick="this.classList.toggle('collapsed')">
                    <h4>History <span class="chevron">▼</span></h4>
                    <div class="content"><p>{{ dest.history }}</p></div>
                </div>
            </div>
            <div>
                <div class="info-box" onclick="this.classList.toggle('collapsed')">
                    <h4>Weather <span class="chevron">▼</span></h4>
                    <div class="content"><p>{{ dest.weather }}</p></div>
                </div>
                <div class="info-box" onclick="this.classList.toggle('collapsed')">
                    <h4>Visitor Info <span class="chevron">▼</span></h4>
                    <div class="content"><p>{{ dest.tips }}</p></div>
                </div>
            </div>
        </div>
    </main>

    <footer>© 2026 Virtual_Tour. Explore responsibly.</footer>

    <script>
        // ================================================================
        // 1. DATA: All available locations
        // ================================================================
        const allLocations = [
            { id: 0, name: "Independence Square", video: "/static/independence_square_compressed.mp4" },
            { id: 1, name: "Planetarium",        video: "/static/planetarium_compressed.mp4" },
            { id: 2, name: "Viharamahadevi Park",video: "/static/viharamahadevi_park_compressed.mp4" },
            { id: 3, name: "Port City",          video: "/static/port_city_compressed.mp4" }
        ];

        let customOrder = [];
        let tourStarted = false;

        const vid = document.getElementById('video360');
        const nowViewing = document.getElementById('nowViewingName');
        const orderGrid = document.getElementById('orderGrid');
        const orderList = document.getElementById('orderList');
        const orderHint = document.getElementById('orderHint');
        const startBtn = document.getElementById('startTourBtn');

        // ================================================================
        // 2. Build the choice buttons
        // ================================================================
        function buildOrderButtons() {
            orderGrid.innerHTML = '';
            allLocations.forEach((loc, index) => {
                const btn = document.createElement('button');
                btn.className = 'order-btn';
                const letter = String.fromCharCode(65 + index);
                btn.innerHTML = `<span class="letter">${letter}</span> ${loc.name}`;
                btn.dataset.id = loc.id;
                if (customOrder.some(item => item.id === loc.id)) {
                    btn.classList.add('picked');
                }
                btn.onclick = () => pickLocation(loc.id);
                orderGrid.appendChild(btn);
            });
        }

        // ================================================================
        // 3. Pick a location (add to custom order)
        // ================================================================
        function pickLocation(id) {
            if (tourStarted) return;
            if (customOrder.some(item => item.id === id)) return;
            if (customOrder.length >= allLocations.length) return;

            const loc = allLocations.find(l => l.id === id);
            if (!loc) return;

            customOrder.push(loc);
            updateUI();
        }

        // ================================================================
        // 4. Update UI after picking
        // ================================================================
        function updateUI() {
            document.querySelectorAll('.order-btn').forEach(btn => {
                const id = parseInt(btn.dataset.id);
                if (customOrder.some(item => item.id === id)) {
                    btn.classList.add('picked');
                } else {
                    btn.classList.remove('picked');
                }
            });

            if (customOrder.length === 0) {
                orderList.innerHTML = 'Tap locations below to build your tour order';
            } else {
                orderList.innerHTML = customOrder.map((loc, i) =>
                    `<span class="step"><span class="num">${i+1}.</span> ${loc.name}</span>`
                ).join(' ');
            }

            const remaining = allLocations.length - customOrder.length;
            if (remaining === 0) {
                orderHint.innerHTML = '✅ All 4 locations selected! Click <span class="highlight">Start Tour</span>';
                startBtn.disabled = false;
            } else {
                orderHint.innerHTML = `Choose <span class="highlight">${remaining} more</span> location${remaining > 1 ? 's' : ''}`;
                startBtn.disabled = true;
            }
        }

        // ================================================================
        // 5. Reset order
        // ================================================================
        function resetOrder() {
            if (tourStarted) return;
            customOrder = [];
            startBtn.disabled = true;
            updateUI();
        }

        // ================================================================
        // 6. Start custom tour — plays intro FIRST, then user order
        // ================================================================
        function startCustomTour() {
            if (tourStarted) return;
            if (customOrder.length < allLocations.length) return;

            tourStarted = true;
            startBtn.disabled = true;
            document.querySelectorAll('.order-btn').forEach(b => b.disabled = true);

            // Hide overlay if visible
            const overlay = document.getElementById('playOverlay');
            overlay.style.display = 'none';

            orderHint.innerHTML = '▶ Playing intro...';
            orderList.innerHTML = customOrder.map((loc, i) =>
                `<span class="step"><span class="num">${i+1}.</span> ${loc.name}</span>`
            ).join(' ');

            // Play intro first
            vid.muted = false;
            vid.src = '{{ dest.intro_video or dest.video }}';
            vid.load();

            const playIntro = () => {
                vid.play().then(() => {
                    nowViewing.innerText = 'Intro, 360°';
                    vid.ontimeupdate = updateProgress;
                    vid.onended = () => {
                        // Intro done → start custom order
                        playCustomSegment(0);
                    };
                }).catch(err => {
                    console.error('Intro error:', err);
                    orderHint.innerHTML = '⚠️ Error playing intro. Try again.';
                    tourStarted = false;
                    startBtn.disabled = false;
                    document.querySelectorAll('.order-btn').forEach(b => b.disabled = false);
                });
            };

            if (vid.readyState >= 3) {
                playIntro();
            } else {
                vid.addEventListener('canplaythrough', function onReady() {
                    vid.removeEventListener('canplaythrough', onReady);
                    playIntro();
                });
                setTimeout(() => {
                    if (vid.paused && vid.readyState > 0) {
                        console.log('Fallback: forcing intro play');
                        playIntro();
                    }
                }, 5000);
            }
        }

        // ================================================================
        // 7. Play custom segment by index
        // ================================================================
        function playCustomSegment(index) {
            if (index >= customOrder.length) {
                nowViewing.innerText = '🎉 Tour complete!';
                document.getElementById('progressFill').style.width = '100%';
                orderHint.innerHTML = '🎉 All done!';
                return;
            }

            const seg = customOrder[index];
            nowViewing.innerText = seg.name + ', 360°';

            vid.src = seg.video;
            vid.muted = false;
            vid.load();
            vid.play().catch(err => console.error('Play error:', err));

            vid.ontimeupdate = updateProgress;
            vid.onended = () => {
                playCustomSegment(index + 1);
            };
        }

        // ================================================================
        // 8. Intro (via play overlay)
        // ================================================================
        function startIntro() {
            if (tourStarted) return;
            tourStarted = true;

            document.querySelectorAll('.order-btn').forEach(b => b.disabled = true);
            startBtn.disabled = true;
            orderHint.innerHTML = '▶ Playing intro...';

            const overlay = document.getElementById('playOverlay');
            overlay.innerHTML = '<div class="play-circle">⏳</div><div>Loading...</div>';
            overlay.style.display = 'flex';

            vid.muted = false;
            vid.src = '{{ dest.intro_video or dest.video }}';
            vid.load();

            const playIt = () => {
                vid.play().then(() => {
                    overlay.style.display = 'none';
                    nowViewing.innerText = 'Intro, 360°';
                    vid.ontimeupdate = updateProgress;
                    vid.onended = () => {
                        // After intro, play user's custom order (if any) or fallback to default order
                        if (customOrder.length === allLocations.length) {
                            playCustomSegment(0);
                        } else {
                            // Fallback: play default order
                            customOrder = [...allLocations];
                            playCustomSegment(0);
                        }
                    };
                }).catch(err => {
                    console.error('Intro error:', err);
                    overlay.innerHTML = '<div class="play-circle">⚠️</div><div>Error. Click to retry.</div>';
                    overlay.style.display = 'flex';
                    overlay.onclick = startIntro;
                });
            };

            if (vid.readyState >= 3) {
                playIt();
            } else {
                vid.addEventListener('canplaythrough', function onReady() {
                    vid.removeEventListener('canplaythrough', onReady);
                    playIt();
                });
                setTimeout(() => {
                    if (vid.paused && vid.readyState > 0) {
                        console.log('Fallback: forcing intro play');
                        playIt();
                    }
                }, 5000);
            }
        }

        // ================================================================
        // 9. Progress bar
        // ================================================================
        function updateProgress() {
            if (vid.duration && isFinite(vid.duration)) {
                const pct = (vid.currentTime / vid.duration) * 100;
                document.getElementById('progressFill').style.width = pct + '%';
            }
        }

        // ================================================================
        // 10. Pause / Resume
        // ================================================================
        function togglePause() {
            const btn = document.getElementById('pauseBtn');
            if (vid.paused) {
                vid.play();
                btn.innerHTML = '⏸';
            } else {
                vid.pause();
                btn.innerHTML = '▶';
            }
        }

        // ================================================================
        // 11. Fullscreen
        // ================================================================
        function toggleFullscreen() {
            const wrapper = document.querySelector('.video-wrapper');
            const isFull = document.fullscreenElement || document.webkitFullscreenElement;
            if (!isFull) {
                (wrapper.requestFullscreen || wrapper.webkitRequestFullscreen).call(wrapper);
            } else {
                (document.exitFullscreen || document.webkitExitFullscreen).call(document);
            }
        }

        // ================================================================
        // 12. VR mode (split-screen)
        // ================================================================
        let vrActive = false;
        const sceneEl = document.querySelector('a-scene');

        function toggleVR() {
            if (!sceneEl) return;
            if (vrActive) {
                sceneEl.exitVR();
                vrActive = false;
                document.getElementById('vrBtn').textContent = '🥽';
            } else {
                sceneEl.enterVR();
                vrActive = true;
                document.getElementById('vrBtn').textContent = '⏹';
            }
        }

        sceneEl.addEventListener('exit-vr', () => {
            vrActive = false;
            document.getElementById('vrBtn').textContent = '🥽';
        });
        sceneEl.addEventListener('enter-vr', () => {
            vrActive = true;
            document.getElementById('vrBtn').textContent = '⏹';
        });

        document.addEventListener('fullscreenchange', () => { if (sceneEl && sceneEl.resize) sceneEl.resize(); });
        document.addEventListener('webkitfullscreenchange', () => { if (sceneEl && sceneEl.resize) sceneEl.resize(); });

        // ================================================================
        // 13. Save / Share
        // ================================================================
        function toggleSave(id) {
            let saved = JSON.parse(localStorage.getItem('wishlist') || '[]');
            const heart = document.getElementById('heartIcon');
            if (saved.includes(id)) {
                saved = saved.filter(s => s !== id);
                heart.innerHTML = '♥';
                document.getElementById('saveBtn').classList.remove('saved');
                showToast('Removed from wishlist');
            } else {
                saved.push(id);
                heart.innerHTML = '❤️';
                document.getElementById('saveBtn').classList.add('saved');
                showToast('Saved to wishlist!');
            }
            localStorage.setItem('wishlist', JSON.stringify(saved));
        }

        function shareDestination(title, url) {
            if (navigator.share) {
                navigator.share({ title, url }).catch(() => {});
            } else {
                navigator.clipboard.writeText(url).then(() => {
                    showToast('Link copied!');
                }).catch(() => {
                    const ta = document.createElement('textarea');
                    ta.value = url;
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand('copy');
                    document.body.removeChild(ta);
                    showToast('Link copied!');
                });
            }
        }

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.classList.add('show');
            clearTimeout(t._timeout);
            t._timeout = setTimeout(() => t.classList.remove('show'), 3000);
        }

        // ================================================================
        // 14. On load
        // ================================================================
        document.addEventListener('DOMContentLoaded', () => {
            buildOrderButtons();
            updateUI();

            const saved = JSON.parse(localStorage.getItem('wishlist') || '[]');
            if (saved.includes('{{ slug }}')) {
                document.getElementById('heartIcon').innerHTML = '❤️';
                document.getElementById('saveBtn').classList.add('saved');
            }
        });
    </script>
</body>
</html>
```

**JavaScript function reference**

| Function | Purpose |
|---|---|
| `buildOrderButtons()` | Renders A/B/C/D pick buttons from `allLocations` |
| `pickLocation(id)` | Adds a location to `customOrder`, refreshes UI |
| `updateUI()` | Syncs picked state, step list, remaining hint, Start button |
| `resetOrder()` | Clears `customOrder` (blocked after tour starts) |
| `startCustomTour()` | Plays intro, then `customOrder` segments in order |
| `playCustomSegment(i)` | Plays segment `i`, chains to `i+1` on `ended` |
| `startIntro()` | Plays intro from the overlay, then order (or default fallback) |
| `updateProgress()` | Moves the progress bar from `timeupdate` |
| `togglePause()` | Pause/resume + button icon swap |
| `toggleFullscreen()` | Fullscreen API with webkit fallback, resizes A-Frame |
| `toggleVR()` | `sceneEl.enterVR()` / `exitVR()` |
| `toggleSave(id)` | Wishlist add/remove in `localStorage` |
| `shareDestination(title, url)` | Web Share API, clipboard fallback |

---

### static/style.css

```css
:root {
    --bg: #0A0C10;
    --surface: #111318;
    --surface-container: #1A1D23;
    --surface-container-high: #282a2e;
    --glass: rgba(26, 29, 37, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);

    --primary: #00dbe7;
    --primary-glow: rgba(0, 219, 231, 0.4);
    --secondary: #2e9fa8;

    --text-heading: #e2e2e8;
    --text-body: #b9cacb;
    --outline: #849495;
    --footer-text: #888;
    --saved-bg: rgba(0, 219, 231, 0.15);
    --saved-border: rgba(0, 219, 231, 0.5);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: var(--bg);
    color: var(--text-body);
    font-family: 'Inter', -apple-system, "Segoe UI", Arial, sans-serif;
}

h1, h2, h3, .logo {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.skip-link {
    position: absolute;
    top: -100%;
    left: 16px;
    background: var(--primary);
    color: var(--bg);
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    z-index: 200;
    text-decoration: none;
}
.skip-link:focus {
    top: 16px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--glass);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--glass-border);
}

.logo {
    font-size: 20px;
    color: var(--text-heading);
}
.logo span { color: var(--primary); }

nav a {
    color: var(--text-body);
    text-decoration: none;
    margin-left: 30px;
    font-size: 15px;
}
nav a:hover { color: var(--primary); }

main { padding: 40px; max-width: 1300px; margin: 0 auto; }

h1 { font-size: 48px; color: var(--text-heading); margin-bottom: 8px; }
.subtitle { color: var(--outline); margin-bottom: 30px; }

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 25px;
}

.card {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    display: block;
    height: 220px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 20px var(--primary-glow);
}
.card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.card:hover img { transform: scale(1.05); }

.card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 70%;
    background: linear-gradient(to top, rgba(0,0,0,0.85), transparent);
}

.card .hover-play {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.2);
    opacity: 0;
    transition: opacity 0.3s ease;
    font-size: 40px;
    color: var(--primary);
    z-index: 2;
}
.card:hover .hover-play { opacity: 1; }

.badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: var(--glass);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: var(--text-heading);
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 16px;
    z-index: 2;
}

.card-body {
    position: absolute;
    bottom: 15px;
    left: 15px;
    right: 15px;
    z-index: 2;
}
.card-body h3 { font-size: 18px; color: var(--text-heading); margin-bottom: 2px; }
.card-body p { font-size: 13px; color: var(--primary); }

.card.disabled { opacity: 0.4; pointer-events: none; }

footer {
    text-align: center;
    padding: 25px;
    color: var(--footer-text);
    font-size: 13px;
    border-top: 1px solid var(--glass-border);
    margin-top: 40px;
}

/* Destination page */
.back-link {
    text-decoration: none;
    display: inline-block;
    margin-bottom: 15px;
    font-size: 14px;
}

.video-wrapper {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #000;
    height: min(420px, 56.25vw);
    min-height: 280px;
}
.video-wrapper a-scene { width: 100%; height: 100%; }

.play-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.3);
    cursor: pointer;
    color: var(--text-heading);
    z-index: 10;
}
.play-circle {
    width: 60px; height: 60px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    margin-bottom: 10px;
}

.info-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
    margin-top: 25px;
}

.info-box, .fact-card {
    background: var(--glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
}

.info-box {
    padding: 18px;
    margin-bottom: 15px;
    cursor: pointer;
}
.info-box h4 {
    margin-bottom: 8px;
    font-size: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.info-box p { color: var(--text-body); font-size: 14px; line-height: 1.5; }
.info-box .content {
    max-height: 500px;
    overflow: hidden;
    transition: max-height 0.3s ease;
}
.info-box.collapsed .content {
    max-height: 0;
}
.info-box .chevron {
    transition: transform 0.3s ease;
    font-size: 14px;
}
.info-box.collapsed .chevron {
    transform: rotate(-90deg);
}

.dest-title { font-size: 26px; color: var(--text-heading); margin-top: 20px; }
.dest-location { margin-bottom: 15px; }

.quick-facts {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 20px 0 30px;
}

.fact-card {
    padding: 14px 10px;
    text-align: center;
    transition: border-color 0.2s ease;
}
.fact-card:hover { border-color: var(--primary); }

.fact-icon { font-size: 22px; margin-bottom: 6px; }
.fact-label { font-size: 12px; color: var(--text-body); margin-bottom: 4px; }
.fact-value { font-size: 14px; color: var(--text-heading); font-weight: 600; }

.action-row {
    display: flex;
    gap: 12px;
    margin: 15px 0 10px;
}

.info-box h4, .dest-location, .back-link, .card-body p { color: var(--primary); }

.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--surface-container);
    border: 1px solid var(--primary);
    color: var(--text-heading);
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 14px;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.3s ease, transform 0.3s ease;
    z-index: 100;
}
.toast.show {
    opacity: 1;
    transform: translateY(0);
}

/* Glassmorphism button system */
.glass-btn {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--glass-border);
    color: var(--text-heading);
    font-weight: 500;
    border-radius: 12px;
    padding: 10px 20px;
    box-shadow:
        0 4px 6px rgba(0, 0, 0, 0.1),
        0 1px 3px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
}
.glass-btn:hover {
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.2),
        0 2px 8px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
}
.glass-btn:active {
    background: rgba(255, 255, 255, 0.05);
    transform: translateY(0) scale(0.98);
    box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.1),
        inset 0 1px 2px rgba(0, 0, 0, 0.2);
}
.glass-btn:focus-visible,
.info-box:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

.glass-btn-icon {
    width: 44px;
    height: 44px;
    padding: 0;
    justify-content: center;
    border-radius: 50%;
    font-size: 18px;
}

.glass-btn-sm {
    padding: 10px 14px;
    font-size: 13px;
    border-radius: 10px;
    min-height: 44px;
}

.glass-btn.saved {
    background: var(--saved-bg);
    border-color: var(--saved-border);
    color: var(--primary);
}

.prompt-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 60px;
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(rgba(10,12,16,0.55), rgba(10,12,16,0.75));
    z-index: 15;
    padding: 30px 20px;
    text-align: center;
}
.prompt-overlay.show { display: flex; }

.prompt-tag {
    color: var(--primary);
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    letter-spacing: 0.1em;
    margin-bottom: 20px;
}

.prompt-heading {
    font-size: 32px;
    line-height: 1.2;
    color: var(--text-heading);
    margin-bottom: 25px;
}
.prompt-heading span { color: var(--primary); }

.segment-list {
    width: 100%;
    max-width: 500px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.segment-item {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 12px 18px;
    cursor: pointer;
    text-align: left;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.segment-item:hover,
.segment-item:focus-visible {
    border-color: var(--primary);
    background: rgba(255,255,255,0.1);
}
.segment-number {
    font-family: 'Montserrat', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--primary);
    min-width: 24px;
}
.segment-text-category {
    font-size: 11px;
    letter-spacing: 0.06em;
    color: var(--primary);
    margin-bottom: 2px;
}
.segment-text-name {
    font-size: 17px;
    font-weight: 600;
    color: var(--text-heading);
}

.player-bar {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 18px;
    background: linear-gradient(transparent, rgba(0,0,0,0.6));
    z-index: 12;
}
.mini-btn {
    background: rgba(0,219,231,0.15);
    border: 1px solid var(--primary);
    color: var(--primary);
    width: 44px;
    height: 44px;
    border-radius: 50%;
    font-size: 12px;
    cursor: pointer;
    flex-shrink: 0;
}
.mini-btn:focus-visible {
    outline: 2px solid var(--primary-glow);
    outline-offset: 2px;
}
.now-viewing {
    min-width: 0;
}
.now-viewing-label {
    font-size: 10px;
    color: var(--primary);
    letter-spacing: 0.05em;
}
.now-viewing-name {
    font-size: 13px;
    color: var(--text-heading);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.progress-track {
    flex: 1;
    height: 3px;
    background: rgba(255,255,255,0.2);
    border-radius: 3px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    width: 0%;
    background: var(--primary);
    transition: width 0.2s linear;
}
.video-wrapper:fullscreen,
.video-wrapper:-webkit-full-screen {
    height: 100vh;
    border-radius: 0;
}
.video-wrapper:fullscreen .prompt-overlay,
.video-wrapper:fullscreen .player-bar,
.video-wrapper:-webkit-full-screen .prompt-overlay,
.video-wrapper:-webkit-full-screen .player-bar {
    z-index: 999;
}
.a-enter-ar-button {
    display: none !important;
}
.a-enter-vr-button {
    display: none !important;
}

/* Responsive — tablet */
@media (max-width: 768px) {
    header {
        padding: 14px 16px;
    }
    nav a {
        margin-left: 16px;
        font-size: 14px;
    }
    main {
        padding: 24px 16px;
    }
    h1 {
        font-size: 34px;
    }
    .info-grid {
        grid-template-columns: 1fr;
    }
    .quick-facts {
        grid-template-columns: repeat(3, 1fr);
    }
    .prompt-heading {
        font-size: 24px;
    }
    .segment-item {
        padding: 10px 14px;
        gap: 12px;
    }
    .segment-text-name {
        font-size: 15px;
    }
}

/* Responsive — mobile */
@media (max-width: 480px) {
    header {
        padding: 12px 12px;
    }
    nav a {
        margin-left: 10px;
        font-size: 13px;
    }
    main {
        padding: 16px 12px;
    }
    h1 {
        font-size: 26px;
    }
    .grid {
        grid-template-columns: 1fr;
    }
    .card {
        height: 200px;
    }
    .quick-facts {
        grid-template-columns: repeat(2, 1fr);
    }
    .player-bar {
        gap: 8px;
        padding: 10px 12px;
    }
    .now-viewing {
        display: none;
    }
    .prompt-heading {
        font-size: 20px;
    }
    .prompt-overlay {
        padding: 20px 12px;
    }
    .segment-list {
        max-width: 100%;
    }
    .action-row {
        flex-wrap: wrap;
    }
    .info-box {
        padding: 14px;
    }
}
```

**Design tokens**

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0A0C10` | Page background |
| `--primary` | `#00dbe7` | Teal accent |
| `--text-heading` | `#e2e2e8` | Headings |
| `--text-body` | `#b9cacb` | Body copy |
| `--glass` | `rgba(26, 29, 37, 0.7)` | Glass surfaces |
| `--glass-border` | `rgba(255, 255, 255, 0.1)` | Glass borders |
| `--primary-glow` | `rgba(0, 219, 231, 0.4)` | Hover glow |

---

### destination_content.json

```json
{
  "colombo": {
    "about": "Colombo Port City is a futuristic, master-planned financial and lifestyle hub reclaimed from the Indian Ocean. It features modern architecture, upscale promenades, and upcoming luxury resorts right next to Sri Lanka's bustling capital.",
    "history": "Construction began in 2014 as a joint venture between the Sri Lankan government and China Harbor Engineering Company to transform the coastline. It represents a bold step into the future, symbolizing modern economic ambition and cosmopolitan culture.",
    "weather": "The climate is tropical and warm year-round, with temperatures typically hovering between 25°C and 30°C. Expect high humidity and occasional tropical downpours, particularly during the monsoon seasons.",
    "tips": "Visit the Port City Marina Promenade in the late afternoon to enjoy cool ocean breezes and stunning sunset views over the Indian Ocean. Wear light, breathable clothing and stay hydrated while exploring the open-air developments."
  },
  "galle-fort": {
    "about": "Galle Fort is a UNESCO World Heritage site located on the southwestern coast of Sri Lanka. This stunning coastal fortification seamlessly blends European architectural styles with South Asian traditions within a vibrant community.",
    "history": "Originally built by the Portuguese in the 16th century, the fort was extensively fortified by the Dutch in the 17th century. Today, its preserved ramparts enclose charming cobblestone streets, colonial-era villas, museums, and boutique cafes.",
    "weather": "The region experiences a tropical climate with warm temperatures year-round. The best time to visit is during the dry season from December to March.",
    "tips": "Wear comfortable walking shoes to explore the historic ramparts and narrow streets on foot. Make sure to stay for the sunset view from the fort walls."
  },
  "sigiriya": {
    "about": "Sigiriya Rock Fortress is an ancient palace and fortress complex rising dramatically from the central plains of Sri Lanka. Designated as a UNESCO World Heritage site, it is world-renowned for its breathtaking summit views, ancient water gardens, and the famous frescoes of celestial maidens.",
    "history": "Built in the 5th century AD by King Kasyapa, the site served as his royal capital and a heavily fortified stronghold. Following the king's death, the fortress was converted into a Buddhist monastery before eventually being abandoned and rediscovered by British explorers in the 19th century.",
    "weather": "The region experiences a tropical climate with warm temperatures year-round, typically ranging from 28°C to 33°C. The best time to visit is during the dry season from January to April to avoid monsoon rains.",
    "tips": "Climb the rock early in the morning to beat the heat and large tour groups, and wear comfortable walking shoes with good grip. Make sure to stay hydrated and protect yourself from the strong sun along the open staircases."
  },
  "ella": {
    "about": "Nestled in Sri Lanka's lush central highlands, Ella is a breathtaking mountain village renowned for its dramatic waterfalls, verdant tea plantations, and stunning panoramic views. It serves as a paradise for nature lovers and hikers seeking scenic trails like Ella Rock and Little Adam's Peak.",
    "history": "Originally a remote and sleepy agricultural settlement, Ella gained prominence during the British colonial era when the surrounding hills were cleared for vast tea estates. Today, it has blossomed into a vibrant cultural hub that blends traditional Sri Lankan hill-country heritage with a welcoming backpacker atmosphere.",
    "weather": "Ella enjoys a pleasant, cooler climate year-round compared to the coastal lowlands, though rain can occur unexpectedly at any time. Mornings are typically crisp and clear, making them ideal for outdoor exploration before afternoon mists roll in.",
    "tips": "Book your train tickets well in advance, as the iconic journey to Ella is considered one of the most scenic rail rides in the world. Pack sturdy walking shoes for the steep trails and a light jacket for cooler evening temperatures."
  },
  "kandy-lake": {
    "about": "Kandy Lake is a picturesque artificial body of water located in the heart of Kandy, Sri Lanka, framed by rolling green hills. Also known as Kiri Muhuda or the Sea of Milk, it offers peaceful walking paths and stunning reflections of the city.",
    "history": "Built in 1807 by the last king of Sri Lanka, Sri Wickrama Rajasinghe, the lake holds significant cultural and spiritual importance. It is situated adjacent to the sacred Temple of the Tooth Relic, making it a central landmark in Sri Lankan heritage.",
    "weather": "Kandy features a tropical rainforest climate with warm temperatures year-round and cooler evenings. Rain showers can occur at any time, though the heaviest rainfall typically happens during the monsoon seasons.",
    "tips": "Take a leisurely stroll along the perimeter walkway in the early morning or late afternoon to avoid the midday heat. Be mindful of the local wildlife, including monkeys and various bird species, and dress modestly when visiting the nearby temple."
  }
}
```

---

## Troubleshooting

| Problem | Cause / Fix |
|---|---|
| Browser shows certificate warning | Expected — mkcert self-signed cert. Click "Advanced → Proceed". |
| VR button does nothing | WebXR requires **HTTPS** (or localhost). Use the mkcert HTTPS server or ngrok. |
| Video is distorted in the sphere | Footage must be equirectangular 2:1 (e.g. 3840×1920). Re-export from the 360 camera. |
| Video won't autoplay | Browsers block autoplay with sound. The app starts playback from a user click (overlay / Start Tour). |
| `ffmpeg` not found | Add FFmpeg to PATH, or rely on `imageio-ffmpeg` (used by `check_durations.py`). |
| `GEMINI_API_KEY is not set` | Set the env var before running `generate_content.py` (see [section 8](#generating-destination-content-gemini-ai)). |
| Port 5000 already in use | Stop the other process or change the port in `app.py`. |
| SSL file errors on start | Ensure `10.159.155.140+2.pem` and `10.159.155.140+2-key.pem` exist next to `app.py`, or regenerate with `mkcert 10.159.155.140`. |

---

## Deployment Notes

- The app binds to `0.0.0.0:5000` and serves HTTPS using the included mkcert-generated PEM files. This makes the site reachable from other devices on the LAN at `https://10.159.155.140:5000` (the cert's name).
- For public sharing, expose it with `ngrok http 5000` (see `Commands guide.txt`).
- For production, replace the dev server with a WSGI server (waitress/gunicorn) and use a real certificate; update the hard-coded `ssl_context` paths in `app.py`.
- If the user does not pick a custom order, the app falls back to the default segment order after the intro.

---

## Browser / VR Support

- A-Frame **1.5.0** (WebVR/WebXR) loaded from CDN
- VR button uses `sceneEl.enterVR()`; works on WebXR-compatible headsets (Quest browser, Chrome + Cardboard, etc.)
- On desktop without a headset, VR mode falls back to A-Frame's fullscreen stereo view
- Fullscreen API used with `webkit` fallbacks for Safari/iOS
- Recommended: Chrome or Edge; iOS Safari has limited WebXR support

---

© 2026 Virtual_Tour. Explore responsibly.
