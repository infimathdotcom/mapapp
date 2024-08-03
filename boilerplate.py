import os

def create_file(path, content=""):
    with open(path, 'w') as file:
        file.write(content)

# Define the folder structure
folders = [
    'map_app',
    'map_app/static',
    'map_app/static/css',
    'map_app/static/js',
    'map_app/templates'
]

# Define the files and their content
files = {
    'map_app/main.py': """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class RouteRequest(BaseModel):
    start: str  # e.g., "13.388860,52.517037"
    end: str    # e.g., "13.397634,52.529407"

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"

@app.post("/route")
async def get_route(route_request: RouteRequest):
    start = route_request.start
    end = route_request.end
    url = f"{OSRM_BASE_URL}/{start};{end}?overview=full"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching route")
    return response.json()

# Serve static files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="map_app/static"), name="static")

@app.get("/")
async def root():
    with open('map_app/templates/index.html') as f:
        return f.read()
""",
    'map_app/templates/index.html': """
<!DOCTYPE html>
<html>
<head>
    <title>Map App</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        #map { width: 100%; height: 600px; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([52.5200, 13.4050], 13);  // Centered on Berlin

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        async function getRoute(start, end) {
            const response = await fetch('/route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ start: start, end: end })
            });
            const data = await response.json();
            const coords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
            L.polyline(coords, { color: 'blue' }).addTo(map);
        }

        // Example usage: getting route between two points
        getRoute("13.388860,52.517037", "13.397634,52.529407");
    </script>
</body>
</html>
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with content
for path, content in files.items():
    create_file(path, content)

print("Project structure created successfully.")
