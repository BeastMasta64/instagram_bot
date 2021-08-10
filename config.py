import os

from dotenv import load_dotenv

load_dotenv()

USERNAME_KIR = str(os.getenv("USERNAME_KIR"))
PASSWORD_KIR = str(os.getenv("PASSWORD_KIR"))
USERNAME_MART = str(os.getenv("USERNAME_MART"))
PASSWORD_MART = str(os.getenv("PASSWORD_MART"))

CHROMEDRIVER_PATH = './drivers/chromedriver.exe'
