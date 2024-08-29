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
def get_roads(
    road_code: int | None = None,
    epsg: str | None = None,
    attr: bool = True,
    geo: bool = True
):
    with Session() as session:
        keys = ['id', 'road_code']
        if attr:
            keys += ['name', 'length_km']
        if geo:
            keys += ['geomtype', 'coordinates']
        if road_code is not None:
            result = session.query(Road).filter(Road.road_code == road_code).all()
        else:
            result = session.query(Road).all()
        filtered_result = [
            {
                key: road.__dict__[key] for key in keys
            } for road in result
        ]
        return filtered_result