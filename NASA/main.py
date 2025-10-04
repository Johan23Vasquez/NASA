from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(
    title="Weather API",
    description="API que recibe lat/lon y devuelve variables meteorológicas",
    version="1.0"
)

# 🔓 Habilitar CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather(lat: float = Query(...), lon: float = Query(...)):
    """
    Devuelve variables climáticas para una latitud y longitud.
    Aquí usamos un dataset de prueba de NASA (Hydrology Data Rods).
    """
    nasa_url = f"https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/access/timeseries.cgi"
    params = {
        "variable": "Precipitation",
        "lat": lat,
        "lon": lon,
        "startDate": "2020-01-01",
        "endDate": "2020-01-10",
        "type": "asc2"
    }

    try:
        r = requests.get(nasa_url, params=params, timeout=30)
        data = r.text.splitlines()

        # 🧹 Limpiamos y convertimos en JSON
        series = []
        for line in data:
            if line.strip() and line[0].isdigit():
                parts = line.split()
                if len(parts) == 2:
                    series.append({"date": parts[0], "value": float(parts[1])})

        return {
            "location": {"lat": lat, "lon": lon},
            "variable": "precipitation",
            "unit": "mm/day",
            "count": len(series),
            "series": series
        }
    except Exception as e:
        return {"error": str(e)}
