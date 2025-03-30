import requests
import allure
from urls import Urls


class CourierAPI:

    @staticmethod
    @allure.step('Create new courier.')
    def create_courier(login: str, password: str, first_name: str):
        response = requests.post(Urls.CREATE_COURIER,
                                 json={"login": login, "password": password, "firstName": first_name})
        return response

    @staticmethod
    @allure.step('Login courier.')
    def login_courier(login: str, password: str):
        response = requests.post(Urls.LOGIN_COURIER, json={"login": login, "password": password})
        return response

    @staticmethod
    @allure.step('Delete courier.')
    def delete_courier(courier_id: int):
        response = requests.delete(f'{Urls.DELETE_COURIER}{courier_id}')
        return response
