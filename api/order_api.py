from urls import Urls
import requests
import allure


class OrderApi:

    @staticmethod
    @allure.step('Create new order.')
    def create_order(order_data):
        headers = {"Content-type": "application/json"}
        response = requests.post(Urls.CREATE_ORDER, data=order_data, headers=headers)
        return response

    @staticmethod
    @allure.step('Accept order.')
    def accept_order(order_id: int, courier_id=int):
        response = requests.put(f'{Urls.ACCEPT_ORDER}{order_id}', params={'courierId': courier_id})
        return response

    @staticmethod
    @allure.step('Accept order: order id is missed.')
    def accept_order_url_missed_order_id(courier_id=int):
        response = requests.put(f'{Urls.ACCEPT_ORDER}{courier_id}')
        return response

    @staticmethod
    @allure.step('Get order id.')
    def get_order_id(track_number: int):
        response = requests.get(Urls.GET_ORDER_ID, params={'t': track_number})
        return response

    @staticmethod
    @allure.step('Get order list: all orders.')
    def get_orders_list_no_parameters():
        response = requests.get(Urls.ORDERS_LIST)
        return response

    @staticmethod
    @allure.step('Get order list by courier id.')
    def get_orders_list_by_courier_id(courier_id):
        response = requests.get(Urls.ORDERS_LIST, params={'courierId': courier_id})
        return response
