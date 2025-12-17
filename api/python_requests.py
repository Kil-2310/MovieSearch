import requests
from typing import Dict, Any, List, Tuple

# from config_data.config import API_TOKEN, SERVER_URL
from typing import Callable
BOT_TOKEN = '8528315371:AAF9PiqUBEhjgUTU9VpQbS6LL0LkARGGS4M'
API_TOKEN = 'QR6BNFX-7YC4D2M-HWENZ72-SFJRKAH'
SERVER_URL = 'https://api.poiskkino.dev'

headers = {'X-API-KEY': API_TOKEN}

def parse_film_data(film: Dict[str, Any]) -> Dict[str, Any]:
    
    return {
        'id': film['id'],
        'name': film['name'] if film['name'] is not None else film['alternativeName'],
        'type': film['type'],
        'year': film['year'],
        'genres': [genre['name'] for genre in film.get('genres', [])],
        'rating': film['rating']['kp'] if film.get('rating') and film['rating'].get('kp') is not None and film['rating']['kp'] != 0 else 'Отсутствует',
        'description': film.get('description') if film.get('description') and film['description'] is not None else 'Отсутствует',
        'poster': film['poster']['url'] if film.get('poster') and film['poster'].get('url') and film['poster']['url'] is not None else 'Отсутствует'
    }


def try_except_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Tuple[bool, Dict | List | None, str | None]:
        try:
            result = func(*args, **kwargs)
            return True, result, None
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка сети: {e}"
            print(error_msg)
            return False, None, error_msg
        except (KeyError, IndexError) as e:
            error_msg = f"Ошибка данных: {e}"
            print(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Ошибка: {e}"
            print(error_msg)
            return False, None, error_msg
        except ValueError as e:
            error_msg = f"{e}"
            print(error_msg)
            return False, None, error_msg
    return wrapper


@try_except_decorator
def get_movie_by_name(name: str) -> Dict[str, Any] | None:

    response = requests.get(
        f'{SERVER_URL}/v1.4/movie/search',
        params={
            'query': name,
            'limit': 1
            },
        headers=headers
    )
    response.raise_for_status()
    
    data = response.json()
    
    if not data.get('docs'):
        raise ValueError(f"Фильм '{name}' не найден")

    return parse_film_data(data['docs'][0])


@try_except_decorator
def get_movie_by_rating(rating: str, amount: int = 10) -> List[Dict[str, Any]] | None:
    response = requests.get(
        f'{SERVER_URL}/v1.4/movie',
        params={
                'rating.kp': rating,
                'limit': amount
            },
        headers=headers
    )
    response.raise_for_status()

    data = response.json()
    
    if not data.get('docs'):
        raise ValueError(f"Фильм с рейтингом {rating} не найден")
    
    return [parse_film_data(film) for film in data['docs']]


@try_except_decorator
def get_movie_by_budget(budget: str, amount: int = 10) -> List[Dict[str, Any]] | None:
    response = requests.get(
        f'{SERVER_URL}/v1.4/movie',
        params={
                'budget.value': budget,
                'limit': amount
            },
        headers=headers
    )
    response.raise_for_status()

    data = response.json()

    if not data.get('docs'):
        raise ValueError(f"Фильм с бюджетом {budget} не найден")

    return [parse_film_data(film) for film in data['docs']]

@try_except_decorator
def get_random_movie() -> Dict[str, Any] | None:
    response = requests.get(
        f'{SERVER_URL}/v1.4/movie/random',
        headers=headers
    )
    response.raise_for_status()

    data = response.json()

    return parse_film_data(data)

@try_except_decorator
def deep_search(rating: str, budget: str, amount: int = 1) -> List[Dict[str, Any]] | None:
    response = requests.get(
        f'{SERVER_URL}/v1.4/movie',
        params={
                'budget.value': budget,
                'rating.kp': rating,
                'limit': amount
            },
        headers=headers
    )
    response.raise_for_status()

    data = response.json()

    if not data.get('docs'):
        raise ValueError(f"Фильм с бюджетом {budget} и рейтингом {rating} не найден")

    return [parse_film_data(film) for film in data['docs']]




# success, data, error = deep_search('2.0 - 6', '99 - 1000')
# if success:
#     print(success)
#     print(error)
# else:
#     print(f"Ошибка: {error}")