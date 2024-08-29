import io
import json
from fastapi import APIRouter, UploadFile, HTTPException
from core.database import Session
from typing import Optional
from core.utils import process_result, upload_data, EPSGEnum, ModeType
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
            return session.query(Semaphore).filter(Semaphore.road_code == road_code).all()
        return session.query(Semaphore).order_by(Semaphore.road_code.desc()).all()


@router.post('')
def upload_semaphore(data: UploadFile):
    return upload_data(data, Semaphore)