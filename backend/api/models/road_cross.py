from core.database import BaseModel
from sqlalchemy import Column, Integer, Numeric, Text, DateTime, String, Float


class RoadCross(BaseModel):
    
    __tablename__ = "tbl_road_cross"
    
    id = Column(Integer, primary_key=True, index=True)
    geomtype = Column(Text, nullable=False, default='Point')
    coordinates = Column(Text, nullable=False, default='[]')
    road_code = Column(Integer, nullable=False)
    roadid = Column(String)
    km_beg = Column(Numeric, nullable=False)
    k_s025_1 = Column(String)
    angle = Column(Float)
    name = Column(String)
    width = Column(Float)
    create_date = Column(DateTime, nullable=True)
    delete_date = Column(DateTime, nullable=True)