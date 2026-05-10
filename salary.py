def print_table(vacancies):
    title = 'superjob_moscow'
    for lang, vacancies_stats in vacancies.items():
        vacancies_found = vacancies_stats.get('vacancies_found')
        vacancies_processed = vacancies_stats.get('vacancies_processed')
        average_salary = vacancies_stats.get('average_salary')
        table_data = (
            ('languages', 'vacancies_found', 'vacancies_processed', 'average_salary'),
            (lang, vacancies_found, vacancies_processed, average_salary),
        )
    table = AsciiTable(table_data, title)
    return (table.table)

v = get_salary_sj()
a = print_table(v)
print(a)
