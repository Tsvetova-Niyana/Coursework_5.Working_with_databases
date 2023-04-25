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


    #         # cur.execute("""SELECT * FROM employer;""")
    #         # print(cur.fetchall())
    #         # # создание таблиц
    #         # create_table(conn)
    #         #
    #         # # добавление клиентов
    #         # add_client(conn, "Василий", "Пупкин", "pupkin@bk.ru")
    #         # add_client(conn, "Иван", "Сидоров", "sidorov@bk.ru")
    #         # add_client(conn, "Иван", "Иванов", "ivanov@list.ru")
    #         # add_client(conn, "Семен", "Иванов", "ivanovS@list.ru")
    #         # add_client(conn, "Андрей", "Семенов", "aSemenoff@mail.ru")
    #         #
    #         # # проверка информации о добавленных клиентах
    #         # print("Клиенты в базе (без телефонов):")
    #         # select_info_client(conn)
    #         # print()
    #         #
    #         # # добавление телефонов клиентов
    #         # add_phone(conn, 1, "89991234567")
    #         # add_phone(conn, 2, "83331234567")
    #         # add_phone(conn, 1, "87771234567")
    #         # add_phone(conn, 4, "89371234567")
    #         # add_phone(conn, 5, "85551234567")
    #         #
    #         # # проверка информации о добавленных клиентах
    #         # print("Клиенты в базе (инфо с телефонами):")
    #         # select_info_client_with_phone(conn)
    #         # print()
    #         #
    #         # # обновление информации о клиенте с id = 1 (изменяем имя клиента и его номер телефона на позиции 3
    #         # # в справочнике телефонов)
    #         # update_info_client(conn, 1, "Виталий", None, None, "89776655555", 3)
    #         #
    #         # # обновление информации о клиенте с id = 2 (изменяем email клиента)
    #         # update_info_client(conn, 2, None, None, "sidorov@list.ru")
    #         #
    #         # # обновление информации о клиенте с id = 1 (изменяем номер телефона клиента на позиции 3
    #         # # в справочнике телефонов)
    #         # update_info_client(conn, 1, None, None, None, "89116655555", 1)
    #         #
    #         # # проверка информации о клиентах после обновления информации
    #         # print("Информация о клиентах после обновления:")
    #         # select_info_client_with_phone(conn)
    #         # print()
    #         #
    #         # # удаление номера телефона с id = 2
    #         # delete_phone(conn, 2)
    #         #
    #         # print("Информация о клиентах после удаления телефона:")
    #         # select_info_client_with_phone(conn)
    #         # print()
    #         #
    #         # # удаление клиента с id = 2
    #         # delete_client(conn, 2)
    #         #
    #         # print("Информация после удаления клиента:")
    #         # select_info_client_with_phone(conn)
    #         # print()
    #         #
    #         # # поиск клиента по имени
    #         # print("Поиск клиента по имени:")
    #         # search_client_by_info(conn, "Виталий")
    #         # print()
    #         #
    #         # print("Поиск клиента по фамилии:")
    #         # search_client_by_info(conn, None, "Иванов")
    #         # print()
    #         #
    #         # print("Поиск клиента по email:")
    #         # search_client_by_info(conn, None, None, "aSemenoff@mail.ru")
    #         # print()
    #         #
    #         # print("Поиск клиента по телефону:")
    #         # search_client_by_info(conn, None, None, None, "89116655555")
    #
    conn.close()
