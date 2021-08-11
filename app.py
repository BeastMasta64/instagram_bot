from instagram_bot_class import InstagramBot
from config import USERNAME_MART, PASSWORD_MART

# создаем экземпляр класса
bot = InstagramBot(USERNAME_MART, PASSWORD_MART)
# выполняем вход в инстаграм
bot.login()
# проверяем запросы от новых пользователей
bot.check_requests()
# проверяем папку основные
bot.check_dms(60, 1)
# проверяем папку общее
# bot.check_dms(15, 1)
# закрываем браузер
bot.close_browser()
