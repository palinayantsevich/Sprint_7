import pytest
import allure

from api.courier_api import CourierAPI
from helpers.helper_courier import HelperCourier


@pytest.fixture(scope='function')
@allure.step('Generate courier data.')
def generate_courier_data():
    login = HelperCourier.generate_random_string(10)
    password = HelperCourier.generate_random_string(10)
    first_name = HelperCourier.generate_random_string(10)

    payload = {
        'login': login,
        'password': password,
        'firstName': first_name
    }
    return payload


@pytest.fixture(scope='function')
def create_and_delete_courier(generate_courier_data):
    with allure.step('Create new courier.'):
        create_courier = CourierAPI.create_courier(generate_courier_data['login'], generate_courier_data['password'],
                                                   generate_courier_data['firstName'])
    courier_id = HelperCourier.return_courier_id(generate_courier_data['login'], generate_courier_data['password'])
    yield create_courier
    with allure.step('Delete courier.'):
        CourierAPI.delete_courier(courier_id)


@pytest.fixture(scope='function')
@allure.step('Create and return courier id.')
def create_courier_and_return_courier_id(generate_courier_data):
    CourierAPI.create_courier(generate_courier_data['login'], generate_courier_data['password'],
                              generate_courier_data['firstName'])
    courier_id = HelperCourier.return_courier_id(generate_courier_data['login'], generate_courier_data['password'])
    return courier_id
