import os
from dotenv import load_dotenv

load_dotenv()

#PRIVREMENO ZAKOMENTARISANO, DOK SE NE ISTESTIRA KONEKCIJA NA BAZU
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_NAME = os.getenv("DB_NAME")
# DB_PORT = os.getenv("DB_PORT")

DB_HOST = "localhost"
DB_USER = "ocr_user"
DB_PASSWORD = "ocr_password"
DB_NAME = "ocr_app"
DB_PORT = "3306"