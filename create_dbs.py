from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
from models import Base

if __name__ == '__main__':
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
    session = Session(engine)
    Base.metadata.create_all(engine)