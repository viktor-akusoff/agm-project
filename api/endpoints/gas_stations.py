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
            result = session.query(GasStation).filter(GasStation.road_code == road_code).all()
        else:
            result = session.query(GasStation).order_by(GasStation.road_code.desc()).all()
            
    return [gas_station.__dict__ for gas_station in result]