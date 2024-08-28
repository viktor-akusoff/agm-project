from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from core.settings import AGMSettings

conn_string = AGMSettings.SQLITE_CONN
engine = create_engine(conn_string)

class BaseModel(DeclarativeBase): pass
