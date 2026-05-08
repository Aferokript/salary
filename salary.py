def get_salary_sj():
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    result = {}

    for lang in languages:
        page = 0
        all_vacancies = []
        count_per_page = 100
        headers = {'X-Api-App-Id': SECRET_KEY}
        total_found = 0

        while True:
            params = {
                'keyword': lang,
                'town': 4,
                'page': page,
                'count': count_per_page
            }

            response = requests.get(SUPER_JOB_URL, headers=headers, params=params)
            data = response.json()

            if page == 0:
                total_found = data.get('total', 0)

            objects = data.get('objects', [])

            if not objects:
                break

            all_vacancies.extend(objects)

            if len(objects) < count_per_page:
                break

            page += 1

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

        result[lang] = {
            "vacancies_found": total_found,
            "vacancies_processed": processed,
            "average_salary": int(avg)
        }

    return result

v = get_salary_sj()


def print_table(vacancies):
    title = 'superjob_moscow'
    table_data = (
        ('languages', 'vacancies_found', 'vacancies_processed', 'average_salary'),
    )
    table = AsciiTable(table_data, title)
    print(table.table)



print_table(v)


