import requests
import json
import sys
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config_data.config import API_TOKEN, SERVER_URL
from typing import Callable

headers = {'X-API-KEY': API_TOKEN}

def try_except_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Ошибка данных: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None
    return wrapper


@try_except_decorator
def get_movie_by_name(name: str) -> Optional[Dict[str, Any]]:

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
        print(f"Фильм '{name}' не найден")
        return None
        
    search_location = data['docs'][0]
    
    return {
        'name': search_location.get('name'),
        'year': search_location.get('year'),
        'description': search_location.get('description'),
        'age_rating': search_location.get('ageRating'),
        'type': search_location.get('type'),
        'id': search_location.get('id'),
        'rating': search_location.get('rating', {}).get('kp'),
        'genres': [genre.get('name') for genre in search_location.get('genres', [])],
        'poster': search_location.get('poster', {}).get('url')
    }


@try_except_decorator
def get_movies_by_rating(rating: str, amount: int = 10) -> list:
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
        print(f"Фильм с рейтингом {rating} не найден")
        return None
    
    total_films = list()

    for film in data['docs']:
        total_films.append({
            'id': film['id'],
            'name': film['name'] if film['name'] is not None else film['alternativeName'],
            'type': film['type'],
            'year': film['year'],
            'genres': [genre['name'] for genre in film.get('genres', [])],
            'rating': film['rating']['kp'] if film.get('rating') and film['rating'].get('kp') is not None and film['rating']['kp'] != 0 else 'Отсутствует',
            'description': film.get('description') if film.get('description') and film['description'] is not None else 'Отсутствует',
            'poster': film['poster']['url'] if film.get('poster') and film['poster'].get('url') and film['poster']['url'] is not None else 'Отсутствует'
        })

    return total_films


@try_except_decorator
def get_movie_by_budget(budget: str, amount: int = 10) -> Optional[Dict[str, Any]]:
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
        print(f"Фильм с бюджетом {budget} не найден")
        return None

    total_films = list()

    for film in data['docs']:
        total_films.append({
            'id': film['id'],
            'name': film['name'] if film['name'] is not None else film['alternativeName'],
            'type': film['type'],
            'year': film['year'],
            'genres': [genre['name'] for genre in film.get('genres', [])],
            'rating': film['rating']['kp'] if film.get('rating') and film['rating'].get('kp') is not None and film['rating']['kp'] != 0 else 'Отсутствует',
            'description': film.get('description') if film.get('description') and film['description'] is not None else 'Отсутствует',
            'poster': film['poster']['url'] if film.get('poster') and film['poster'].get('url') and film['poster']['url'] is not None else 'Отсутствует'
        })

    return total_films

@try_except_decorator
def get_random_movie() -> Optional[Dict[str, Any]]:
    response = requests.get(
        f'{SERVER_URL}/v1.4/movie/random',
        headers=headers
    )
    response.raise_for_status()

    data = response.json()

    return {
        'id': data['id'],
        'name': data['name'] if data['name'] is not None else data['alternativeName'],
        'type': data['type'],
        'year': data['year'],
        'genres': [genre['name'] for genre in data.get('genres', [])],
        'rating': data['rating']['kp'] if data.get('rating') and data['rating'].get('kp') is not None and data['rating']['kp'] != 0 else 'Отсутствует',
        'description': data.get('description') if data.get('description') and data['description'] is not None else 'Отсутствует',
        'poster': data['poster']['url'] if data.get('poster') and data['poster'].get('url') and data['poster']['url'] is not None else 'Отсутствует'
    }


def deep_search(rating: str, budget:str, amount: int = 10) -> Dict[str, Any]:
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
        print(f"Фильм с такими параметрами не найден")
        return None
    
    total_films = list()

    for film in data['docs']:
        total_films.append({
            'id': film['id'],
            'name': film['name'] if film['name'] is not None else film['alternativeName'],
            'type': film['type'],
            'year': film['year'],
            'genres': [genre['name'] for genre in film.get('genres', [])],
            'rating': film['rating']['kp'] if film.get('rating') and film['rating'].get('kp') is not None and film['rating']['kp'] != 0 else 'Отсутствует',
            'description': film.get('description') if film.get('description') and film['description'] is not None else 'Отсутствует',
            'poster': film['poster']['url'] if film.get('poster') and film['poster'].get('url') and film['poster']['url'] is not None else 'Отсутствует'
        })

    return total_films
if __name__ == "__main__":
    movie_data = deep_search('2.1 - 4', '1900 - 2000')
    if movie_data:
        print(json.dumps(movie_data, ensure_ascii=False, indent=2))