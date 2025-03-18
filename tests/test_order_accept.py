import allure
import pytest

from data import ResponseMessage as RM, ResponseStatus as RS, OrderData, CourierData
from api.order_api import OrderApi
from helpers.helper_courier import HelperCourier
from helpers.helper_order import HelperOrder


class TestOrderAccept:

    @allure.title(
        'Verify that the order is accepted successfully if passing valid order and courier id.')
    @allure.description(
        'Verify that 200 code is returned for PUT request with valid order and courier id.')
    def test_accept_order_accepted_successfully(self, create_courier_and_return_courier_id):
        order_id = HelperOrder.get_order_id()
        response = OrderApi.accept_order(order_id, create_courier_and_return_courier_id)
        assert response.status_code == RS.OK and response.text == RM.SUCCESSFULL_ACCEPT_ORDER
        HelperCourier.delete_courier(create_courier_and_return_courier_id)

    @allure.title(
        'Verify that the order is not accepted if courier id value is not passed.')
    @allure.description(
        'Verify that 400 code is returned for PUT request with empty value for courier id.')
    def test_accept_order_no_courier_id_not_accepted(self):
        courier_id = ''
        order_id = HelperOrder.get_order_id()
        response = OrderApi.accept_order(order_id, courier_id)
        assert response.status_code == RS.BAD_REQUEST and response.json()['message'] == RM.ACCEPT_ORDER_MISSED_PARAMETER

    @allure.title(
        'Verify that the order is not accepted if order id is not passed.')
    @allure.description(
        'Verify that 400 code is returned for PUT request if order id is not passed.')
    def test_accept_order_no_order_id_not_accepted(self, create_courier_and_return_courier_id):
        response = OrderApi.accept_order_url_missed_order_id(create_courier_and_return_courier_id)
        assert response.status_code == RS.BAD_REQUEST and response.json()['message'] == RM.ACCEPT_ORDER_MISSED_PARAMETER
        HelperCourier.delete_courier(create_courier_and_return_courier_id)

    @allure.title(
        'Verify that the order is not accepted if passing invalid order id.')
    @allure.description(
        'Verify that 404 code is returned for PUT request if order id is invalid.')
    def test_accept_order_not_existing_order_id_not_accepted(self, create_courier_and_return_courier_id):
        response = OrderApi.accept_order(OrderData.NOT_EXISTING_ORDER_ID, create_courier_and_return_courier_id)
        assert response.status_code == RS.NOT_FOUND and response.json()['message'] == RM.ACCEPT_ORDER_INVALID_ORDER_ID
        HelperCourier.delete_courier(create_courier_and_return_courier_id)

    @allure.title(
        'Verify that the order is not accepted if passing invalid courier id.')
    @allure.description(
        'Verify that 404 code is returned for PUT request if courier id is invalid.')
    def test_accept_order_not_existing_courier_id_not_accepted(self):
        order_id = HelperOrder.get_order_id()
        response = OrderApi.accept_order(order_id, CourierData.NOT_EXISTING_COURIER_ID)
        assert response.status_code == RS.NOT_FOUND and response.json()['message'] == RM.ACCEPT_ORDER_INVALID_COURIER_ID

    @allure.title(
        'Verify that the order is not accepted if passing already processed order id.')
    @allure.description(
        'Verify that 404 code is returned for PUT request if passing already processed order id.')
    def test_accept_order_processed_order_not_accepted(self, create_courier_and_return_courier_id):
        response = OrderApi.accept_order(OrderData.PROCESSED_ORDER, create_courier_and_return_courier_id)
        assert response.status_code == RS.CONFLICT and response.json()['message'] == RM.ACCEPT_ORDER_PROCESSED_ERROR
        HelperCourier.delete_courier(create_courier_and_return_courier_id)
