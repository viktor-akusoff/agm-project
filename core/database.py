from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker
from core.settings import settings

conn_string = settings.SQLITE_CONN
engine = create_engine(conn_string)

Session = sessionmaker(bind=engine)
session = Session()

class BaseModel(DeclarativeBase): pass
