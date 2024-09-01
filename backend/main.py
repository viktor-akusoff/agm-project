from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import engine, r, BaseModel
from api.endpoints import (
    gas_stations,
    roads,
    semaphores,
    road_cross,
    lines,
    panorama
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Creating tables')
    BaseModel.metadata.create_all(bind=engine)
    yield
    print('Closing databases')
    engine.dispose()

app = FastAPI(
    title="AGM Systems API",
    root_path="/api/v1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(gas_stations.router)
app.include_router(roads.router)
app.include_router(semaphores.router)
app.include_router(road_cross.router)
app.include_router(lines.router)
app.include_router(panorama.router)