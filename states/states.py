from telebot.handler_backends import State, StatesGroup

class ApiTotalStates(StatesGroup):
    movie_search_api = State()
    movie_by_rating_api = State()
    selecting_number_records = State()
    movie_by_budget_api = State()
    deep_search_api = State()