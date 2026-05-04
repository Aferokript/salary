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
        salaries = predict_rub_salary(vacancies_list)
        processed = len(salaries)
        average_salary = sum(salaries) / processed if processed else 0

        vacancies_list = []
        page = 0
        pages_number = vacancies['meta']['totalPages']

        while page < pages_number:
            page_response = requests.get(url, params={'page': page})
            page_response.raise_for_status()
            page_payload = page_response.json()
            page_payload = page_payload['list']
            vacancies_list.extend(page_payload)

            page += 1

        result[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": salaries,
            "average_salary": average_salary
        }
    return result


work = get_work()



















