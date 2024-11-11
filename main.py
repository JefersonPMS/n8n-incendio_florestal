from fastapi import FastAPI, Query
from typing import Dict
import random  # Import para gerar valores aleatórios

app = FastAPI()

@app.get("/avaliar_risco_incendio/")
def avaliar_risco_incendio(lat: float = Query(..., description="Latitude"), lon: float = Query(..., description="Longitude")) -> Dict:
    # Gerar um valor de risco aleatório entre 0 e 1
    risco_medio = random.uniform(0, 1)

    return {
        "latitude": lat,
        "longitude": lon,
        "risco_medio": risco_medio,
        "mensagem": f"O valor médio de risco de incêndio na área do buffer é {risco_medio:.2f}"
    }
