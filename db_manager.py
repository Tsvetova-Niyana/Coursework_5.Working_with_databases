"""
Создать класс DBManager для работы с данными в БД.
Создайте класс `DBManager`, который будет подключаться к БД Postgres и иметь следующие методы:

- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и
    зарплаты и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем
    вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в
    метод слова, например “python”.
"""
import psycopg2


class DBManager:

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

    @property
    def connect(self):
        connect = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password)

        return connect

    @staticmethod
    def drop_table(cur):
        cur.execute("""
                DROP TABLE IF EXISTS vacancies;      
                DROP TABLE IF EXISTS experience;
                DROP TABLE IF EXISTS employment;    
                DROP TABLE IF EXISTS employer;      
                """)

    @staticmethod
    def create_table(cur):
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS employer (
                    id varchar(20) PRIMARY KEY,
                    name_company varchar(150) NOT NULL,
                    site_url varchar(150),
                    alternate_url varchar(150),
                    open_vacancies int,
                    area_name varchar(20)
                    );     
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS experience(
                    id_experience varchar(20) PRIMARY KEY,
                    name_experience varchar(150) NOT NULL
                    );     
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS employment(
                    id_employment varchar(20) PRIMARY KEY,
                    name_employment varchar(150) NOT NULL
                    );    
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies(
                    id varchar(20) PRIMARY KEY,
                    name_vacancy varchar(150) NOT NULL,
                    department varchar(150),
                    area_name varchar(20),
                    salary_from int,
                    salary_to int, 
                    salary_currency varchar(10),
                    published_at timestamp,
                    alternate_url varchar(150),
                    employer_id varchar(20) REFERENCES employer(id),
                    experience_name varchar(20) REFERENCES experience(id_experience),
                    employment_name varchar(20) REFERENCES employment(id_employment),
                    address varchar(150)
                    );    
                    """)

    @staticmethod
    def add_experience(cur, response_experience):
        for experience in response_experience["experience"]:
            cur.execute("""
                            INSERT INTO experience(
                            id_experience,
                            name_experience
                            )
                            VALUES (%s, %s)
                            ON CONFLICT (id_experience)
                            DO NOTHING;
                            """, (
                experience["id"],
                experience['name']
            ))

    @staticmethod
    def add_employment(cur, response_experience):
        for employment in response_experience["employment"]:
            cur.execute("""
                        INSERT INTO employment(
                        id_employment,
                        name_employment
                        )
                        VALUES (%s, %s)
                        ON CONFLICT (id_employment)
                        DO NOTHING;
                        """, (
                employment["id"],
                employment['name']
            ))

    @staticmethod
    def add_employer(cur, response_company):
        cur.execute("""
            INSERT INTO employer(
            id,
            name_company,
            site_url,
            alternate_url,
            open_vacancies,
            area_name)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO NOTHING;
            """, (
            response_company["id"],
            response_company["name"],
            response_company["site_url"],
            response_company["alternate_url"],
            response_company["open_vacancies"],
            response_company["area"]["name"]))

    @staticmethod
    def add_vacancies(cur, response_vacancies):
        # заполнение таблицы вакансий
        for vac in response_vacancies["items"]:
            if vac["address"] is None:
                address = None
            else:
                address = vac["address"]["raw"]

            if vac["salary"] is None:
                salary_from = None
            else:
                salary_from = vac["salary"]["from"]

            if vac["salary"] is None:
                salary_to = None
            else:
                salary_to = vac["salary"]["to"]

            if vac["salary"] is None:
                salary_currency = None
            else:
                salary_currency = vac["salary"]["currency"]

            cur.execute("""
                                INSERT INTO vacancies(
                                id,
                                name_vacancy,
                                department,
                                area_name,
                                salary_from,
                                salary_to,
                                salary_currency,
                                published_at,
                                alternate_url,
                                employer_id,
                                experience_name,
                                employment_name,
                                address)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id)
                                DO NOTHING;
                                """, (
                vac["id"],
                vac["name"],
                vac["department"],
                vac["area"]["name"],
                salary_from,
                salary_to,
                salary_currency,
                vac["published_at"],
                vac["alternate_url"],
                vac["employer"]["id"],
                vac["experience"]["id"],
                vac["employment"]["id"],
                address))

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """
        Функция для получения из БД списка всех компаний и количество вакансий у каждой компании.
        """

        cur.execute("""SELECT 
        e.name_company, 
        e.open_vacancies 
        FROM employer e;""")
        company_query = cur.fetchall()

        for company in company_query:
            print(f'\nНазвание компании: {company[0]}\nКоличество открытых вакансий: {company[1]}')

    @staticmethod
    def get_all_vacancies(cur):
        """
        Функция для получения из БД списка всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию.
        """

        cur.execute(
            """
            SELECT
                e.name_company,
                v.name_vacancy, 
                coalesce(v.salary_from, 0) as salary_from, 
                coalesce(v.salary_to, 0) as salary_to, 
                coalesce(v.salary_currency, 'Не указано') as salary_currency, 
                v.alternate_url 
            FROM vacancies v
            JOIN employer e ON v.employer_id = e.id;
            """
        )

        result = cur.fetchall()

        for vacancy in result:
            print(f'\nКомпания: {vacancy[0]}\n'
                  f'Вакансия: {vacancy[1]}\n'
                  f'Диапазон зарплаты: {vacancy[2]} - {vacancy[3]}\n'
                  f'Валюта зарплаты: {vacancy[4]}\n'
                  f'Ссылка на вакансию: {vacancy[5]}')

    @staticmethod
    def get_avg_salary(cur):
        """
         Функция для получения из БД средней зарплаты по вакансиям (по нижней границе).
        """
        cur.execute(
            """
            SELECT ROUND(AVG(v.salary_from), 2) as salary_from
            FROM vacancies v;
            """
        )

        result = cur.fetchall()

        print(f'\nСредняя зарплата по вакансиям (срез по нижней границе) - {result[0][0]}')

    @staticmethod
    def get_vacancies_with_higher_salary(cur):
        """
        Функция для получения из БД списка всех вакансий, у которых зарплата выше средней по всем
        вакансиям
        """

        cur.execute(
            """
            SELECT 
                v.name_vacancy, 
                v.salary_from, 
                v.salary_currency 
            FROM vacancies v
            WHERE v.salary_from > (SELECT ROUND(AVG(v.salary_from), 2) FROM vacancies v);
            """
        )

        result = cur.fetchall()

        for vacancy in result:
            print(f"Вакансия: {vacancy[0]}, зарплата: {vacancy[1]} {vacancy[2]}")
