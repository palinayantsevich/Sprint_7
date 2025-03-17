import json
import allure

import pytest

from data import ResponseMessage as RM, ResponseStatus as RS, OrderData, CourierData
from api.order_api import OrderApi
from helpers.helper_courier import HelperCourier
from helpers.helper_order import HelperOrder


class TestOrderCreation:

    @allure.title(
        'Verify that the order is created successfully with different combination of colors.')
    @allure.description(
        'Verify that 201 code is returned for POST request with different colors.')
    @pytest.mark.parametrize('colors', OrderData.COLORS)
    def test_create_order_different_colors_order_created(self, colors):
        order_data_dict = OrderData.ORDER_DATA
        order_data_dict['color'] = colors
        order_data_json = json.dumps(order_data_dict)
        print(order_data_json)
        response = OrderApi.create_order(order_data_json)
        print(response.json()['track'])
        assert response.status_code == RS.CREATED and response.json()['track'] > 0


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


class TestOrderGetByID:
    @allure.title(
        'Verify that the order id is returned if passing valid track number.')
    @allure.description(
        'Verify that 200 code is returned for GET request if passing valid track number.')
    def test_get_order_id_by_track_number_returned_successfully(self):
        track_number = HelperOrder.get_order_track_number()
        response = OrderApi.get_order_id(track_number)
        assert response.status_code == RS.OK and response.json()['order']['id'] > 0

    @allure.title(
        'Verify that the order id is not returned if passing empty value track number.')
    @allure.description(
        'Verify that 400 code is returned for GET request if passing empty track number value.')
    def test_get_order_id_by_empty_track_number_not_returned(self):
        track_number = ''
        response = OrderApi.get_order_id(track_number)
        assert response.status_code == RS.BAD_REQUEST and response.json()[
            'message'] == RM.GET_ORDER_ID_BY_EMPTY_TRACK_NUMBER

    @allure.title(
        'Verify that the order id is not returned if passing invalid track number.')
    @allure.description(
        'Verify that 404 code is returned for GET request if passing invalid track number.')
    def test_get_order_id_by_invalid_track_number_not_returned(self):
        response = OrderApi.get_order_id(OrderData.INVALID_TRACK_NUMBER)
        assert response.status_code == RS.NOT_FOUND and response.json()[
            'message'] == RM.GET_ORDER_ID_BY_INVALID_TRACK_NUMBER


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
        print(courier_id)
        assert response.status_code == RS.OK and (
                courier_id == response.json()['orders'][0]['courierId'] and order_id ==
                response.json()['orders'][0]['id'])
        HelperCourier.delete_courier(courier_id)

    @allure.title(
        'Verify that the list of orders is not returned if passing invalid courier id.')
    @allure.description(
        'Verify that 404 code is not returned for GET request with invalid courier id.')
    def test_get_order_list_by_invalid_courier_id_not_returned(self):
        response = OrderApi.get_orders_list_by_courier_id(CourierData.NOT_EXISTING_COURIER_ID)
        assert response.status_code == RS.NOT_FOUND and response.json()[
            'message'] == HelperOrder.generate_error_message_for_get_order_list_with_invalid_courier_id(
            CourierData.NOT_EXISTING_COURIER_ID)
