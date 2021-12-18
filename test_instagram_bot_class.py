from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import insert
from sqlalchemy.orm import session

from config import CHROMEDRIVER_PATH
from models import TestNicknameModel, NicknameModel


class InstagramBot():
    def __init__(self, username, password, session):

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
        browser.get('https://www.instagram.com')
        sleep(3)
        username_input = browser.find_element_by_name('username')
        username_input.clear()
        sleep(1)
        username_input.send_keys(self.username)
        sleep(2)
        password_input = browser.find_element_by_name('password')
        password_input.clear()
        sleep(1)
        password_input.send_keys(self.password)
        sleep(1)
        password_input.send_keys(Keys.ENTER)
        sleep(4)

    # функция проверки упоминания в истории
    def check_mentions(self):
        # находим все сообщения пользователя
        messages = self.browser.find_elements_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div'
        )
        # цикл по сообщениям пользователя
        for message in messages:
            try:
                # есть ли упоминание в сообщении
                message.find_element_by_xpath('.//h1[contains(text(), "Mentioned you in their story")]')
                # есть элеменент-картинка в сообщении
                message.find_element_by_xpath('.//button/div/div/div/img')
                return True
            except:
                continue
        return False

    def click_not_now_button(self):
        try:
            not_now_button = self.browser.find_element_by_xpath(
                '//*[contains(text(), "Not Now")]')
            not_now_button.click()
        except NoSuchElementException:
            pass

    # метод обработки запросов
    def check_requests(self):
        # Заходим в личные сообщения
        self.browser.get('https://www.instagram.com/direct/inbox/')
        sleep(5)

        # Нажимаем кнопку не сейчас
        self.click_not_now_button()
        sleep(4)

        mentioned = True
        while mentioned:
            mentioned = False
            # Заходим в запросы
            try:
                requests_button = '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div[2]/span/button/h5'
                self.browser.find_element_by_xpath(requests_button).click()
            except NoSuchElementException:
                print('Нет новых запросов от пользователей')
                break
            sleep(2)

            # Запускаем цикл по количеству пользователей, в поисках упоминаний
            mentioned = self.cycle_through_requests_to_look_for_mentions()
            if mentioned:
                self.accept_request()
                print('Добавил запрос в основные\n')
                sleep(2)

    def cycle_through_requests_to_look_for_mentions(self):
        # Ищем список пользователей в запросах
        request_list = self.browser.find_elements_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div'
        )

        for user_index in range(1, len(request_list) + 1):
            # Заходим в переписку к пользователю
            person = f'/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div[{user_index}]'
            self.browser.find_element_by_xpath(person).click()
            print(f'Проверяю {user_index} пользователя в запросах')
            sleep(2)

            if self.check_mentions():
                return True
        return False

    def accept_request(self):
        accept_button = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/button'
        self.browser.find_element_by_xpath(accept_button).click()
        sleep(2)
        main_button = '/html/body/div[6]/div/div/div/div[2]/button[1]'
        self.browser.find_element_by_xpath(main_button).click()

    def check_dms(self, quantity, variant):
        if variant == 'main':
            # Заходим в основные
            self.browser.get('https://www.instagram.com/direct/inbox/')
        elif variant == 'general':
            # Заходим в общие
            self.browser.get('https://www.instagram.com/direct/inbox/general/')
        sleep(4)

        # Нажимаем кнопку не сейчас
        self.click_not_now_button()
        sleep(4)

        # цикл по количеству человек
        for user_index in range(1, quantity + 1):
            print(f'\nПроверяю {user_index} клиента.')

            # if user_index == 27:
            #     self.browser.refresh()
            #     sleep(2)

            # скроллим ленту сообщений от пользователей
            self.scroll_dm_field_to_user(user_index=user_index)
            if user_index > 26:
                user_index = 26

            user = self.browser.find_element_by_xpath(
                f'/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[{user_index}]'
            )
            user.click()
            sleep(1)

            # # после 28 человека - порядковый номер диалога в хтмл коде не изменяется и равен 28
            # if user_index > 28:
            #     user_index = 28
            #
            # # переменная под всех пользователей, которых видит бот
            # users = self.browser.find_elements_by_xpath(
            #     '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[1]'
            #     '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[26]'
            #     '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[26]'
            #     '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[10]'
            #     '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div'
            # )
            # # выбираем i-того пользователя
            # users[user_index - 1].click()
            # sleep(2)

            # смотрим имя пользователя
            user_nickname = self.browser.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div'
                '/div/div[2]/div[1]/div/div/div[2]/div/div[2]/button/div/div/div'
            ).text

            self.process_user(user_nickname=user_nickname)
            sleep(2)

    def process_user(self, user_nickname):
        # Проверка на упоминание
        if self.check_mentions() and not self.check_if_user_exists_in_db(nickname=user_nickname):
            try:
                db_user_id = self.insert_nickname_in_db_return_id(nickname=user_nickname)
                self.send_customer_his_nomerok(nomerok=db_user_id)
                self.session.commit()
            except Exception as e:
                print(f'While processing user {user_nickname} caught an exception:\n'
                      f'{e}\n'
                      f'Rolling back the session')
                self.session.rollback()
                raise e
            print(f'добавил юзера {user_nickname} с номерком {db_user_id}')
        else:
            print(f'{user_nickname} - ему не надо')

    def scroll_dm_field_to_user(self, user_index: int):
        # поле сообщений
        dm_field = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div'
        )

        # первый пользователь прогружается через 7 пикселя, остальные - каждые последующие 72 пикселя
        # начальное количество пользователей в поле основные = 18
        # максимальное количество пользователей в поле основные = 28
        # на 11 пользователя бот почему-то нажать не может,
        # прокрутим страницу вниз хотя бы на 1 пиксель - это помогает
        if user_index == 11:
            self.browser.execute_script(f"arguments[0].scrollTo(0, {1});", dm_field)
            print(f'Листаю на {1} пикселей')
            sleep(2)
        # после 18 человека необходимо листать вниз, чтобы искомый диалог прогрузился
        elif user_index > 18:
            self.browser.execute_script(f"arguments[0].scrollTo(0, {7 + 72 * (user_index - 19)});", dm_field)
            print(f'Листаю на {7 + 72 * (user_index - 19)} пикселей')
            sleep(2)

    def check_if_user_exists_in_db(self, nickname):
        nickname_model_id_q = self.session.query(NicknameModel.id).filter(NicknameModel.nickname == nickname)
        check = self.session.query(nickname_model_id_q.exists()).scalar()
        return check

    def insert_nickname_in_db_return_id(self, nickname):
        insert_stmt = (
            insert(NicknameModel).
                values(nickname=nickname).
                returning(NicknameModel.id)
        )
        db_user_id = self.session.execute(insert_stmt).scalar()
        return db_user_id

    def send_customer_his_nomerok(self, nomerok):
        text_box = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'
        )
        text_box.clear()
        text_box.send_keys(f'Ваш номерок {nomerok}!\n'
                           f'Удачи:)')
        send_button = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'
        )
        send_button.click()
