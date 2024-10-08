import io
import json
from fastapi import APIRouter, UploadFile, HTTPException
from core.database import Session, r
from typing import Optional
from core.utils import process_result, upload_data, EPSGEnum, ModeType
from api.models.lines import Line

router = APIRouter(
    prefix='/lines',
    tags=["Lines management"]
)

@router.get('')
@process_result('lines')
def get_lines(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(Line).filter(Line.road_code == road_code).all()
        return session.query(Line).order_by(Line.road_code.desc()).all()


@router.post('')
def upload_lines(data: UploadFile):
    for key in r.scan_iter("lines*"):
        r.delete(key)
    return upload_data(data, Line)