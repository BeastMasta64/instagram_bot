from time import sleep

from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import *
from krisa_bot_class import KrisaBot


def create_session():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
    session = Session(engine)
    return session


session = create_session()

username_element = './div/div[1]/div[2]/div[1]/span/a/span'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def krisss():
    krisa = KrisaBot(username=USERNAME_KIR, password=PASSWORD_KIR, session=session)
    krisa.login()
    sleep(2)
    krisa.click_not_now_button()
    sleep(1)
    krisa.browser.find_element(by=By.XPATH,
                               value='/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div').click()

    # krisa.browser.find_element(by=By.XPATH,
    #                            value='/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div').click()
    sleep(2)
    return krisa.scroll()
