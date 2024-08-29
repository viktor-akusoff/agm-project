from fastapi import APIRouter
from core.database import Session
from api.models.semaphores import Semaphore
from core.utils import coordinates_eval

router = APIRouter(
    prefix='/semaphores',
    tags=["Semaphores management"]
)

@router.get('')
@coordinates_eval
def get_semaphores(road_code: int | None = None, epsg: str | None = None):
    with Session() as session:
        if road_code is not None:
            result = session.query(Semaphore).filter(Semaphore.road_code == road_code).all()
        else:
            result = session.query(Semaphore).order_by(Semaphore.road_code.desc()).all()
            
    return [semaphore.__dict__ for semaphore in result]