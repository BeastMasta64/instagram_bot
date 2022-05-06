import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import insert
from sqlalchemy.orm import session

from config import CHROMEDRIVER_PATH
from models import TestNicknameModel, NicknameModel


class KrisaBot():
    def __init__(self, username: str, password: str, session: session):

        self.username = username
        self.password = password
        self.session = session
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
        sleep(3)
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
        not_now_button = self.browser.find_element(by=By.XPATH, value='//*[contains(text(), "Не сейчас")]')
        not_now_button.click()
        try:
            print('Нажал на кнопку не сейчас')
        except NoSuchElementException:
            print('Не смог нажать на кнопку не сейчас')
            pass


    def scroll(self):
        SCROLL_PAUSE_TIME = 1.2
        # element_for_size = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]/ul')

        element_for_size = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[3]/ul')
        last_height = element_for_size.size['height']
        # Get scroll height
        flags_for_break = 0
        a = 0
        same_height = []
        while True:
            element_to_scroll = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[3]')
            # element_to_scroll = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]')

            a += 1
            print(f'last_height={last_height}')
            # Scroll down to bottom
            self.browser.execute_script(f"arguments[0].scrollTo(0, 30000000);", element_to_scroll)

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            # element_for_size = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]/ul')

            element_for_size = self.browser.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[3]/ul')

            new_height = element_for_size.size['height']
            if new_height == last_height:
                if same_height:
                    if new_height > same_height[0]:
                        same_height = [new_height]
                    else:
                        same_height.append(new_height)
                else:
                    same_height.append(new_height)

            print(same_height)

            if len(same_height) == 4:
                print(same_height)
                # users = self.browser.find_elements(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[2]/ul/div/li')
                users = self.browser.find_elements(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[3]/ul/div/li')
                print(f'users_count:{len(users)}')
                return users

            last_height = new_height

