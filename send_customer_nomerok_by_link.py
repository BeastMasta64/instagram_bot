from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import USERNAME_DIAMETRO, PASSWORD_DIAMETRO, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
from instagram_bot_class import InstagramBot


link = input('Отправь мне ссылку на типа и я отправлю ему номерок:\n')

def create_session():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
    session = Session(engine)
    return session

session = create_session()
# создаем экземпляр класса
bot = InstagramBot(USERNAME_DIAMETRO, PASSWORD_DIAMETRO, session)
# выполняем вход в инстаграм
bot.login()

bot.send_customer_his_nomerok_by_link(link=link)
bot.close_browser()
