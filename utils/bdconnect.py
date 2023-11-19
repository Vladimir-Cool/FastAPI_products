from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# from models.components import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)


# Зависимость для получения сессии базы данных
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()