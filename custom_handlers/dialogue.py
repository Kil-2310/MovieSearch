from loader import bot
from telebot.types import Message, CallbackQuery
from typing import Dict, Any, List, Callable

import api.python_requests as MyRequests
from states.states import ApiTotalStates
from keyboards.reset_btn import get_remove_btn, get_amount_btn

from validation import DataValidator

validator = DataValidator()

# Обработчик данных фильма для дальнейшего показа пользователю
def parse_film_data(film: Dict[str, Any]) -> str:
    return f"""
        🎬 Информация о фильме

        
        🎥 <b>Название:</b> {film['name']}

        📆 <b>Год:</b> {film['year']}

        🏅 <b>Рейтинг:</b> {film['rating']}

        🔥 <b>Жанры:</b> {', '.join(film['genres'])}

        📀 <b>Постер: </b> {film['poster']}

        📖 <b>Описание:</b> {film['description']}
    """

# Функция - менеджер для работы с состояниями
def state_manager(chat_id: int, data_for_remember_name: str | List = None, data_for_remember_value: str | List = None) -> bool:
    """
    Управляет состояниями и возвращает:
    - True: если все состояния обработаны и нужно выполнить финальный запрос
    - False: если нужно продолжить выполнение цепочки
    """

    with bot.retrieve_data(chat_id) as data:

        if data_for_remember_name and data_for_remember_value:
            if isinstance(data_for_remember_name, str) and isinstance(data_for_remember_value, str):
                data[data_for_remember_name] = data_for_remember_value
            else:
                for name, value in zip(data_for_remember_name, data_for_remember_value):
                    if name and value:
                        data[name] = value

        if not data['name_funcs'] and not data['name_states']:
            return True
        
        func_name = data['name_funcs'].pop(0)
        state_name = data['name_states'].pop(0)
        
        state = getattr(ApiTotalStates, state_name)

        print('Cur. state:', state)

    globals()[func_name](chat_id)
    bot.set_state(chat_id, state)
        
    return False

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
        '/movie_by_rating - Поиск фильма/сериала по рейтингу\n'
        '/movie_by_budget - Поиск фильмов по бюджету\n'
        '/random_movie - Получить рандомный фильм/сериал\n'
        '/deep_search - Поиск тайтлов по бюджету и рейтингу'
    )


def show_message_raiting(chat_id: int) -> None:
    bot.send_message(
        chat_id, 
        'Введите рейтинг фильма/сериала в формате: 2.1-5',
        reply_markup=get_remove_btn()
    )


def show_message_budget(chat_id: int) -> None:
    bot.send_message(
        chat_id, 
        'Введите бюджет в долларах, формата: 1900-20000',
        reply_markup=get_remove_btn()
    )


def show_message_deep_search(chat_id: int) -> None:
    try:
        with bot.retrieve_data(chat_id) as data:
            success, movie_data, error = MyRequests.deep_search(data['rating'], data['budget'], data['cur_amount'])

        if success and movie_data:
            for index, el in enumerate(movie_data, start=1):
                if el is None:
                    bot.send_message(chat_id, 'Фильмы, по вашему фильтру, закончились')
                    break
                bot.send_message(chat_id, f'<b>{index}:</b> {parse_film_data(el)}', parse_mode='HTML')
            
            bot.delete_state(chat_id)
            show_main_menu(chat_id)
            return
            
        bot.send_message(chat_id, error)
        
    except Exception as e:
        bot.send_message(chat_id, 'Произошла непонятная ошибка')


# Функция для обработки inline клавиатуры
@bot.callback_query_handler(func=lambda call: call.data.startswith('first'))
def handle_amount_button(call: CallbackQuery) -> None:
    amount = call.data.split('_')

    bot.answer_callback_query(call.id)

    state_manager(call.from_user.id, 'cur_amount', amount[1])
    

# Функция для предоставления выбора количества фильмов и установки соответствующего состояния
def choosing_number_films(chat_id: int, name_states: list | str, name_funcs: list | str) -> None:
    bot.send_message(chat_id, 'Выберете количество фильмов:', 
                    reply_markup=get_amount_btn())
    
    bot.set_state(chat_id, ApiTotalStates.selecting_number_records)

    with bot.retrieve_data(chat_id) as data:
        data['name_funcs'] = [name_funcs] if not isinstance(name_funcs, list) else name_funcs
        data['name_states'] = [name_states] if not isinstance(name_states, list) else name_states


# Состояние для выбора количества фильмов через обычную клавиатуру
@bot.message_handler(state=ApiTotalStates.selecting_number_records)
@decorator_check_reset
def handler_selecting_number_records(message: Message) -> None:
    try:
        message_text = int(message.text.strip())

        state_manager(message.from_user.id, 'cur_amount', message_text)

    except ValueError:
        bot.send_message(message.from_user.id, 
                       'Пожалуйста, введите число или используйте кнопки.')

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


