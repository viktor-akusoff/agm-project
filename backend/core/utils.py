from functools import wraps
from pyproj import Proj, transform
from fastapi import HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from enum import Enum
from typing import Dict, List, Any
from core.database import Session, r
import json

class EPSGEnum(str, Enum):
    EPSG4326 = '4326'
    EPSG3857 = '3857'
    EPSG326327 = '32637'
    EPSG32638 = '32638'
    
    
class ObjectType(str, Enum):
    POINT = 'Point',
    MULTIPOINT = 'MultiPoint'
    LINESTRING = 'LineString'
    MULTILINESTRING = 'MultiLineString'
    POLYGON = 'Polygon'
    MULTIPOLYGON = 'MultiPolygon'
    GEOMETRY_COLLECTION = 'GeometryCollection'
    FEATURE = 'Feature'
    FEATURE_COLLECTION = 'FeatureCollection'
    
    
class ModeType(Enum):
    GEOM_ONLY = 'geom'
    PROP_ONLY = 'prop'
    BOTH = 'both'


def process_point(point, in_proj: Proj, out_proj: Proj):
    coord_num = len(point)
    new_point = list(transform(in_proj, out_proj, point[1], point[0]))
    if coord_num > 2:
        new_point = [*new_point, point[2]]
    return new_point


def process_line(line, in_proj: Proj, out_proj: Proj):
    new_line = []
    for point in line:
        new_line.append(process_point(point, in_proj, out_proj))
    return new_line
        
        
def process_polygon(polygon, in_proj: Proj, out_proj: Proj):
    new_polygon = []
    for line in polygon:
        new_polygon.append(process_line(line, in_proj, out_proj))
    return new_polygon


def process_geometry(obj: Dict, epsg: EPSGEnum):

    geomtype: ObjectType = ObjectType(obj['geomtype'])
    coordinates: List = json.loads(obj['coordinates'])
    
    if epsg == EPSGEnum.EPSG4326:
        return {
            "type": geomtype,
            "coordinates": coordinates
        }
    

    in_proj = Proj('epsg:4326')
    out_proj = Proj(f'epsg:{epsg.value}')
    
    if geomtype == ObjectType.POINT:
        coordinates = process_point(coordinates, in_proj, out_proj)

    elif geomtype in ObjectType.LINESTRING:
        coordinates = process_line(coordinates, in_proj, out_proj)
        
    elif geomtype in ObjectType.POLYGON:
        coordinates = process_polygon(coordinates, in_proj, out_proj)

    return {
        "type": geomtype,
        "coordinates": coordinates
    }
    
    
def process_properties(obj: Dict):
    
    cleaned_obj = obj

    cleaned_obj.pop('geomtype')
    cleaned_obj.pop('coordinates')
    
    return cleaned_obj

def process_result(redis_prefix: str):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            
            road_code = kwargs.get('road_code')
            
            epsg = kwargs.get('epsg')
            epsg = EPSGEnum(epsg) if epsg is not None else EPSGEnum.EPSG4326
            
            mode = kwargs.get('mode')
            mode = ModeType(mode) if mode is not None else ModeType.BOTH
            
            redis_key = f'{redis_prefix}_{epsg}_{mode}'
            
            if road_code:
                redis_key += f'_{road_code}'
                
            cache = r.get(redis_key)

            if cache is not None:
                return json.loads(cache)
                
            result = func(*args, **kwargs)
            
            processed_result = []
            
            for element in result:
                
                processed_element: Dict[str, Any] = {'type': ObjectType.FEATURE}
                
                if mode in [ModeType.GEOM_ONLY, ModeType.BOTH]:
                    processed_element['geometry'] = process_geometry(element.__dict__, epsg)
                    
                if mode in [ModeType.PROP_ONLY, ModeType.BOTH]:
                    processed_element['properties'] = process_properties(element.__dict__)
                
                processed_result.append(processed_element)

            feature_collection = {
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": f'EPSG:{epsg.value}'
                    }
                },
                "type": ObjectType.FEATURE_COLLECTION,
                "features": processed_result
            }
            
            r.set(redis_key, json.dumps(jsonable_encoder(feature_collection)))
            
            return feature_collection

        return wrapper
    
    return decorator


def upload_data(data: UploadFile, Class):
    try:
        features = json.loads(data.file.read().decode('utf-8'))['features']
        
        semaphores = []
        
        for feature in features:
            geomtype = feature['geometry']['type']
            coordinates = str(feature['geometry']['coordinates'])
            new_semaphore = {
                "geomtype": geomtype,
                "coordinates": coordinates,
                **feature["properties"]
            }
            semaphores.append(Class(**new_semaphore))
            
        with Session() as session:
            session.bulk_save_objects(semaphores)
            session.commit()

    except Exception:
        raise HTTPException(status_code=400, detail='Incorrect JSON file!')
    
    return {'detail': 'success'}
