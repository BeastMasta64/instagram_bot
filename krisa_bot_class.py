import datetime
import time
from typing import List, Union

from krisa_bot_values import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import distinct, desc, or_
from sqlalchemy.orm import Session

from config import CHROMEDRIVER_PATH
from models import *


class KrisaBot():
    def __init__(self, username: str, password: str, session: Session, mode: str = ''):

        self.username = username
        self.password = password
        self.session = session
        self.mode = mode
        # все эти опции необходимы для качественной работы браузера,
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        # опция headless включает режим без отображения окна браузера
        self.options.headless = False
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')

        self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=self.options)

    # метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com/nikonova_ira/')
        sleep(4)
        username_input = browser.find_element(by=By.NAME, value='username')
        username_input.clear()
        sleep(1)
        username_input.send_keys(self.username)
        sleep(2)
        password_input = browser.find_element(by=By.NAME, value='password')
        password_input.clear()
        sleep(1)
        password_input.send_keys(self.password)
        sleep(1)
        password_input.send_keys(Keys.ENTER)
        sleep(4)

    def click_not_now_button(self):
        try:
            not_now_button = self.browser.find_element(by=By.XPATH, value='//*[contains(text(), "Не сейчас")]')
            not_now_button.click()
            print('Нажал на кнопку не сейчас')
        except NoSuchElementException:
            print('Не смог нажать на кнопку не сейчас')
            pass

    def scroll(self):
        SCROLL_PAUSE_TIME = 1.7

        element_for_size = self.browser.find_element(by=By.XPATH, value=element_for_size_xpath[self.mode])
        # Get scroll height
        last_height = element_for_size.size['height']
        same_height = []
        print('scrolling...')
        while True:
            # print(f'last_height={last_height}')

            # Scroll down to bottom
            element_to_scroll = self.browser.find_element(by=By.XPATH, value=element_to_scroll_xpath[self.mode])
            self.browser.execute_script(f"arguments[0].scrollTo(0, 30000000);", element_to_scroll)
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height,
            # if same height appears after 4 scrolldowns, we stop,
            # we almost 100% sure that it is the end of the page
            element_for_size = self.browser.find_element(by=By.XPATH, value=element_for_size_xpath[self.mode])
            new_height = element_for_size.size['height']
            if new_height == last_height:
                if same_height:
                    if new_height > same_height[0]:
                        same_height = [new_height]
                    else:
                        same_height.append(new_height)
                else:
                    same_height.append(new_height)

            # print(f'same_height_list: {same_height}')

            if len(same_height) == 4:
                print('I guess this is the end of the mf page!')
                break

            last_height = new_height

    def get_usernames(self) -> List[str]:
        users = self.browser.find_elements(by=By.XPATH, value=users_xpath[self.mode])
        print(f'users_count: {len(users)}')
        usernames = []
        print('getting usernames....')
        for user in users:
            # try:
            #     # print(f'trying adding nickname, using element_xpath: {username_element_xpath_list[0]}')
            #     username = user.find_element(by=By.XPATH, value=username_element_xpath_list[0]).text
            #     usernames.append(username)
            #     # print(f'added username: {username}')
            # except Exception as e:
            #     print(e)
            try:
                # print(f'trying adding nickname, using element_xpath: {username_element_xpath_list[1]}')
                username = user.find_element(by=By.XPATH, value=username_element_xpath_list[1]).text
                usernames.append(username)
                # print(f'added username: {username}')
            except Exception as e:
                username = user.find_element(by=By.XPATH, value=username_element_xpath_list[0]).text
                usernames.append(username)
        print('done')
        return usernames

    def loop_to_get_all_usernames(self) -> set[str]:
        loops_quantity = 15
        real_usernames_quantity = self.browser.find_element(by=By.XPATH, value=users_quantity_xpath[self.mode]).text
        print(f'real_{self.mode}_quantity: {real_usernames_quantity}')
        usernames_unique_set = set()
        usernames_list = []
        print('looping to find em all')
        full_cycles_number = 1
        retries_number = 0
        self.browser.find_element(by=By.XPATH, value=users_button_xpath[self.mode]).click()
        for i in range(loops_quantity):
            print(f'loop number: {full_cycles_number}')
            try:
                sleep(4)
                self.scroll()
                usernames_list += self.get_usernames()
                self.browser.refresh()
                sleep(5)
                full_cycles_number += 1
            except Exception as e:
                retries_number += 1
                print(e)
                self.browser.refresh()
                sleep(3)
                pass
            usernames_unique_set = set(usernames_list)
            print(f'usernames_unqique_set: {len(usernames_unique_set)}\n')
            if len(usernames_unique_set) >= int(real_usernames_quantity):

                print(f'found all {real_usernames_quantity}')
                print(f'full_cycles: {full_cycles_number-1}, retries: {retries_number}')
                break
        if len(usernames_unique_set) < int(real_usernames_quantity):
            raise Exception("Couldn't get all the usernames")
        return usernames_unique_set

    def add_usernames_data_to_database(self, usernames: Union[set[str]]):
        usernames_data_tables = {
            'followers': FollowersDataModel,
            'followings': FollowingsDataModel,
        }
        UsernameDataModel = usernames_data_tables[self.mode]
        for username in usernames:
            self.session.add(
                UsernameDataModel(username=username, check_date=datetime.date.today()))
        self.session.commit()

    def find_new_or_left_users(self) -> dict[str: list[str]]:
        usernames_data_tables = {
            'followers': FollowersDataModel,
            'followings': FollowingsDataModel,
        }
        UsernameDataModel: Union[FollowersDataModel,
                                 FollowingsDataModel] = usernames_data_tables[self.mode]
        two_dates = self.session. \
            query(distinct(UsernameDataModel.check_date)). \
            order_by(desc(UsernameDataModel.check_date)). \
            limit(2).all()
        if len(two_dates) != 2:
            print(f'i need two chekups in database to start comparisson, how many checkups now: {len(two_dates)}')
            raise Exception
        date_after, date_before = [date[0] for date in two_dates]
        difference_in_usernames_data_tables = {
            'followers': DiffFollowersModel,
            'followings': DiffFollowingsModel,
        }
        DiffInUsernamesDataModel: Union[DiffFollowersModel,
                                        DiffFollowingsModel] = difference_in_usernames_data_tables[self.mode]
        last_checkup_date = self. \
            session.query(distinct(DiffInUsernamesDataModel.date_after)). \
            order_by(DiffInUsernamesDataModel.date_after) \
            .first()
        if last_checkup_date:
            if last_checkup_date[0] == datetime.date.today():
                print('already done checkup for today')
                raise Exception
        date_after_usernames_raw = self.session. \
            query(UsernameDataModel.username). \
            filter(UsernameDataModel.check_date == date_after). \
            all()
        date_before_usernames_raw = self.session. \
            query(UsernameDataModel.username). \
            filter(UsernameDataModel.check_date == date_before). \
            all()
        date_after_usernames = [username[0] for username in date_after_usernames_raw]
        date_before_usernames = [username[0] for username in date_before_usernames_raw]
        new_usernames_set = set(date_after_usernames).difference(set(date_before_usernames))
        left_usernames_set = set(date_before_usernames).difference(set(date_after_usernames))
        left_usernames = list(left_usernames_set)
        new_usernames = list(new_usernames_set)

        return date_after, date_before, left_usernames, new_usernames

    def add_difference_in_usernames_data_to_database(self,
                                                     date_after: datetime.date,
                                                     date_before: datetime.date,
                                                     left_usernames: List[tuple[str]],
                                                     new_usernames: List[tuple[str]]):
        if not left_usernames and not new_usernames:
            print(f'no new or left username from {date_before} to {date_after}')
            return
        difference_in_usernames_data_tables = {
            'followers': DiffFollowersModel,
            'followings': DiffFollowingsModel,
        }
        DiffInUsernamesDataModel = difference_in_usernames_data_tables[self.mode]
        for username in left_usernames:
            self.session.add(
                DiffInUsernamesDataModel(username=username, status='left',
                                         date_before=date_before, date_after=date_after))
        for username in new_usernames:
            self.session.add(
                DiffInUsernamesDataModel(username=username, status='new',
                                         date_before=date_before, date_after=date_after))
        self.session.commit()
