from fastapi import APIRouter
from core.database import Session
from api.models.gas_stations import GasStation
from core.utils import coordinates_eval

router = APIRouter(
    prefix='/gas-stations',
    tags=["Gas stations management"]
)

@router.get('')
@coordinates_eval
def get_gas_stations(road_code: int | None = None, epsg: str | None = None):
    with Session() as session:
        if road_code is not None:
            return session.query(GasStation).filter(GasStation.road_code == road_code).all()
        return session.query(GasStation).order_by(GasStation.road_code.desc()).all()