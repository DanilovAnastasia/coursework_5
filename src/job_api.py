from abc import ABC, abstractmethod
import random
import requests
import time


class JobAPI(ABC):
    """
    Абстрактный класс для работы с Api сервиса с вакансиями.
    Данный класс реализует парсинг вакансий и информации о них, с какого-либо источника.
    """

    @abstractmethod
    def get_headers(self) -> None:
        """Абстрактный метод для получения headers для запроса."""
        pass

    @abstractmethod
    def get_params(self) -> None:
        """Абстрактный метод для получения params для запроса"""
        pass

    @staticmethod
    def random_sleep() -> None:
        """Cтатический метод для рандомного сна, между запросами."""
        time.sleep(random.uniform(0.2, 0.6))

    @abstractmethod
    def get_response(self, basic_url: str, headers: dict, params: dict) -> dict or Exception:
        """Абстрактный метод, который отправляет запрос и возвращает ответ о вакансях.
        :param basic_url: url для requests;
        :param headers: headers для requests
        :param params: parameters для requests
        :return: response со списком вакансий, либо ошибка.
        """
        response = requests.get(basic_url, headers=headers, params=params)
        if bool(response):
            json_response = response.json()
            return json_response
        else:
            raise requests.HTTPError('Error. При попытке получить вакансии bool(response)=False')

    # @abstractmethod
    # def get_vacancies(self):
    #     """
    #     Cтатический метод, который использует запрос, получает вакансии и приводит их к нашему виду.
    #     """
    #     pass