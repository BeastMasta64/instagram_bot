from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import insert
from sqlalchemy.orm import session

from config import CHROMEDRIVER_PATH
from just_py import TestNicknameModel


class InstagramBot():

    def __init__(self, username, password, session):

        self.username = username
        self.password = password
        self.session = session
        # все эти опции необходимы для качественной работы браузера,
        # опция headless включает режим без отображения окна браузера
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        # self.options.headless = True
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
        # mentioned = False
        # browser = self.browser
        #
        # # находим все сообщения пользователя
        #
        # messages = browser.find_elements_by_xpath(
        #     '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div')
        # # цикл по сообщениям пользователя
        # for message in messages:
        #     try:
        #         # есть ли упоминание в сообщении
        #         message.find_element_by_xpath('.//h1[contains(text(), "Упомянул(-а) вас в своей истории")]')
        #         # есть элеменент-картинка в сообщении
        #         message.find_element_by_xpath('.//button/div/div/div/img')
        #         mentioned = True
        #     except NoSuchElementException:
        #         continue
        mentioned = True
        return mentioned

    def refreshik(self):
        browser = self.browser
        browser.get('https://www.instagram.com/direct/inbox/')
        sleep(3)

        # Нажимаем кнопку не сейчас
        try:
            not_now_button = browser.find_element_by_xpath(
                '//*[contains(text(), "Не сейчас")]')
            not_now_button.click()
        except NoSuchElementException:
            pass
        sleep(2)
        browser.refresh()

    # метод обработки запросов
    def check_requests(self):
        browser = self.browser

        mentioned = True

        # Заходим в личные сообщения
        browser.get('https://www.instagram.com/direct/inbox/')
        sleep(5)

        # Нажимаем кнопку не сейчас
        try:
            not_now_button = browser.find_element_by_xpath(
                '//*[contains(text(), "Не сейчас")]')
            not_now_button.click()
        except NoSuchElementException:
            pass
        sleep(4)

        while mentioned:
            mentioned = False

            # Заходим в запросы
            try:
                requests_button = '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div[2]/span/button/h5'
                browser.find_element_by_xpath(requests_button).click()
            except NoSuchElementException:
                print('Нет новых запросов от пользователей')
                break
            sleep(2)

            # Ищем список пользователей в запросах
            request_list_path = '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div'
            request_list = browser.find_elements_by_xpath(request_list_path)

            # Запускаем цикл по количеству пользователей
            for i in range(1, len(request_list) + 1):

                # Заходим в переписку к пользователю
                person = f'/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div[{i}]'
                browser.find_element_by_xpath(person).click()
                print(f'Проверяю {i} пользователя в запросах')
                sleep(2)

                if self.check_mentions():
                    mentioned = True

                    accept_button = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/' \
                                    'div/div[2]/div[5]/button'
                    browser.find_element_by_xpath(accept_button).click()
                    sleep(2)
                    main_button = '/html/body/div[6]/div/div/div/div[2]/button[1]'
                    browser.find_element_by_xpath(main_button).click()
                    print('Добавил запрос в основные\n')
                    sleep(2)
                    break

                sleep(2)

    def check_dms(self, quantity, variant):

        browser = self.browser

        result = True
        nicknames_list = []
        f = open('nicknames.txt', 'r')
        for nickname in f:
            nicknames_list.append(nickname.replace('\n', ''))
        f.close()

        try:
            if variant == 1:
                # Заходим в основные
                browser.get('https://www.instagram.com/direct/inbox/')

            elif variant == 2:
                # Заходим в общие
                browser.get('https://www.instagram.com/direct/inbox/general/')

            sleep(4)

            # Нажимаем кнопку не сейчас
            try:
                not_now_button = browser.find_element_by_xpath(
                    '//*[contains(text(), "Not Now")]')
                not_now_button.click()
            except NoSuchElementException:
                pass
            sleep(4)

            # первый пользователь прогружается через 7 пикселя, остальные - каждые последующие 72 пикселя
            # начальное количество пользователей в поле основные = 18
            # максимальное количество пользователей в поле основные = 28

            # цикл по количеству человек
            for i in range(1, quantity + 1):
                print(f'\nПроверяю {i} клиента.')

                # скроллим ленту сообщений от пользователей
                self.scroll_dm_field(user_index=i)

                # после 28 человека - порядковый номер диалога в хтмл коде не изменяется и равен 28
                if i > 28:
                    i = 28

                # переменная под всех пользователей, которых видит бот
                users = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div')

                # выбираем i-того пользователя
                users[i - 1].click()
                sleep(2)

                # смотрим имя пользователя
                nickname_window = '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[2]' \
                                  '/div[1]/div/div/div[2]/div/div[2]/button/div/div/div'
                user_nickname = browser.find_element_by_xpath(nickname_window).text

                # Проверка на упоминание
                if self.check_mentions() and not self.check_if_user_exists(nickname=user_nickname):
                    id = self.insert_nickname_in_db_return_id(nickname=user_nickname)
                    self.send_customer_his_nomerok(nomerok=id)
                    print(f'добавил юзера {user_nickname} с номерком {id}')
                else:
                    print(f'{user_nickname} - ему не надо')
                sleep(2)

        except Exception as exception:
            print('Поймал Exception\n'
                  f'Ошибка: {exception}')
            result = False
        except:
            print('Что-то не так...')
            result = False

        f = open('nicknames.txt', 'w')
        for nickname in nicknames_list:
            f.write(nickname + '\n')
        f.close()
        print('\nПроверка завершена')
        return result

    def scroll_dm_field(self, user_index: int):
        # поле сообщений
        dm_field = self.browser.find_element_by_xpath(

            '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[1]/div[3]/div/div/div')

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

    def check_if_user_exists(self, nickname):
        nickname_model_id_q = self.session.query(TestNicknameModel.id).filter(TestNicknameModel.nickname == nickname)
        check = self.session.query(nickname_model_id_q.exists()).scalar()
        return check

    def insert_nickname_in_db_return_id(self, nickname):
        insert_stmt = (
            insert(TestNicknameModel).
                values(nickname=nickname).
                returning(TestNicknameModel.id)
        )
        id = self.session.execute(insert_stmt).scalar()
        return id

    def send_customer_his_nomerok(self, nomerok):
        # next_nomerok = self.count_nicknames() + 1
        text_box = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        text_box.clear()
        text_box.send_keys(f'Ваш номерок {nomerok}!\n'
                           f'Удачи:)')
        send_button = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')
        send_button.click()