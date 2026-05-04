import requests

HABR_URL = 'https://career.habr.com/api/frontend/vacancies'


def get_work():
    params = {
        'q': 'python',
    }
    response = requests.get(HABR_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data


def predict_rub_salary(vacancies):

    list_of_vacancies = []
    for vacancy in vacancies:
        salary = vacancy.get('salary')

        if not salary:
            continue

        if salary.get('from') and salary.get('to'):
            predicted = (salary['from'] + salary['to']) / 2

        elif salary.get('from'):
            predicted =  salary['from'] * 1.2

        elif salary.get('to'):
            predicted = salary['to'] * 0.8

        else:
            continue

        list_of_vacancies.append(predicted)
    return list_of_vacancies


def get_salary(work):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']

    result = {}

    for lang in languages:
        params = {'q': lang}
        response = requests.get(f'https://career.habr.com/api/frontend/vacancies', params=params)
        response.raise_for_status()
        vacancies = response.json()
        vacancies_list = vacancies['list']
        vacancies_found = vacancies['meta']['totalResults']
        vacancies_processed = predict_rub_salary(vacancies_list)
        average_salary = sum(vacancies_processed) / len(vacancies_processed) if vacancies_processed else 0
        result[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
        return result


def download_pages(pages):
    url = 'https://career.habr.com/api/frontend/vacancies'
    page = 0
    pages_number = 1

    while page < pages_number:
        page_response = requests.get(url, params={'page': pages_number})
        page_response.raise_for_status()

        page_payload = page_response.json()
        page_payload = page_payload['list']
        page += 1


















