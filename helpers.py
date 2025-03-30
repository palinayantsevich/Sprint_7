import random
import string
import allure

from api.courier_api import CourierAPI

from data import ResponseStatus as RS


class HelperCourier:

    @staticmethod
    @allure.step('Generate test data.')
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    @allure.step('Return courier id.')
    def return_courier_id(login, password):
        courier_id = -1
        response_login_courier = CourierAPI.login_courier(login, password)
        if response_login_courier.status_code == RS.OK:
            courier_id = response_login_courier.json()['id']
        return courier_id
