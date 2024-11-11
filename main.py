from fastapi import FastAPI, Query
from typing import Dict
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
from pyproj import Transformer
import numpy as np

app = FastAPI()

@app.get("/avaliar_risco_incendio/")
def avaliar_risco_incendio(lat: float = Query(..., description="Latitude"), lon: float = Query(..., description="Longitude")) -> Dict:
    # Caminho do arquivo local
    raster_path = r"C:\Users\taisr\Downloads\RF.PREV.T0.tif"

    with rasterio.open(raster_path) as src:
        point = Point(lon, lat)
        transformer = Transformer.from_crs("epsg:4326", src.crs.to_string(), always_xy=True)
        lon_proj, lat_proj = transformer.transform(lon, lat)
        buffer = Point(lon_proj, lat_proj).buffer(500)
        shapes = [buffer.__geo_interface__]
        out_image, out_transform = mask(src, shapes, crop=True)
        out_image = out_image[0]

        # Substituir valores NaN ou negativos se houver algum problema com valores
        out_image = np.where((out_image < 0) | np.isnan(out_image), np.nan, out_image)

        # Calcular a média ignorando NaN
        risco_medio = np.nanmean(out_image)

        if np.isnan(risco_medio):
            return {"latitude": lat, "longitude": lon, "risco_medio": "Valor inválido", "mensagem": "Não foi possível determinar o valor de risco de incêndio na área do buffer"}

    return {"latitude": lat, "longitude": lon, "risco_medio": risco_medio, "mensagem": f"O valor médio de risco de incêndio na área do buffer é {risco_medio:.2f}"}
