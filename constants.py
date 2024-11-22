import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
USERS_DATA_PATH = "./output/users_data.xlsx"