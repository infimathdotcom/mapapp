from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"

@app.post("/route")
async def get_route():
    start = "86.9842,25.2437"  # Bhagalpur University
    end = "86.9806,25.2537"    # SM College
    
    url = f"{OSRM_BASE_URL}/{start};{end}?overview=full&geometries=geojson&steps=true"
    print(f"Requesting URL: {url}")  # Debugging: print the URL
    
    response = requests.get(url)
    print(f"Response Status Code: {response.status_code}")  # Debugging: print the response status code
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching route")
    
    data = response.json()
    print(f"Response JSON: {data}")  # Debugging: print the response JSON
    
    coordinates = data['routes'][0]['geometry']['coordinates']
    intersections = [
        {
            'location': step['maneuver']['location'],
            'maneuver': step['maneuver']['modifier'] if 'modifier' in step['maneuver'] else step['maneuver']['type']
        }
        for leg in data['routes'][0]['legs'] for step in leg['steps']
    ]
    
    print(f"Coordinates: {coordinates}")  # Debugging: print the route coordinates
    print(f"Intersections: {intersections}")  # Debugging: print the intersections list
    
    return {
        "route": coordinates,
        "intersections": intersections
    }

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open('app/templates/index.html') as f:
        html_content = f.read()
    print("Serving index.html")  # Debugging: print when serving the HTML file
    return HTMLResponse(content=html_content)
