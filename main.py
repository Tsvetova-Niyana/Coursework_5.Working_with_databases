import json
import psycopg2

import requests as requests

from db_manager import add_experience, add_employment, add_employer, drop_table, create_table, add_vacancies


def get_info_company(id_employer):
    # получение информации о компании
    response_company = requests.get(f'https://api.hh.ru/employers/{id_employer}').json()
    return response_company

def get_vacancies(id_employer):
    for page in range(5):
        response_vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={id_employer}',
                                          params={'per_page': 100, 'page': page}).json()
    return response_vacancies


if __name__ == '__main__':

    # получение информации о справочниках
    response_experience = requests.get(f'https://api.hh.ru/dictionaries').json()

    # получение информации об опыте
    for experience in response_experience["experience"]:
        print(experience['id'], experience['name'])
    print()

    # получение информации о занятости
    for employment in response_experience["employment"]:
        print(employment['id'], employment['name'])
    print()



    # получение информации о вакансии
    # for page in range(5):
    #     response_vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id=1519011',
    #                                       params={'per_page': 100, 'page': page}).json()

        # print(response_vacancies['items'][0]['id'])

        # for vac in response_vacancies["items"]:
        #     # print(json.dumps(vac, indent=4, ensure_ascii=False))
        #     print(
        #         vac["id"],
        #         vac["name"],
        #         vac["department"],
        #         vac["area"]["name"],
        #         vac["salary"]["from"],
        #         vac["salary"]["to"],
        #         vac["salary"]["currency"],
        #         vac["published_at"],
        #         vac["alternate_url"],
        #         vac["employer"]["id"],
        #         vac["experience"]["id"],
        #         vac["employment"]["id"]
        #         # vac["address"]["raw"]
        #     )

        # print(json.dumps(response_vacancies["items"], indent=4, ensure_ascii=False))

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



    with psycopg2.connect(database="coursework_working_with_databases", user="postgres",
                          password="postgres") as conn:
        with conn.cursor() as cur:
            # удаление таблиц
            drop_table(cur)

            # создание таблиц
            create_table(cur)

            # заполнение таблицы об опыте
            add_experience(cur, response_experience)

            #  заполнение таблицы о режиме занятости
            add_employment(cur, response_experience)

            #  заполнение таблицы компаний
            for item in range(10):
                id_employer = input("Введите идентификатор компании (id_employer): ")
                response_company = get_info_company(id_employer)
                add_employer(cur, response_company)

                for page in range(5):
                    response_vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={id_employer}',
                                                      params={'per_page': 100, 'page': page}).json()
                    add_vacancies(cur, response_vacancies)

                # заполнение таблицы вакансий
                #     for vac in response_vacancies["items"]:
                #         print(vac)
                #         if vac["address"].get('raw') == None:
                #             address = None
                #         else:
                #             address = vac["address"]["raw"]
                #
                #         cur.execute("""
                #                         INSERT INTO vacancies(
                #                         id,
                #                         name_vacancy,
                #                         department,
                #                         area_name,
                #                         salary_from,
                #                         salary_to,
                #                         salary_currency,
                #                         published_at,
                #                         alternate_url,
                #                         employer_id,
                #                         experience_name,
                #                         employment_name,
                #                         address)
                #                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, , %s);
                #                         """, (
                #             vac["id"],
                #             vac["name"],
                #             vac["department"],
                #             vac["area"]["name"],
                #             vac["salary"]["from"],
                #             vac["salary"]["to"],
                #             vac["salary"]["currency"],
                #             vac["published_at"],
                #             vac["alternate_url"],
                #             vac["employer"]["id"],
                #             vac["experience"]["id"],
                #             vac["employment"]["id"],
                #             address))

    #
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
    for page in range(5):
        response_vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id=1519011',
                                          params={'per_page': 100, 'page': page}).json()
        for vac in response_vacancies["items"]:
            print(vac)