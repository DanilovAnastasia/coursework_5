import os
import requests
from src.job_api import JobAPI

API_CLIENT_ID = os.getenv('API_KEY_HeadHunter_client_ID')
API_CLIENT_SECRET = os.getenv('API_KEY_HeadHunter_secret')


class HeadHunterAPI(JobAPI):
    """
    Класс реализует анализ информации о вакансиях с HeadHunter.ru
    """

    api_client_id = API_CLIENT_ID
    api_client_secret = API_CLIENT_SECRET
    basic_url = 'https://api.hh.ru/vacancies'
    basic_url_employers = 'https://api.hh.ru/employers'

    def __init__(self, criteries: dict) -> None:
        """Конструктор класса
        :param criteries: Критерии поиска вакансий.
        """
        if criteries != {}:
            self.criteries = criteries
            self.params = self.get_params()
        self.headers = self.get_headers()
        self.params_employers = {'area': 1, 'per_page': 20, 'only_with_vacancies': 'true'}

    def get_headers(self) -> dict:
        """Метод для получения headers для запроса.
        :return: headers для запроса
        """
        headers = {
            'User-Agent': 'api-test-agent'
        }
        return headers

    def get_params(self) -> dict:
        """Метод для получения params для запроса.
        :return: params для запроса
        """
        dict_experience_headhunter = {
            range(0, 1): "noExperience",
            range(1, 3): "between1And3",
            range(3, 6): "between3And6",
            range(6, 100): "moreThan6",
        }
        name_vacancy = self.criteries['name_vacancy']
        experience_vacancy = None
        if self.criteries['experience_vacancy'] is None:
            experience_vacancy = None
        else:
            for key, value in dict_experience_headhunter.items():
                if self.criteries['experience_vacancy'] in key:
                    experience_vacancy = value
                    break

        params_ = {
            'page': 0,
            'per_page': 100,
            'text': name_vacancy,
            'experience': experience_vacancy
        }
        print(params_)

        params = {
            key: value for key, value in params_.items() if value is not None
        }

        return params

    def get_response(self, basic_url: str, headers: dict, params: dict):
        """
        Метод для работы с api HH, запрос.
        :return:
        """
        response = super().get_response(basic_url=basic_url, headers=headers, params=params)
        return response

    @staticmethod
    def format_vacancy(dic_vacancy: dict) -> dict:
        """
        Метод для парсинга вакансий
        """
        vacancy = {
            'id': dic_vacancy['id'],
            'name': dic_vacancy['name'],
            'address': (
                'Не указан' if not dic_vacancy.get('address') else dic_vacancy['address'].get('raw', 'Не указан')),
            'salary': {
                'from': 0 if not dic_vacancy.get('salary') else dic_vacancy['salary'].get('from', 0),
                'to': 0 if not dic_vacancy.get('salary') else dic_vacancy['salary'].get('to', 0),
                'currency': 0 if not dic_vacancy.get('salary') else dic_vacancy['salary'].get('currency', 0),
            },
            'experience': dic_vacancy['experience']['id'],
            'url': dic_vacancy['alternate_url'],
        }
        return vacancy

    def get_vacancies(self, url_vac: str) -> dict:
        """Метод работы и получения данных от API hh по работодателю о вакансиях"""
        try:
            response = requests.get(url_vac, self.params_employers).json()
        except requests.exceptions.RequestException as e:
            print(f"Нет соединения.")
        else:
            return response

    def get_employers(self) -> dict or None:
        """Метод для получения всех вакансий с HeadHunter"""
        try:
            print(
                f"-------------------Ожидайте, происходит получение информации с HH...-------------------")
            response = self.get_response(basic_url=self.basic_url_employers, headers=self.headers, params=self.params_employers)
        except requests.HTTPError:
            print('Ошибка подключения')
            return None
        return response


# a = HeadHunterAPI({'name_vacancy': 'python', 'experience_vacancy': 5, 'top_n_vacancy': 10})
# vacs = a.get_employers()
#
# print(len(vacs))
# for i in vacs:
#     print(i)
