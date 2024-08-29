from functools import wraps
from pyproj import Proj, transform
import json

SUPPORTED = ['32637', '32638']

def coordinates_eval(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_epsg = False
        epsg = kwargs.get('epsg')
        result = func(*args, **kwargs)
        cleaned_result = []
        if epsg is not None and epsg in SUPPORTED:
            in_proj = Proj('epsg:4326')
            out_proj = Proj(f'epsg:{epsg}')
            is_epsg = True
        for element in result:
            cleaned_element = element
            cleaned_element.coordinates = json.loads(element.coordinates)
            if not is_epsg:
                cleaned_result.append(cleaned_element)
                continue
            if cleaned_element.geomtype == "Point":
                coord = cleaned_element.coordinates
                cleaned_element.coordinates = transform(in_proj, out_proj, coord[1], coord[0])
            elif cleaned_element.geomtype == "LineString":
                cleaned_element.coordinates = [
                    transform(in_proj, out_proj, coord[1], coord[0]) for coord in cleaned_element.coordinates
                ]                
            cleaned_result.append(cleaned_element)
        return cleaned_result
    return wrapper