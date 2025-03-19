import json
import allure

from api.order_api import OrderApi
from data import ResponseStatus as RS, OrderData


class HelperOrder:

    @staticmethod
    @allure.step('Get order track number.')
    def get_order_track_number():
        track_number = -1
        order_data = json.dumps(OrderData.ORDER_DATA)
        response_create_order = OrderApi.create_order(order_data)
        if response_create_order.status_code == RS.CREATED:
            track_number = response_create_order.json()['track']
        return track_number

    @staticmethod
    @allure.step('Get order id.')
    def get_order_id():
        order_id = -1
        track_number = HelperOrder.get_order_track_number()
        response = OrderApi.get_order_id(track_number)
        if response.status_code == RS.OK:
            order_id = response.json()['order']['id']
        return order_id
