import pytest
import allure

from data import ResponseMessage as RM, ResponseStatus as RS, CourierData
from helpers.helper_courier import HelperCourier
from api.courier_api import CourierAPI


class TestCourierLogin:

    @allure.title(
        'Verify that the courier is logged-in successfully if passing valid login and password in the request.')
    @allure.description(
        'Verify that 200 code is returned for POST request for courier login with valid login and password.')
    def test_login_courier_all_fields_logged_in(self, create_and_delete_courier, generate_courier_data):
        response = CourierAPI.login_courier(generate_courier_data['login'], generate_courier_data['password'])
        assert response.status_code == RS.OK and response.json()['id'] > 0

    @allure.title(
        'Verify that the courier is not logged-in if login or password are missed in the request.')
    @allure.description(
        'Verify that 400 code is returned for POST request for courier login with missed login or password (or both).')
    @pytest.mark.parametrize(
        'login,password',
        [
            ['', CourierData.VALID_PASSWORD],
            [CourierData.VALID_LOGIN, ''],
            ['', '']
        ]
    )
    def test_login_courier_missed_mandatory_parameter_not_logged_in(self, login, password):
        response = CourierAPI.login_courier(login, password)
        assert response.status_code == RS.BAD_REQUEST and response.json()['message'] == RM.INCOMPLETE_DATA_COURIER_LOGIN

    @allure.title(
        'Verify that the courier is not logged-in if passing invalid login or password.')
    @allure.description(
        'Verify that 404 code is returned for POST request for courier login with invalid login or password (or both).')
    @pytest.mark.parametrize(
        'login,password',
        [
            [HelperCourier.generate_random_string(10), CourierData.VALID_PASSWORD],
            [CourierData.VALID_LOGIN, HelperCourier.generate_random_string(10)],
            [HelperCourier.generate_random_string(10), HelperCourier.generate_random_string(10)]
        ]
    )
    def test_login_courier_invalid_mandatory_parameter_not_logged_in(self, login, password):
        response = CourierAPI.login_courier(login, password)
        assert response.status_code == RS.NOT_FOUND and response.json()['message'] == RM.NOT_FOUND_COURIER_LOGIN
