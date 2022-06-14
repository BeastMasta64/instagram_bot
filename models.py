from sqlalchemy import Column, Integer, String, DateTime, func, create_engine, Date
from sqlalchemy.orm import declarative_base
from config import *


Base = declarative_base()


# class TestNicknameModel(Base):
#     __tablename__ = 'test_nickname'
#
#     id = Column(Integer, primary_key=True)
#     nickname = Column(String)
#
# class NicknameModel(Base):
#     __tablename__ = 'nicknames_table'
#
#     id = Column(Integer, primary_key=True)
#     nickname = Column(String)

class FollowersDataModel(Base):
    __tablename__ = 'followers_data_table'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    check_date = Column(Date, server_default=func.now())


class FollowingsDataModel(Base):
    __tablename__ = 'followings_data_table'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    check_date = Column(Date, server_default=func.now())


class DiffFollowersModel(Base):
    __tablename__ = 'dif_followers_table'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    status = Column(String)
    date_before = Column(Date)
    date_after = Column(Date)



class DiffFollowingsModel(Base):
    __tablename__ = 'dif_followings_table'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    status = Column(String)
    date_before = Column(Date)
    date_after = Column(Date)

# engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}", echo=True)
#
# Base.metadata.create_all(engine)
