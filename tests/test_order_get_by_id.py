import allure
import pytest

from data import ResponseMessage as RM, ResponseStatus as RS, OrderData, CourierData
from api.order_api import OrderApi
from helpers.helper_order import HelperOrder


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
