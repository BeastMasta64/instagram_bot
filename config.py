import os

from dotenv import load_dotenv

load_dotenv()
# логины и пароли аккаунтов инстаграм
USERNAME_KIR = str(os.getenv("USERNAME_KIR"))
PASSWORD_KIR = str(os.getenv("PASSWORD_KIR"))
USERNAME_MART = str(os.getenv("USERNAME_MART"))
PASSWORD_MART = str(os.getenv("PASSWORD_MART"))

DB_USER = str(os.getenv("DB_USER"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = str(os.getenv("DB_PORT"))
DB_DATABASE = str(os.getenv("DB_DATABASE"))

project_path = os.path.dirname(os.path.abspath(__file__))

CHROMEDRIVER_PATH = os.path.join(project_path, 'chromedriver/chromedriver')
OPERADRIVER_PATH = './operadriver/operadriver.exe'
