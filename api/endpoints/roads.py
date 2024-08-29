from fastapi import APIRouter
from core.database import Session
from core.utils import coordinates_eval
from api.models.roads import Road

router = APIRouter(
    prefix='/roads',
    tags=["Roads management"]
)

@router.get('')
@coordinates_eval
def get_roads(road_code: int | None = None, epsg: str | None = None):
    with Session() as session:
        if road_code is not None:
            return session.query(Road).filter(Road.road_code == road_code).all()
        return session.query(Road).all()