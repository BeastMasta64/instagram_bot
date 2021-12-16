from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TestNicknameModel(Base):
    __tablename__ = 'test_nickname'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)

class NicknameModel(Base):
    __tablename__ = 'nicknames_table'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)

