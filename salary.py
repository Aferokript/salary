def get_salary(work):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    url = 'https://career.habr.com/api/frontend/vacancies'
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

        page = 0
        pages_number = 1

        while page < pages_number:
            page_response = requests.get(url, params={'page': pages_number})
            page_response.raise_for_status()

            page_payload = page_response.json()
            page_payload = page_payload['list']
            page += 1

        result[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
        return result

work = get_work()
salary = get_salary(work)
print(salary)



















