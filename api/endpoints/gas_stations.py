from fastapi import APIRouter
from core.database import Session
from typing import Optional
from core.utils import process_result, EPSGEnum, ModeType
from api.models.gas_stations import GasStation

router = APIRouter(
    prefix='/gas-stations',
    tags=["Gas stations management"]
)

@router.get('')
@process_result
def get_gas_stations(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(GasStation).filter(GasStation.road_code == road_code).all()
        return session.query(GasStation).order_by(GasStation.road_code.desc()).all()