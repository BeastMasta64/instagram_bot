from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# from direct_users_list import direct_users_list
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os
import emoji
from config import CHROMEDRIVER_PATH, USERNAME_MART, PASSWORD_MART


class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
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
        sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(self.username)

        sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.send_keys(Keys.ENTER)
        sleep(5)

    # функция проверки упоминания в истории
    def check_mentions(self):
        mentioned = False
        browser = self.browser

        # находим все сообщения пользователя
        messages = browser.find_elements_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div')
        # цикл по сообщениям пользователя
        for message in messages:
            try:
                # есть ли упоминание в сообщении
                message.find_element_by_xpath('.//h1[contains(text(), "Упомянул(-а) вас в своей истории")]')
                # есть элеменент картинка в сообщении
                message.find_element_by_xpath('.//button/div/div/div/img')
                mentioned = True
            except NoSuchElementException:
                continue

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
                sleep(2)

                if self.check_mentions():
                    mentioned = True

                    accept_button = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/' \
                                    'div/div[2]/div[5]/button'
                    browser.find_element_by_xpath(accept_button).click()
                    sleep(2)
                    main_button = '/html/body/div[6]/div/div/div/div[2]/button[1]'
                    browser.find_element_by_xpath(main_button).click()
                    sleep(2)
                    break

                sleep(2)

    def check_dms(self, quantity, variant):

        browser = self.browser

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

            sleep(3)
            browser.refresh()
            sleep(5)

            # Нажимаем кнопку не сейчас
            try:
                not_now_button = browser.find_element_by_xpath(
                    '//*[contains(text(), "Не сейчас")]')
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

                dm_field = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div')

                # на 11 пользователя бот почему-то нажать не может,
                # прокрутим страницу вниз хотя бы на 1 пиксель - это помогает
                if i == 11:
                    browser.execute_script(f"arguments[0].scrollTo(0, {1});", dm_field)
                    print(f'листаю на {1} пикселей')
                    sleep(2)
                # после 18 человека необходимо листать вниз, чтобы искомый диалог прогрузился
                if i > 18:
                    browser.execute_script(f"arguments[0].scrollTo(0, {7 + 72 * (i - 19)});", dm_field)
                    print(f'листаю на {7 + 72 * (i - 19)} пикселей')
                    sleep(2)
                # после 28 человека - порядковый номер диалога в хтмл коде не изменяется и равен 28
                if i > 28:
                    i = 28

                # переменная под всех пользователей, которых видит бот
                users = browser.find_elements_by_xpath(
                    '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div')

                # выбираем i-того пользователя
                users[i - 1].click()
                sleep(2)

                # смотрим имя пользователя
                nickname_window = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[1]/div/div' \
                                  '/div[2]/div/div[2]/button/div/div[1]/div'
                user_nickname = browser.find_element_by_xpath(nickname_window).text

                # Проверка на упоминание
                if self.check_mentions() and user_nickname not in nicknames_list:
                    text_box = browser.find_element_by_xpath(
                        '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
                    text_box.clear()
                    text_box.send_keys(f'Ваш номерок {len(nicknames_list) + 1}!\n'
                                       f'Удачи:)')
                    send_button = browser.find_element_by_xpath(
                        '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')
                    send_button.click()
                    nicknames_list.append(user_nickname)
                    print(f'добавил юзера {user_nickname}')
                else:
                    print(f'{user_nickname} - ему не надо')
                sleep(2)
        except:
            print('Что-то не так...')
        f = open('nicknames.txt', 'w')
        for nickname in nicknames_list:
            f.write(nickname + '\n')
        f.close()
        print('Проверка завершена')


my_bot = InstagramBot(USERNAME_MART, PASSWORD_MART)
my_bot.login()
my_bot.check_requests()
my_bot.check_dms(30, 1)
# my_bot.close_browser()


# my_bot.check_dms(5, 2)

# my_bot.check_dms(10, 1)
# my_bot.gavno()

# my_bot.send_direct_message('kryakrya64', 'working!')
