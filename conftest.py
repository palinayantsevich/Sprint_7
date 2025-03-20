import pytest
import allure
import json

from api.courier_api import CourierAPI
from api.order_api import OrderApi
from data import OrderData, ResponseStatus as RS
from helpers import HelperCourier


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
def delete_courier():
    courier_id = []
    yield courier_id
    with allure.step('Delete courier.'):
        CourierAPI.delete_courier(*courier_id)


@pytest.fixture(scope='function')
@allure.step('Create and return courier id.')
def create_courier_and_return_courier_id(generate_courier_data):
    CourierAPI.create_courier(generate_courier_data['login'], generate_courier_data['password'],
                              generate_courier_data['firstName'])
    courier_id = HelperCourier.return_courier_id(generate_courier_data['login'], generate_courier_data['password'])
    return courier_id


@pytest.fixture(scope='function')
@allure.step('Get order track number.')
def create_order_and_return_order_track_number():
    track_number = -1
    order_data = json.dumps(OrderData.ORDER_DATA)
    response_create_order = OrderApi.create_order(order_data)
    if response_create_order.status_code == RS.CREATED:
        track_number = response_create_order.json()['track']
    return track_number


@pytest.fixture(scope='function')
@allure.step('Get order id.')
def create_order_and_return_order_id():
    order_id = -1
    track_number = -1
    order_data = json.dumps(OrderData.ORDER_DATA)
    response_create_order = OrderApi.create_order(order_data)
    if response_create_order.status_code == RS.CREATED:
        track_number = response_create_order.json()['track']
    response = OrderApi.get_order_id(track_number)
    if response.status_code == RS.OK:
        order_id = response.json()['order']['id']
    return order_id
