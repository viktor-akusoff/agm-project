from core.database import BaseModel
from sqlalchemy import Column, Integer, Numeric, Text, Float
from sqlalchemy.orm import Mapped, mapped_column


class Semaphore(BaseModel):
    
    __tablename__ = "tbl_semaphores"
    
    id = Column(Integer, primary_key=True, index=True)
    geomtype = Column(Text, nullable=False, default='Point')
    coordinates = Column(Text, nullable=False, default='[]')
    road_code = Column(Integer, unique=True, nullable=False)
    angle = Column(Float, nullable=False)
    km_beg = Column(Numeric, nullable=False)
    vertical_order = Column(Numeric, nullable=False)