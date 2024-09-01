from fastapi import APIRouter, UploadFile
from core.database import Session, r
from typing import Optional
from core.utils import process_result, upload_data, EPSGEnum, ModeType
from api.models.gas_stations import GasStation

router = APIRouter(
    prefix='/gas-stations',
    tags=["Gas stations management"]
)

@router.get('')
@process_result('gas_stations')
def get_gas_stations(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(GasStation).filter(GasStation.road_code == road_code).all()
        return session.query(GasStation).order_by(GasStation.road_code.desc()).all()
    
    
@router.post('')
def upload_semaphore(data: UploadFile):
    for key in r.scan_iter('gas_stations*'):
        r.delete(key)
    return upload_data(data, GasStation)