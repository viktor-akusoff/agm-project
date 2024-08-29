from fastapi import APIRouter
from core.database import Session
from core.utils import coordinates_eval
from api.models.roads import Road

router = APIRouter(
    prefix='/roads',
    tags=["Roads management"]
)

@router.get('/')
@coordinates_eval
def get_roads():
    with Session() as session:
        return session.query(Road).all()

@router.get('/{road_code}')
@coordinates_eval
def get_road(road_code: int):
    with Session() as session:
        return session.query(Road).filter(Road.road_code == road_code).all()