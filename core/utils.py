from functools import wraps
from pyproj import Proj, transform
from enum import Enum
from typing import Dict, List, Any
import json

class EPSGEnum(str, Enum):
    EPSG4326 = '4326'
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


def process_coordinates(coordinates, in_proj: Proj, out_proj: Proj):

    coord_num = len(coordinates)
    new_coordinates = list(transform(in_proj, out_proj, coordinates[1], coordinates[0]))

    if coord_num > 2:
        new_coordinates = [*new_coordinates, coordinates[2]]

    return new_coordinates


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
        
        coordinates = process_coordinates(coordinates, in_proj, out_proj)

    elif geomtype == ObjectType.LINESTRING:

        new_coordinates = []

        for c in coordinates:
            new_coordinates.append(process_coordinates(c, in_proj, out_proj))

        coordinates = new_coordinates

    return {
        "type": geomtype,
        "coordinates": coordinates
    }
    
    
def process_properties(obj: Dict):
    
    cleaned_obj = obj

    cleaned_obj.pop('geomtype')
    cleaned_obj.pop('coordinates')
    
    return cleaned_obj

    
def process_result(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)
        
        epsg = kwargs.get('epsg')
        epsg = EPSGEnum(epsg) if epsg is not None else EPSGEnum.EPSG4326
        
        mode = kwargs.get('mode')
        mode = ModeType(mode) if mode is not None else ModeType.BOTH
        
        processed_result = []
        
        for element in result:
            
            processed_element: Dict[str, Any] = {'type': ObjectType.FEATURE}
            
            if mode in [ModeType.GEOM_ONLY, ModeType.BOTH]:
                processed_element['geometry'] = process_geometry(element.__dict__, epsg)
                
            if mode in [ModeType.PROP_ONLY, ModeType.BOTH]:
                processed_element['properties'] = process_properties(element.__dict__)
            
            processed_result.append(processed_element)

        return processed_result

    return wrapper
