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