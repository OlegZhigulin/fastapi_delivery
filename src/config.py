import os
from dotenv import load_dotenv

load_dotenv()
# Переменные приложения
FLAG_CREATE_CAR = os.getenv('LOGIN', default='None')  # Логин суперюзера
FLAG_CREATE_CAR = os.getenv('PASSWORD', default='None') # Пароль суперюзера

# Переменные базы данных
POSTGRES_DB = os.getenv('DB_NAME', default='None')  # Название базы данных
POSTGRES_USER = os.getenv('POSTGRES_USER', default='None')  # Логин для подключения к базе данных
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', default='None')  # Пароль для подключения к базе данных
DB_HOST = os.getenv('DB_HOST', default='db')  # Название сервиса (контейнера)
DB_PORT = os.getenv('DB_PORT', default=5432), # Порт для подключения к базе данных

