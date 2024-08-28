from fastapi import APIRouter, Query
from core.database import session
from api.models.gas_stations import GasStation

router = APIRouter(prefix='/gas-stations')

@router.get('/')
def get_gas_stations(road_code: int | None = None):
    if road_code:
        result = session.query(GasStation).filter(GasStation.road_code == road_code).all()
    else:
        result = session.query(GasStation).order_by(GasStation.road_code.desc()).all()
    
    cleaned_result = []
    
    for element in result:
        cleaned_element = element
        cleaned_element.coordinates = eval(element.coordinates) # type: ignore
        cleaned_result.append(cleaned_element)
        
    return cleaned_result