import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable


def count_salary(vacancies):
    all_salaries = []
    for vacancy in vacancies:
        salary = vacancy.get('salary')
        if not salary:
            continue
        if salary.get('currency') != 'rur':
            continue
        salary_from = salary.get('from')
        salary_to = salary.get('to')

        if salary_from and salary_to:
            prediction = (salary_from + salary_to) / 2
            all_salaries.append(prediction)
        elif salary_from:
            prediction = salary_from * 1.2
            all_salaries.append(prediction)
        elif salary_to:
            prediction = salary_to * 0.8
            all_salaries.append(prediction)
        else:
            continue
    return all_salaries


def create_table(results, title):
    table_data = [
        ('Языки программирования', 'Вакансий найдено', 'Обработано вакансий', 'Примерная зарплата')
    ]
    for lang, result in results.items():
        vacancies_found = result['vacancies_found']
        vacancies_processed = result['vacancies_processed']
        average_salary = result['average_salary']
        table_data.append((lang, vacancies_found, vacancies_processed, average_salary))
    table = AsciiTable(table_data, title)
    return (table.table)


def get_hh_statistics(hh_url):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    salary_data = {}

    for lang in languages:
        vacancies = []
        response = requests.get(hh_url, params={'q': lang, 'locations[]': 'r_14068'})
        response.raise_for_status()
        data = response.json()
        vacancies.extend(data['list'])
        vacancies_found = data['meta']['totalResults']
        pages_number = data['meta']['totalPages']

        page = 1
        while page < pages_number:
            response = requests.get(hh_url, params={'q': lang, 'page': page})
            response.raise_for_status()
            data = response.json()
            vacancies.extend(data['list'])
            page += 1

        salaries = count_salary(vacancies)
        vacancies_processed = len(salaries)
        average_salary = sum(salaries) / vacancies_processed if vacancies_processed else None

        salary_data[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return salary_data


def get_sj_statistics(secret_key, super_job_url):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    salary_static = {}
    headers = {'X-Api-App-Id': secret_key}
    moscow_code = 4
    amount_pages = 100

    for lang in languages:
        page = 0
        all_vacancies = []

        while True:
            params = {
                'keyword': lang,
                'town': moscow_code,
                'page': page,
                'count': amount_pages,
            }

            response = requests.get(super_job_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            objects = data.get('objects', [])
            if not objects:
                break

            all_vacancies.extend(objects)

            if len(objects) < 100:
                break
            page += 1

        total_found = data.get('total', 0)
        salaries = count_salary(objects)
        vacancies_processed = len(salaries)
        average_salary = sum(salaries) / vacancies_processed if vacancies_processed else 0
        salary_static[lang] = {
            "vacancies_found": total_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": int(average_salary)
        }
    return salary_static


def main():
    load_dotenv()

    secret_key = os.environ['SECRET_KEY']
    hh_url = 'https://career.habr.com/api/frontend/vacancies'
    super_job_url = 'https://api.superjob.ru/2.0/vacancies/'

    try:
        hh_work = get_hh_statistics(hh_url)
        title = 'Head Hunter Moscow'
        table = create_table(hh_work, title)
        print(table)

    except requests.exceptions.RequestException as e:
        print('Ошибка на стороне сервера')
    try:
        superjob_work = get_sj_statistics(secret_key, super_job_url)
        title = 'SuperJob Moscow'
        table = create_table(superjob_work, title)
        print(table)
    except requests.exceptions.RequestException as e:
        print('Ошибка на стороне сервера')

if __name__ == '__main__':
    main()
