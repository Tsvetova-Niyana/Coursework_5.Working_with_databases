from db_manager import *
from get_api_object import get_info_dictionaries, get_info_company, get_info_vacancies

if __name__ == '__main__':

    #   1519011 - ФККГруп
    #   139     - IBS
    #   35065   - Sitronics Group
    #   55828   - Инсайрес
    #   2733062 - Лига Цифровой Экономики
    #   9026346 - Code Mode
    #   1302952 - МБК
    #   2136982 - ООО Квантбокс
    #   4649269 - Иннотех
    #   32918   - MANGO OFFICE

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
            for item in range(2):
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

            connect_db.get_companies_and_vacancies_count(cur)

            connect_db.get_all_vacancies(cur)

            connect_db.get_avg_salary(cur)

            connect_db.get_vacancies_with_higher_salary(cur)

    conn.close()
