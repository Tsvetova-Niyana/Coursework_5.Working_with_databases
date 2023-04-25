-- создание БД для курсовой работы
create database coursework_working_with_databases;

-- создание таблицы employer
create table employer (
id varchar(20) primary key,
name_company varchar(150) not null,
site_url varchar(150),
alternate_url varchar(150),
open_vacancies int,
area_name varchar(20)
);

-- создание таблицы experience
create table experience(
id_experience varchar(20) primary key,
name_experience varchar(150)
);

-- создание таблицы employment
create table employment(
id_employment varchar(20) primary key,
name_employment varchar(150)
);

-- создание таблицы vacancies
create table vacancies(
id varchar(20) primary key,
name_vacancy varchar(150) not null,
department varchar(150),
area_name varchar(20),
salary_from int,
salary_to int, 
salary_currency varchar(10),
published_at timestamp,
alternate_url varchar(150),
employer_id varchar(20) references employer(id),
experience_name varchar(20) references experience(id_experience),
employment_name varchar(20) references employment(id_employment),
address varchar(150)
);


-- проверка таблиц после заполнения
select * from employer e;

select * from vacancies v;

select * from employment e ;

select * from experience e ;

select distinct employer_id from vacancies v ;

--Функция для получения из БД списка всех компаний и количество вакансий у каждой компании.
select e.name_company, e.open_vacancies from employer e;

--Функция для получения из БД списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

select 
	v.employer_id,
	e.name_company,
	v.name_vacancy, 
	coalesce(v.salary_from, 0) as salary_from, 
	coalesce(v.salary_to, 0) as salary_to, 
	coalesce(v.salary_currency, 'Не указано') as salary_currency, 
	v.alternate_url 
from vacancies v
join employer e on v.employer_id = e.id;

--Функция для получения из БД средней зарплаты по вакансиям (по нижней границе).

select round(avg(v.salary_from), 2)
from vacancies v;

--Функция для получения из БД списка всех вакансий, у которых зарплата выше средней по всем вакансиям  

select 
	v.id,
	v.name_vacancy, 
	v.salary_from, 
	v.salary_currency 
from vacancies v
where v.salary_from > (select round(avg(v.salary_from), 2)
						from vacancies v)
order by v.salary_from;
					
--Функция для получения из БД списка всех вакансий, в названии которых содержатся переданные в метод слова, например “python”   

select 
	v.name_vacancy,
	v.area_name,
	coalesce(v.salary_from, 0) as salary_from,
	coalesce (v.salary_to, 0) as salary_to,
	coalesce (v.salary_currency, 'Не указано'),
	v.published_at::date,
	v.alternate_url,
	v.employer_id,
	e.name_company, 
	v.experience_name,
	ex.name_experience, 
	v.employment_name,
	em.name_employment, 
	coalesce (v.address, 'Не указано') as address  
from vacancies v 
join employer e on v.employer_id = e.id 
join experience ex on v.experience_name = ex.id_experience 
join employment em on v.employment_name = em.id_employment 
where v.name_vacancy ilike ('%engineer%');

-- удаление данных из таблиц
delete from vacancies ;
delete  from employer;
delete from experience ;
delete from employment ;

-- удаление таблиц
drop table vacancies ;
drop table employer;
drop table experience ;
drop table employment ;