# Обработчик movie_search
@bot.message_handler(commands=['movie_search'])
def hendler_movie_search(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Введите название фильма/сериала:', reply_markup=get_remove_btn())
    bot.set_state(message.from_user.id, ApiTotalStates.movie_search_api)


@bot.message_handler(state=ApiTotalStates.movie_search_api)
@decorator_check_reset
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()

    try:
        validator.validate(message_text, check_on_length=50, check_on_empty_line=True)

        success, movie_data, error = MyRequests.get_movie_by_name(message_text)

        if success and movie_data:
            bot.send_message(message.from_user.id, parse_film_data(movie_data), parse_mode='HTML')
            bot.delete_state(message.from_user.id)
            show_main_menu(message.from_user.id)
            return
        
        bot.send_message(message.from_user.id, error)

    except ValueError as e:
        bot.send_message(message.from_user.id, e)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла непонятная ошибка (')

    
# Обработчик movie_by_rating
@bot.message_handler(commands=['movie_by_rating'])
def handler_movie_by_rating(message: Message) -> None:
    choosing_number_films(message.from_user.id, 'movie_by_rating_api', 'show_message_raiting')


@bot.message_handler(state=ApiTotalStates.movie_by_rating_api)
@decorator_check_reset
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()

    try:
        validator.validate(message_text, check_on_length=10, check_on_empty_line=True)

        if '-' in message_text:
            validator.validate(message_text, check_on_two_parts_with_dash=True, check_on_two_values=True, check_on_range_with_dash = [0, 10])

        else:
            validator.validate(message_text, check_on_range_with_dash = [0, 10])
            
        is_next_state = state_manager(message.from_user.id, 'rating', message_text)
        
        if is_next_state:

            with bot.retrieve_data(message.from_user.id) as data:
                success, movie_data, error = MyRequests.get_movie_by_rating(message_text, data['cur_amount'])
            
            if success and movie_data:
                bot.send_message(message.from_user.id, f'😉 Рейтинг фильмов с оценкой: {message_text}')
                
                for index, el in enumerate(movie_data, start=1):
                    if el is None:
                        bot.send_message(message.from_user.id, 'Фильмы, по вашему фильтру, закончились')
                        break
                    bot.send_message(message.from_user.id, f'<b>{index}:</b> {parse_film_data(el)}', parse_mode='HTML')
                
                show_main_menu(message.from_user.id)
                bot.delete_state(message.from_user.id)
                return

            bot.send_message(message.from_user.id, error)

    except ValueError as e:
        bot.send_message(message.from_user.id, e)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла непонятная ошиба (')


# Обработчик movie_by_budget
@bot.message_handler(commands=['movie_by_budget'])
def handler_movie_by_budget(message: Message) -> None:
    choosing_number_films(message.from_user.id, 'movie_by_budget_api', 'show_message_budget')


@bot.message_handler(state=ApiTotalStates.movie_by_budget_api)
@decorator_check_reset
def hendler_movie_search_api(message: Message) -> None:
    message_text = message.text.strip()
    
    try:
        validator.validate(message_text, check_on_length=14, check_on_empty_line=True, check_on_two_values=True)
        
        is_next_state = state_manager(message.from_user.id, 'budget', message_text)

        if is_next_state:

            with bot.retrieve_data(message.from_user.id) as data:
                success, movie_data, error = MyRequests.get_movie_by_budget(message_text, data['cur_amount'])

            if success and movie_data:
                bot.send_message(message.from_user.id, f'😁 Рейтинг фильмов с бюджетом: {message_text}')

                for index, el in enumerate(movie_data, start=1):
                    if el is None:
                        bot.send_message(message.from_user.id, 'Фильмы, по вашему фильтру, закончились')
                        break
                    bot.send_message(message.from_user.id, f'<b>{index}:</b> {parse_film_data(el)}', parse_mode='HTML')

                bot.delete_state(message.from_user.id)
                show_main_menu(message.from_user.id)
                return

            bot.send_message(message.from_user.id, error)

    except ValueError as e:
        bot.send_message(message.from_user.id, e)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Непонятная ошибка (')
    

# Обработчик random_movie
@bot.message_handler(commands=['random_movie'])
def handler_get_random_movie(message: Message) -> None:

    try:
        success, movie_data, error = MyRequests.get_random_movie()

        if success and movie_data:
            bot.send_message(message.from_user.id, f'Ваш рандомный тайтл\n{parse_film_data(movie_data)}', parse_mode='HTML')
            show_main_menu(message.from_user.id)
            return
        
        bot.send_message(message.from_user.id, error)

    except Exception as e:
        bot.send_message(message.from_user.id, 'Ошибка в работе команды')


# Обработчик deep_search
@bot.message_handler(commands=['deep_search'])
def handler_deep_search(message: Message) -> None:
    choosing_number_films(message.from_user.id, [
                                        'movie_by_rating_api',
                                        'movie_by_budget_api',
                                        'deep_search_api'
                                        ],
                                        [
                                        'show_message_raiting',
                                        'show_message_budget',
                                        'show_message_deep_search'
                                        ])


@bot.message_handler(state=ApiTotalStates.deep_search_api)
@decorator_check_reset
def hendler_movie_search_api(message: Message) -> None:
    ...