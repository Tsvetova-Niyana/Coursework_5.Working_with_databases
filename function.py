from db_manager import *
from get_api_object import get_info_dictionaries, get_info_company, get_info_vacancies


def user_interaction():
    connect_db = DBManager(database="coursework_working_with_databases", user="postgres",
                           password="postgres")

    with connect_db.connect as conn:
        with conn.cursor() as cur:

            # удаление таблиц
            connect_db.drop_table(cur)

            # создание таблиц
            connect_db.create_table(cur)

            # получение справочников с hh.ru
            response_dictionaries = get_info_dictionaries()

            # заполнение таблицы об опыте (experience)
            connect_db.add_experience(cur, response_dictionaries)

            #  заполнение таблицы о режиме занятости (employment)
            connect_db.add_employment(cur, response_dictionaries)

            #  заполнение таблиц компаний и их вакансий (employer / vacancies)
            for item in range(10):
                id_employer = input("Введите идентификатор компании (id_employer): ")

                # получение информации о компании с hh.ru
                response_company = get_info_company(id_employer)

                # заполнение таблицы компаний (employer)
                connect_db.add_employer(cur, response_company)

                # заполнение таблицы вакансий (vacancies)
                for page in range(5):
                    # получение информации о вакансиях компании с hh.ru
                    response_vacancies = get_info_vacancies(id_employer, page)

                    # добавление вакансий в таблицу
                    connect_db.add_vacancies(cur, response_vacancies)

            is_get_companies_and_vacancies_count = input("Вывести перечень компаний с указанием количества "
                                                         "открытых вакансий [да/нет]: ")
            if is_get_companies_and_vacancies_count == 'да':
                connect_db.get_companies_and_vacancies_count(cur)

            is_get_all_vacancies = input("\nВывести перечень вакансий [да/нет]: ")
            if is_get_all_vacancies == 'да':
                connect_db.get_all_vacancies(cur)

            is_get_avg_salary = input("\nВывести среднюю зарплату по вакансиям [да/нет]: ")
            if is_get_avg_salary == 'да':
                connect_db.get_avg_salary(cur)

            is_get_vacancies_with_higher_salary = input("\nВывести вакансии с зарплатой "
                                                        "выше среднего значения [да/нет]: ")
            if is_get_vacancies_with_higher_salary == 'да':
                connect_db.get_vacancies_with_higher_salary(cur)

            is_get_vacancies_with_keyword = input("\nПоиск вакансий по ключевому слову [да/нет]: ")
            if is_get_vacancies_with_keyword == 'да':
                keyword = input('Введите ключевое слово поиска: ')
                connect_db.get_vacancies_with_keyword(cur, keyword)

    conn.close()
