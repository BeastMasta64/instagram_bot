from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
from models import NicknameModel


def create_session():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
    session = Session(engine)
    return session


def insert_nickname_in_db_return_id(session: Session, nickname: str):
    insert_stmt = (
        insert(NicknameModel).
            values(nickname=nickname).
            returning(NicknameModel.id)
    )
    db_user_id = session.execute(insert_stmt).scalar()
    session.commit()
    return db_user_id


if __name__ == '__main__':
    nickname = input('Введи никнейм, чтобы я добавил его в базу:\n')
    nomerok = insert_nickname_in_db_return_id(session=create_session(), nickname=nickname)
    print(f'Добавил юзера "{nickname}" с номерком {nomerok}')
    print(f'Ваш номерок {nomerok}!\n'
          f'Удачи:)')

