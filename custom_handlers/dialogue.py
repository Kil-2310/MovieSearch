from loader import bot
from telebot.types import Message, CallbackQuery

import api.python_requests as MyRequests
from states.states import ApiTotalStates
from keyboards.reset_btn import get_remove_btn, get_amount_btn

from validation import DataValidator

from typing import Callable

validator = DataValidator()

# Функция - менеджер для работы с состояниями
def bool_state_manager(chat_id: int) -> None:
    with bot.retrieve_data(chat_id) as data:

        if not data['name_funcs'] and not data['name_states']:
            return True
        
    return False

def state_manager(chat_id: int) -> None:
    with bot.retrieve_data(chat_id) as data:
        print('state_manager befo:', data)

        if not data['name_funcs'] and not data['name_states']:
            return True
        
        func = data['name_funcs'].pop(0)
        globals()[func](chat_id)

        state = getattr(ApiTotalStates, data['name_states'].pop(0))
        print()
        print('state_manager afte:', data)
        print('Cur. state', state)
        print()
        bot.set_state(chat_id, state)
        
    return False

# ===== Декораторы =====

# Декоратор для сброса бота
def decorator_check_reset(func: Callable) -> Callable:
    def wrapper(message: Message) -> None:
        if message.text == '🔄 Перезапустить бота':
            user_id = message.from_user.id
            current_state = bot.get_state(user_id)
            if current_state:
                bot.delete_state(user_id)
                bot.send_message(
                    user_id,
                    "Все состояния сброшены. Бот перезапущен.",
                )
            show_main_menu(user_id)
            return
        
        func(message)
    return wrapper

# ===== Функции для показа информативных сообщений =====

# Главное меню бота
def show_main_menu(chat_id: int) -> None:
    bot.send_message(
        chat_id,
        '/help - Вывести справку\n'
        '/movie_search - Поиск фильма/сериала по названию\n'
        '/movies_by_rating - Поиск фильма/сериала по рейтингу\n'
        '/movie_by_budget - Поиск фильмов по бюджету\n'
        '/random_movie - Получить рандомный фильм/сериал\n'
        '/deep_search - Поиск тайтлов по бюджету и рейтингу'
    )


def show_message_raiting(chat_id: int) -> None:
    bot.send_message(
        chat_id, 
        'Введите рейтинг фильма/сериала в например:\n'
        '• 4.3\n'
        '• 3\n'
        '• 2.1-5:',
        reply_markup=get_remove_btn()
    )


def show_message_budget(chat_id: int) -> None:
    bot.send_message(
        chat_id, 
        'Введите бюджет в долларах $, формата: 1900-20000',
        reply_markup=get_remove_btn()
    )

def show_message_deep_search(chat_id: int) -> None:
    try:
        print('show_message_deep_search')
        with bot.retrieve_data(chat_id) as data:
            print(data, '=================')
            movie_data = MyRequests.deep_search(data['rating'], data['budget'], data['cur_amount'])
            print(movie_data)
        for index, el in enumerate(movie_data, start=1):
            message_for_user = f"""
                🎬 Информация о фильме

                
                🎥 <b>Название:</b> {el['name']}

                📆 <b>Год:</b> {el['year']}

                🏅 <b>Рейтинг:</b> {el['rating']}

                🔥 <b>Жанры:</b> {', '.join(el['genres'])}

                📀 <b>Постер: </b> {el['poster']}

                📖 <b>Описание:</b> {el['description']}
            """
            if el is None:
                bot.send_message(chat_id, 'Фильмы, по вашему фильтру, закончились')
                break
            bot.send_message(chat_id, f'<b>{index}:</b> {message_for_user}', parse_mode='HTML')
    
    except Exception as e:
        bot.send_message(chat_id, e)
    

# ===== Функции для установки состояний =====

