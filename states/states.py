from telebot.handler_backends import State, StatesGroup

class ApiTotalStates(StatesGroup):
    movie_search_api = State()
    movies_by_rating_api = State()
    selecting_number_records = State()
    movies_by_budget_api = State()
    selecting_number_records_budget = State()
    deep_search_api = State()