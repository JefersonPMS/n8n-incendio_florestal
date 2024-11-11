from fastapi import FastAPI, Query
from typing import Dict
import requests
import rasterio
from rasterio.io import MemoryFile
from shapely.geometry import Point
from pyproj import Transformer
import numpy as np

app = FastAPI()

@app.get("/avaliar_risco_incendio/")
def avaliar_risco_incendio(lat: float = Query(..., description="Latitude"), lon: float = Query(..., description="Longitude")) -> Dict:
    # URL do arquivo raster
    raster_url = "https://dataserver-coids.inpe.br/queimadas/queimadas/riscofogo_meteorologia/previsto/risco_fogo/RF.PREV.T0.tif"

    # Fazer download do arquivo raster
    response = requests.get(raster_url)
    if response.status_code != 200:
        return {"error": "Não foi possível acessar o arquivo de risco de fogo"}

    # Abrir o raster diretamente da memória usando rasterio
    with MemoryFile(response.content) as memfile:
        with memfile.open() as src:
            # Criar um ponto de geometria com shapely
            point = Point(lon, lat)
            transformer = Transformer.from_crs("epsg:4326", src.crs.to_string(), always_xy=True)
            lon_proj, lat_proj = transformer.transform(lon, lat)
            buffer = Point(lon_proj, lat_proj).buffer(500)
            shapes = [buffer.__geo_interface__]

            # Criar uma máscara para o buffer
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_image = out_image[0]

            # Substituir valores NaN ou negativos, se necessário
            out_image = np.where((out_image < 0) | np.isnan(out_image), np.nan, out_image)

            # Calcular o valor médio de risco ignorando NaN
            risco_medio = np.nanmean(out_image)

            if np.isnan(risco_medio):
                return {"latitude": lat, "longitude": lon, "risco_medio": "Valor inválido", "mensagem": "Não foi possível determinar o valor de risco de incêndio na área do buffer"}

    return {"latitude": lat, "longitude": lon, "risco_medio": risco_medio, "mensagem": f"O valor médio de risco de incêndio na área do buffer é {risco_medio:.2f}"}
