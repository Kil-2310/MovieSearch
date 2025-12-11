import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATE_FORMAT = "%d.%m.%Y"
DB_PATH = "database.db"

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("history", "Вывести историю запросов"),
    ("ask_giga_chat", "Задать вопрос нейросети"),
    ("movie_search", "Поиск фильма/сериала по названию"),
    ("movie_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "Поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "Поиск фильмов/сериалов с высоким бюджетом"),
    ("get_my_top_10", "Получить мой топ 10")
)
