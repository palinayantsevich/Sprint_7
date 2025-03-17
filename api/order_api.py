from urls import Urls
import requests


class OrderApi:

    @staticmethod
    def create_order(order_data):
        headers = {"Content-type": "application/json"}
        response = requests.post(Urls.CREATE_ORDER, data=order_data, headers=headers)
        return response

    @staticmethod
    def accept_order(order_id: int, courier_id=int):
        response = requests.put(f'{Urls.ACCEPT_ORDER}{order_id}', params={'courierId': courier_id})
        return response

    @staticmethod
    def accept_order_url_missed_order_id(courier_id=int):
        response = requests.put(f'{Urls.ACCEPT_ORDER}{courier_id}')
        return response

    @staticmethod
    def get_order_id(track_number: int):
        response = requests.get(Urls.GET_ORDER_ID, params={'t': track_number})
        return response

    @staticmethod
    def get_orders_list_no_parameters():
        response = requests.get(Urls.ORDERS_LIST)
        return response

    @staticmethod
    def get_orders_list_by_courier_id(courier_id):
        response = requests.get(Urls.ORDERS_LIST, params={'courierId': courier_id})
        return response
