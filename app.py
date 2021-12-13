from instagram_bot_class import InstagramBot
from config import USERNAME_MART, PASSWORD_MART

# создаем экземпляр класса
bot = InstagramBot(USERNAME_MART, PASSWORD_MART)
# выполняем вход в инстаграм
bot.login()
# проверяем запросы от новых пользователей
# bot.check_requests()
# проверяем папку основные
bot.check_dms(20, 1)
# проверяем папку общее
# bot.check_dms(5, 2)
# закрываем браузер
# bot.close_browser()
