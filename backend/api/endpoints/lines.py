import io
import json
from fastapi import APIRouter, UploadFile, HTTPException
from core.database import Session
from typing import Optional
from core.utils import process_result, upload_data, EPSGEnum, ModeType
from api.models.lines import Line

router = APIRouter(
    prefix='/lines',
    tags=["Lines management"]
)

@router.get('')
@process_result('lines')
def get_semaphores(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(Line).filter(Line.road_code == road_code).all()
        return session.query(Line).order_by(Line.road_code.desc()).all()


@router.post('')
def upload_semaphore(data: UploadFile):
    return upload_data(data, Line)