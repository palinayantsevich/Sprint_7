class ResponseMessage:
    SUCCESSFULL_COURIER_CREATION = '{"ok":true}'
    INCOMPLETE_DATA_COURIER_CREATION = 'Недостаточно данных для создания учетной записи'
    EXISTING_LOGIN_COURIER_CREATION = 'Этот логин уже используется. Попробуйте другой.'
    INCOMPLETE_DATA_COURIER_LOGIN = 'Недостаточно данных для входа'
    NOT_FOUND_COURIER_LOGIN = 'Учетная запись не найдена'
    SUCCESSFULL_COURIER_DELETION = '{"ok":true}'
    NOT_FOUND_COURIER_ID = 'Курьера с таким id нет.'
    SUCCESSFULL_ACCEPT_ORDER = '{"ok":true}'
    GET_ORDER_ID_BY_EMPTY_TRACK_NUMBER = 'Недостаточно данных для поиска'
    GET_ORDER_ID_BY_INVALID_TRACK_NUMBER = 'Заказ не найден'
    ACCEPT_ORDER_MISSED_PARAMETER = 'Недостаточно данных для поиска'
    ACCEPT_ORDER_INVALID_ORDER_ID = 'Заказа с таким id не существует'
    ACCEPT_ORDER_INVALID_COURIER_ID = 'Курьера с таким id не существует'
    ACCEPT_ORDER_PROCESSED_ERROR = 'Этот заказ уже в работе'


class ResponseStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409


class CourierData:
    VALID_LOGIN = 'anakin skywalker'
    VALID_PASSWORD = 'empire0101'
    NOT_EXISTING_COURIER_ID = 1


class OrderData:
    ORDER_DATA = {
        'firstName': 'Anakin',
        'lastName': 'Skyoker',
        'address': 'Tatooine, 4-178',
        'metroStation': 'Lenina',
        'phone': '+7 123 456 789',
        'rentTime': 2,
        'deliveryDate': '2025-01-01',
        'comment': 'Please deliver early in the morning',
        'color': []
    }

    COLORS = [['BLACK'], ['GREY'], ['BLACK, GREY'], ['']]

    INVALID_TRACK_NUMBER = 1
    NOT_EXISTING_ORDER_ID = 1
    PROCESSED_ORDER = 434505
