import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable


load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
HH_URL = 'https://career.habr.com/api/frontend/vacancies'
SUPER_JOB_URL = 'https://api.superjob.ru/2.0/vacancies/'


def hh_statistics():
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    results = {}

    for lang in languages:
        vacancies_list = []
        response = requests.get(HH_URL, params={'q': lang, 'locations[]': 'r_14068'})
        data = response.json()
        vacancies_list.extend(data['list'])
        vacancies_found = data['meta']['totalResults']
        pages_number = data['meta']['totalPages']

        page = 1
        while page < pages_number:
            response = requests.get(HH_URL, params={'q': lang, 'page': page})
            data = response.json()
            vacancies_list.extend(data['list'])
            page += 1

        salaries = []
        for vacancy in vacancies_list:
            salary = vacancy.get('salary')
            if not salary:
                continue
            if salary.get('currency') != 'rur':
                continue
            salary_from = salary.get('from')
            salary_to = salary.get('to')

            if salary_from and salary_to:
                pred = (salary_from + salary_to) / 2
            elif salary_from:
                pred = salary_from * 1.2
            elif salary_to:
                pred = salary_to * 0.8
            else:
                continue
            salaries.append(pred)

        processed = len(salaries)
        avg = sum(salaries) / processed if processed > 0 else 0
        results[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": processed,
            "average_salary": int(avg)
        }
        title = 'Head Hunter Moscow'
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


def sj_statistics():
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    results = {}
    headers = {'X-Api-App-Id': SECRET_KEY}

    for lang in languages:
        page = 0
        all_vacancies = []

        while True:
            params = {
                'keyword': lang,
                'town': 4,
                'page': page,
                'count': 100
            }

            response = requests.get(SUPER_JOB_URL, headers=headers, params=params)
            data = response.json()

            objects = data.get('objects', [])
            if not objects:
                break

            all_vacancies.extend(objects)

            if len(objects) < 100:
                break
            page += 1

        total_found = data.get('total', 0)

        salaries = []
        for vacancy in all_vacancies:
            payment_from = vacancy.get('payment_from')
            payment_to = vacancy.get('payment_to')

            if not payment_from and not payment_to:
                continue

            if payment_from and payment_to:
                pred = (payment_from + payment_to) / 2
            elif payment_from:
                pred = payment_from * 1.2
            elif payment_to:
                pred = payment_to * 0.8
            else:
                continue

            salaries.append(pred)

        processed = len(salaries)
        avg = sum(salaries) / processed if processed > 0 else 0

        results[lang] = {
            "vacancies_found": total_found,
            "vacancies_processed": processed,
            "average_salary": int(avg)
        }

        title = 'SuperJob Moscow'
        table_data = [
            ('Языки программирования', 'Вакансий найдено', 'Обработано вакансий', 'Примерная зарплата')
        ]

        for lang, result in results.items():
            vacancies_found = result.get('vacancies_found')
            vacancies_processed = result.get('vacancies_processed')
            average_salary = result.get('average_salary')
            table_data.append((lang, vacancies_found, vacancies_processed, average_salary))
        table = AsciiTable(table_data, title)
    return (table.table)


def main():
    try:
        hh_vacations = hh_statistics()
        print(hh_vacations)
    except requests.exceptions.RequestException as e:
        print('Ошибка на стороне сервера')
    try:
        superjob_vacations  = sj_statistics()
        print(superjob_vacations)
    except requests.exceptions.RequestException as e:
        print('Ошибка на стороне сервера')

if __name__ == '__main__':
    main()

