import allure
import pytest

from data import ResponseStatus as RS, ResponseMessage as RM, CourierData
from api.order_api import OrderApi
from helpers.helper_courier import HelperCourier
from helpers.helper_order import HelperOrder


class TestOrderList:
    @allure.title(
        'Verify that the list of orders is returned if passing no parameters.')
    @allure.description(
        'Verify that 200 code is returned for GET request.')
    def test_get_order_list_all_orders_returned_successfully(self):
        response = OrderApi.get_orders_list_no_parameters()
        assert response.status_code == RS.OK and len(response.json()['orders']) > 0

    @allure.title(
        'Verify that the list of orders is returned if passing valid courier id.')
    @allure.description(
        'Verify that 200 code is returned for GET request with valid courier id.')
    def test_get_order_list_by_courier_id_returned_successfully(self, create_courier_and_return_courier_id):
        courier_id = create_courier_and_return_courier_id
        order_id = HelperOrder.get_order_id()
        response_accept_order = OrderApi.accept_order(order_id, courier_id)
        response = OrderApi.get_orders_list_by_courier_id(courier_id)
        assert response.status_code == RS.OK and (
                courier_id == response.json()['orders'][0]['courierId'] and order_id ==
                response.json()['orders'][0]['id'])
        HelperCourier.delete_courier(courier_id)

    @allure.title(
        'Verify that the list of orders is not returned if passing invalid courier id.')
    @allure.description(
        'Verify that 404 code is returned for GET request with invalid courier id.')
    def test_get_order_list_by_invalid_courier_id_not_returned(self):
        response = OrderApi.get_orders_list_by_courier_id(CourierData.NOT_EXISTING_COURIER_ID)
        assert response.status_code == RS.NOT_FOUND and response.json()[
            'message'] == RM.GET_LIST_OF_ORDERS_INVALID_COURIER_ID
