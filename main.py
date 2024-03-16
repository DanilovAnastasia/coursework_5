from src.hh_api import HeadHunterAPI
from src.DBManager import DBManager
import psycopg2

if __name__ == '__main__':
    hh_api = HeadHunterAPI({})
    db_manager = DBManager('kurs_work')
    employers = None
    while True:
        inp = input(str(
            '\nПривет, вы используете программу для работы с вакансиями с БД и HH.\n'
            'Введите:\n'
            '1 - если хотите загрузить 20 работодателей (увидите первые 20 рандомных работодателей).\n'
            '2 - Заполняем таблицы БД данными.\n'
            '3 - Вывод всех вакансий.\n'
            '4 - Средней залплаты.\n'
            '5 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
            '6 - Вывод списка всех вакансий по содержанию ключевого слова.\n'
            '7 - Cписок всех компаний и количество вакансий у них.\n'
            '8 - Выйти из программы.\n'
            '-> '))
        if inp == '1':
            employers = hh_api.get_employers()
            for employer in employers['items']:
                print(
                    f"{employer['id']=}, {employer['name']=}, {employer['alternate_url']=}, {employer['vacancies_url']=}, {employer['open_vacancies']=}")
            # db_manager.create_database()
            # db_manager.create_tables()
        elif inp == '2':
            db_manager.create_tables()
            if employers is None:
                print('Не чем заполнять, вначале загрузите работодателей.')
                continue
            try:
                # Заполняем таблицу работодатели по employer_id
                for item in employers["items"]:
                    employer_id = item["id"]
                    employer_name = item["name"]
                    employer_description = item["vacancies_url"]
                    employer_website = item["alternate_url"]

                    db_manager.insert_employer(employer_id, employer_name, employer_description, employer_website)

                    vacansies = hh_api.get_vacancies(employer_description)
                    for item1 in vacansies["items"]:
                        vacancy = item1["name"]
                        vacancy_id = item1['id']
                        try:
                            vacancy_salary = int(item1["salary"]["from"])
                        except TypeError:
                            vacancy_salary = 0
                        vacancy_link = item1["alternate_url"]
                        db_manager.insert_vacancy(vacancy_id, employer_id, vacancy, vacancy_salary,
                                                  vacancy_link)
            except psycopg2.errors.UniqueViolation:
                print("Данные уже занесены, повторно не требуется, или удалите и заново создайте таблицу и БД")
            else:
                print("Таблицы успешно заполнены")
        elif inp == "3":
            try:
                all_vacancies = db_manager.get_all_vacancies()
                # Отрабатываем случай если в таблице нет данных
                if all_vacancies == []:
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    for company, title, salary, link in all_vacancies:
                        print(f"Company: {company}")
                        print(f"Title: {title}")
                        print(f"Salary: {salary}")
                        print(f"Link: {link}")
                        print()
            except:
                print('Непредвиденная ошибка, нет соединения с БД, или отсутсвует БД.')
                continue

        elif inp == "4":
            # Средняя залплата по вакансиям
            try:
                avg_salary = db_manager.get_avg_salary()
                if avg_salary == None:
                    print("Не загружены данные в таблицы")
                else:
                    print("Средняя зарплата(без учета нулевых значений по вакансиям:", avg_salary)
            except:
                print('Непредвиденная ошибка, нет соединения с БД, или отсутсвует БД.')
                continue

        elif inp == "5":
            # Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
            try:
                vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
                # Отрабатываем случай если в таблице нет данных
                if vacancies_with_higher_salary == []:
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    for company, title, salary, link in vacancies_with_higher_salary:
                        print(f"Работодатель: {company}")
                        print(f"Описание: {title}")
                        print(f"Зарплата: {salary}")
                        print(f"Ссылка: {link}")
                        print()
            except:
                print('Непредвиденная ошибка, нет соединения с БД, или отсутсвует БД.')
                continue

        elif inp == "6":
            # Вывод списка всех вакансий, в названии которых содержатся ключевое слово
            try:
                keyword = input("Введите ключевое слово")
                vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
                # Отрабатываем случай если в таблице нет данных
                if vacancies_with_keyword == []:
                    print("Нет данных по этому запросу.")
                else:
                    for company, title, salary, link in vacancies_with_keyword:
                        print(f"Работодатель: {company}")
                        print(f"Описание: {title}")
                        print(f"Зарплата: {salary}")
                        print(f"Ссылка: {link}")
                        print()
            except:
                print('Непредвиденная ошибка, нет соединения с БД, или отсутсвует БД.')
                continue

        elif inp == "7":
            # список всех компаний и количество вакансий у каждой компании
            try:
                companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
                # Отрабатываем случай если в таблице нет данных
                if companies_and_vacancies_count == []:
                    print("Нет таблиц, создайте - пункт 2")
                else:
                    print("Компания и количество вакансий:")
                    for company, count in companies_and_vacancies_count:
                        print(f"{company}: {count}")
            except:
                print('Непредвиденная ошибка, нет соединения с БД, или отсутсвует БД.')
                continue

        elif inp == "8":
            # Выход
            db_manager.close_connection()
            print("exit")
            break
        else:
            print('Вы ввели некорректные данные.')
