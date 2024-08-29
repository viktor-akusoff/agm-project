from typing import Optional
from fastapi import APIRouter
from core.database import Session
from core.utils import process_result, EPSGEnum, ModeType
from api.models.roads import Road

router = APIRouter(
    prefix='/roads',
    tags=["Roads management"]
)

@router.get('')
@process_result
def get_roads(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(Road).filter(Road.road_code == road_code).all()
        return session.query(Road).all()