from core.database import BaseModel
from sqlalchemy import Column, Integer, Numeric, Text


class Road(BaseModel):
    
    __tablename__ = "tbl_roads"
    
    id = Column(Integer, primary_key=True, index=True)
    road_code = Column(Integer, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    length_km = Column(Numeric, nullable=False)
    geomtype = Column(Text, nullable=False, default='LineString')
    coordinates = Column(Text, nullable=False, default='[]')