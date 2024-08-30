import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker
from core.settings import settings

conn_string = settings.SQLITE_CONN
engine = create_engine(conn_string, echo=True)    

Session = sessionmaker(bind=engine, autoflush=True)

class BaseModel(DeclarativeBase): pass

r = redis.Redis(host='redis', port=6379, db=0)