# Функция для предоставления выбора количества фильмов
def choosing_number_films(chat_id: int, name_states: list | str, name_funcs: list | str) -> None:
    bot.send_message(chat_id, 'Выберете количество фильмов:', 
                    reply_markup=get_amount_btn())
    
    bot.set_state(chat_id, ApiTotalStates.selecting_number_records)

    with bot.retrieve_data(chat_id) as data:
        data['name_funcs'] = [name_funcs] if not isinstance(name_funcs, list) else name_funcs
        data['name_states'] = [name_states] if not isinstance(name_states, list) else name_states

@bot.message_handler(state=ApiTotalStates.selecting_number_records)
def handler_selecting_number_records(message: Message) -> None:
    try:
        message_text = int(message.text.strip())

        state_manager(message.from_user.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['cur_amount'] = message_text


    except ValueError:
        bot.send_message(message.from_user.id, 
                       'Пожалуйста, введите число или используйте кнопки.')


# ===== Функции для обработки inline клавиатуры =====

@bot.callback_query_handler(func=lambda call: call.data.startswith('first'))
def handle_amount_button(call: CallbackQuery):
    amount = call.data.split('_')

    bot.answer_callback_query(call.id)
    with bot.retrieve_data(call.from_user.id) as data:
        print(data)
        data['cur_amount'] = int(amount[1])

    state_manager(call.from_user.id)

# ===== Основной код бота =====

# Обработчик start
@bot.message_handler(commands=['start'])
def start_message_handler(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Привет, я бот - Роман, помогу Вам найти любые фильмы и сериалы. Просты выберете команду ниже:')
    show_main_menu(message.from_user.id)

# Обработчик help
@bot.message_handler(commands=['help'])
def help_message_handler(message: Message) -> None:
    show_main_menu(message.from_user.id)

# Нахождение тайтла по названию
@bot.message_handler(commands=['movie_search'])
def hendler_movie_search(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Введите название фильма/сериала:', reply_markup=get_remove_btn())
    bot.set_state(message.from_user.id, ApiTotalStates.movie_search_api)


@bot.message_handler(state=ApiTotalStates.movie_search_api)
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()

    try:
        validator.validate(message_text, check_on_length=50, check_on_empty_line=True)

        movie_data = MyRequests.get_movie_by_name(message_text)

        if not movie_data is None:
            message_for_user = f"""
                🎬 Информация о фильме

                
                🎥 <b>Название:</b> {movie_data['name']}

                📆 <b>Год:</b> {movie_data['year']}

                🏅 <b>Рейтинг:</b> {movie_data['rating']}

                🔥 <b>Жанры:</b> {', '.join(movie_data['genres'])}

                📀 <b>Постер: </b> {movie_data['poster']}

                📖 <b>Описание:</b> {movie_data['description']}
            """

            bot.send_message(message.from_user.id, message_for_user, parse_mode='HTML')
            bot.delete_state(message.from_user.id)
            return
        
        bot.send_message(message.from_user.id, 'Произошла ошибка, попробуйте еще раз')

    except Exception as e:
        bot.send_message(message.from_user.id, e)

    

# Получение списа тайтлов по рейтингу  
@bot.message_handler(commands=['movies_by_rating'])
def handler_movies_by_rating(message: Message) -> None:
    choosing_number_films(message.from_user.id, 'movies_by_rating_api', 'show_message_raiting')


@bot.message_handler(state=ApiTotalStates.movies_by_rating_api)
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()

    try:
        validator.validate(message_text, check_on_length=10, check_on_empty_line=True)

        if '-' in message_text:
            validator.validate(message_text, check_on_two_parts_with_dash=True, check_on_two_values=True, check_on_range_with_dash = [0, 10])

        else:
            validator.validate(message_text, check_on_range = [0, 10])
            
        res_states = state_manager(message.from_user.id)

        with bot.retrieve_data(message.from_user.id) as data:
            if res_states:
                movie_data = MyRequests.get_movies_by_rating(message_text, data['cur_amount'])
            else:
                data['rating'] = message_text
        if res_states and not movie_data is None:
            bot.send_message(message.from_user.id, f'😉 Рейтинг фильмов с оценкой: {message_text}')
            print(movie_data)
            for index, el in enumerate(movie_data, start=1):
                message_for_user = f"""
                    🎬 Информация о фильме

                    
                    🎥 <b>Название:</b> {el['name']}

                    📆 <b>Год:</b> {el['year']}

                    🏅 <b>Рейтинг:</b> {el['rating']}

                    🔥 <b>Жанры:</b> {', '.join(el['genres'])}

                    📀 <b>Постер: </b> {el['poster']}

                    📖 <b>Описание:</b> {el['description']}
                """
                if el is None:
                    bot.send_message(message.from_user.id, 'Фильмы, по вашему фильтру, закончились')
                    break
                bot.send_message(message.from_user.id, f'<b>{index}:</b> {message_for_user}', parse_mode='HTML')
            
            bot.delete_state(message.from_user.id)

    except ValueError as e:
        bot.send_message(message.from_user.id, 'Ведите число')
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла ошибка, проверьте формат вводимых данных')

# Получение фильмов по бюджету
@bot.message_handler(commands=['movie_by_budget'])
def handler_movie_by_budget(message: Message) -> None:
    choosing_number_films(message.from_user.id, 'movies_by_budget_api', 'show_message_budget')

@bot.message_handler(state=ApiTotalStates.movies_by_budget_api)
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()
    
    try:
        validator.validate(message_text, check_on_length=14, check_on_empty_line=True, check_on_two_values=True)
        
        with bot.retrieve_data(message.from_user.id) as data:
            data['budget'] = message_text
        
        res_states = state_manager(message.from_user.id)

        with bot.retrieve_data(message.from_user.id) as data:
            if res_states:
                movie_data = MyRequests.get_movie_by_budget(message_text, data['cur_amount'])

            
        if res_states and not movie_data is None:
            bot.send_message(message.from_user.id, f'😁 Рейтинг фильмов с бюджетом: {message_text}')

            for index, el in enumerate(movie_data, start=1):
                message_for_user = f"""
                    🎬 Информация о фильме

                    
                    🎥 <b>Название:</b> {el['name']}

                    📆 <b>Год:</b> {el['year']}

                    🏅 <b>Рейтинг:</b> {el['rating']}

                    🔥 <b>Жанры:</b> {', '.join(el['genres'])}

                    📀 <b>Постер: </b> {el['poster']}

                    📖 <b>Описание:</b> {el['description']}
                """
                if el is None:
                    bot.send_message(message.from_user.id, 'Фильмы, по вашему фильтру, закончились')
                    break
                bot.send_message(message.from_user.id, f'<b>{index}:</b> {message_for_user}', parse_mode='HTML')

            bot.delete_state(message.from_user.id)

    except ValueError as e:
        bot.send_message(message.from_user.id, e)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка команды')
    


# Получение рандомного тайтала
@bot.message_handler(commands=['random_movie'])
def handler_get_random_movie(message: Message) -> None:

    try:
        movie_data = MyRequests.get_random_movie()
    
        message_for_user = f"""
            🎬 Информация о фильме

            
            🎥 <b>Название:</b> {movie_data['name']}

            📆 <b>Год:</b> {movie_data['year']}

            🏅 <b>Рейтинг:</b> {movie_data['rating']}

            🔥 <b>Жанры:</b> {', '.join(movie_data['genres'])}

            📀 <b>Постер: </b> {movie_data['poster']}

            📖 <b>Описание:</b> {movie_data['description']}
        """

        bot.send_message(message.from_user.id, f'Ваш рандомный тайтл\n{message_for_user}', parse_mode='HTML')
    
    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка в работе команды')


# Глубокий поиск фильмов по рейтингу, годам, жанру, бюджету и актерам
@bot.message_handler(commands=['deep_search'])
def handler_deep_search(message: Message) -> None:
    choosing_number_films(message.from_user.id, ['movies_by_rating_api', 'movies_by_budget_api', 'deep_search_api'], ['show_message_raiting', 'show_message_budget', 'show_message_deep_search'])

@bot.message_handler(state=ApiTotalStates.deep_search_api)
def hendler_movie_search_api(message: Message) -> None:
    state_manager(message.from_user.id)
    bot.delete_state(message.from_user.id)