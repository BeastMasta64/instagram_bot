from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from instagram_bot_class import InstagramBot
from config import USERNAME_MART, PASSWORD_MART, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE, PASSWORD_DIAMETRO, \
    USERNAME_DIAMETRO


def create_session():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
    session = Session(engine)
    return session

session = create_session()
# создаем экземпляр класса
bot = InstagramBot(USERNAME_DIAMETRO, PASSWORD_DIAMETRO, session)
# выполняем вход в инстаграм
bot.login()
# проверяем запросы от новых пользователей
bot.check_requests()
# проверяем папку основные
bot.check_dms(160, 'main')
# # проверяем папку общее
# bot.check_dms(5, 'general')
# # закрываем браузер1
bot.close_browser()
