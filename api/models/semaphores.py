from core.database import BaseModel
from sqlalchemy import Column, Integer, Numeric, Text, DateTime, String


class Semaphore(BaseModel):
    
    __tablename__ = "tbl_semaphores"
    
    id = Column(Integer, primary_key=True, index=True)
    geomtype = Column(Text, nullable=False, default='Point')
    coordinates = Column(Text, nullable=False, default='[]')
    road_code = Column(Integer, nullable=False)
    roadid = Column(String)
    vertical_order = Column(Numeric, nullable=False)
    km_beg = Column(Numeric, nullable=False)
    create_date = Column(DateTime, nullable=True)
    delete_date = Column(DateTime, nullable=True)