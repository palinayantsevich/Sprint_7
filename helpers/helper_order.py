import json

from api.order_api import OrderApi
from data import ResponseStatus as RS, OrderData


class HelperOrder:

    @staticmethod
    def get_order_track_number():
        track_number = -1
        order_data = json.dumps(OrderData.ORDER_DATA)
        response_create_order = OrderApi.create_order(order_data)
        if response_create_order.status_code == RS.CREATED:
            track_number = response_create_order.json()['track']
        return track_number

    @staticmethod
    def get_order_id():
        order_id = -1
        track_number = HelperOrder.get_order_track_number()
        response = OrderApi.get_order_id(track_number)
        if response.status_code == RS.OK:
            order_id = response.json()['order']['id']
        return order_id

    @staticmethod
    def generate_error_message_for_get_order_list_with_invalid_courier_id(courier_id):
        return f'Курьер с идентификатором {courier_id} не найден'
