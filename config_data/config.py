import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

SERVER_URL = 'https://api.poiskkino.dev'

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "Поиск фильма/сериала по названию"),
    ("movie_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("movie_by_budget", "Поиск фильмов/сериалов по бюджету"),
    ("deep_search", "Поиск фильмов/сериалов по бюджету и рейтингу"),
    ("get_random_movie", "Поиск тайтлов по бюджету и рейтингу")
)
