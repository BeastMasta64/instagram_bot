import datetime
from time import sleep
from krisa_bot_values import *
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import *
from krisa_bot_class import KrisaBot


def create_session():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}", echo=True)
    session = Session(engine)
    return session


session = create_session()


def krisss(mode: str):
    import time
    start_time = time.time()
    krisa = KrisaBot(username=USERNAME_KIR, password=PASSWORD_KIR, session=session, mode=mode)
    krisa.login()
    sleep(4)
    krisa.click_not_now_button()
    sleep(4)
    usernames = krisa.loop_to_get_all_usernames()
    krisa.add_usernames_data_to_database(usernames=usernames)
    searching_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    print(f"---Searching time for all {mode} is %s---" % (searching_time))


def left_or_new_usernames(mode: str):
    print('starting to add new or left usernames to DB')
    krisa = KrisaBot(username=USERNAME_KIR, password=PASSWORD_KIR, session=session, mode=mode)
    date_after, date_before, left_usernames, new_usernames = krisa.find_new_or_left_users()
    print(f'left_usernames: {left_usernames}')
    print(f'new_usernames: {new_usernames}')
    krisa.add_difference_in_usernames_data_to_database(date_after=date_after,
                                                       date_before=date_before,
                                                       left_usernames=left_usernames,

                                                       new_usernames=new_usernames)


mode_list = ['followers', 'followings']


def cycle_to_krisss_for_real():

    krisss(mode=mode_list[0])
    krisss(mode=mode_list[1])
    left_or_new_usernames(mode=mode_list[0])
    left_or_new_usernames(mode=mode_list[1])



def login():
    krisa = KrisaBot(username=USERNAME_KIR, password=PASSWORD_KIR, session=session, mode='followings')
    krisa.login()


dict_for_krissa_movements = {
    1: cycle_to_krisss_for_real,
    2: login,
}

dict_for_krissa_movements[1]()
