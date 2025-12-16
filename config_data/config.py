import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

SERVER_URL = 'https://api.poiskkino.dev'
DATE_FORMAT = "%d.%m.%Y"
DB_PATH = "database.db"

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "Поиск фильма/сериала по названию"),
    ("movies_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("movie_by_budget", "Поиск фильмов/сериалов по бюджету")
)
    # ("history", "Вывести историю запросов"),
    # ("ask_giga_chat", "Задать вопрос нейросети"),
