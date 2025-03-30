class Urls:
    URL_MAIN = 'https://qa-scooter.praktikum-services.ru/api/v1/'

    CREATE_COURIER = f'{URL_MAIN}courier'
    LOGIN_COURIER = f'{URL_MAIN}courier/login'
    DELETE_COURIER = f'{URL_MAIN}courier/'

    CREATE_ORDER = f'{URL_MAIN}orders'
    ACCEPT_ORDER = f'{URL_MAIN}orders/accept/'
    GET_ORDER_ID = f'{URL_MAIN}orders/track'
    ORDERS_LIST = f'{URL_MAIN}orders'
