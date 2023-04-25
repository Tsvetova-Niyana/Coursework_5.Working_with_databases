import requests


def get_info_company(id_employer):
    """Получение информации о компании"""
    response_company = requests.get(f'https://api.hh.ru/employers/{id_employer}').json()
    return response_company


def get_info_vacancies(id_employer, page):
    """Получение информации о компании"""
    response_vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={id_employer}',
                                      params={'per_page': 100, 'page': page}).json()
    return response_vacancies


def get_info_dictionaries():
    """Получение информации о справочниках"""
    response_dictionaries = requests.get(f'https://api.hh.ru/dictionaries').json()
    return response_dictionaries
