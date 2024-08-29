from fastapi import APIRouter
from core.database import Session
from typing import Optional
from core.utils import process_result, EPSGEnum, ModeType
from api.models.semaphores import Semaphore

router = APIRouter(
    prefix='/semaphores',
    tags=["Semaphores management"]
)

@router.get('')
@process_result
def get_semaphores(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            result = session.query(Semaphore).filter(Semaphore.road_code == road_code).all()
        else:
            result = session.query(Semaphore).order_by(Semaphore.road_code.desc()).all()
            
    return [semaphore.__dict__ for semaphore in result]