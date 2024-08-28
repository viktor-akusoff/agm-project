from core.database import BaseModel
from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey


class GasStation(BaseModel):
    
    __tablename__ = "tbl_azs"
    
    id = Column(Integer, primary_key=True, index=True)
    road_code = Column(Integer, ForeignKey('tbl_roads.road_code', ondelete='CASCADE'))
    geomtype = Column(Text, nullable=False, default='Point')
    coordinates = Column(Text, nullable=False, default='[0.0,0.0]')