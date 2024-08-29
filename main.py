from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import (
    gas_stations,
    roads,
)

app = FastAPI(
    title="AGM Systems API",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(gas_stations.router)
app.include_router(roads.router)