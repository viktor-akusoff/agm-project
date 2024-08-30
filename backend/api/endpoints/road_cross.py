import io
import json
from fastapi import APIRouter, UploadFile
from core.database import Session
from typing import Optional
from core.utils import process_result, upload_data, EPSGEnum, ModeType
from api.models.road_cross import RoadCross

router = APIRouter(
    prefix='/road-cross',
    tags=["Road cross management"]
)

@router.get('')
@process_result('road_cross')
def get_road_cross(
    road_code: Optional[int] = None,
    epsg: Optional[EPSGEnum] = None,
    mode: Optional[ModeType] = None,
):
    with Session() as session:
        if road_code is not None:
            return session.query(RoadCross).filter(RoadCross.road_code == road_code).all()
        return session.query(RoadCross).order_by(RoadCross.road_code.desc()).all()


@router.post('')
def upload_road_cross(data: UploadFile):
    return upload_data(data, RoadCross)