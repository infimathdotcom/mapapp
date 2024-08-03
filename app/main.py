from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import polyline
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class RouteRequest(BaseModel):
    start: str  # e.g., "86.9550,25.2510"
    end: str    # e.g., "86.9650,25.2610"

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"

@app.post("/route")
async def get_route():
    start = "86.9842,25.2437"  # Bhagalpur University
    end = "86.9806,25.2537"    # SM College
    
    url = f"{OSRM_BASE_URL}/{start};{end}?overview=full"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching route")
    
    data = response.json()
    encoded_polyline = data['routes'][0]['geometry']
    decoded_coordinates = polyline.decode(encoded_polyline)
    
    return {
        "route": decoded_coordinates,
        "start": start,
        "end": end
    }

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open('app/templates/index.html') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
