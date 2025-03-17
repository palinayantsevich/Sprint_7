import pytest
import allure

from data import ResponseMessage as RM, ResponseStatus as RS, CourierData
from helpers.helper_courier import HelperCourier
from api.courier_api import CourierAPI


class TestCourierCreation:
    @allure.title('Verify that the courier is created successfully if all the fields are passed.')
    @allure.description(
        'Verify that 201 code is returned for POST request for courier creation if passing valid login, password and first name fields.')
    def test_create_courier_all_parameters_created_successfully(self, generate_courier_data):
        response = CourierAPI.create_courier(generate_courier_data['login'], generate_courier_data['password'],
                                             generate_courier_data['firstName'])
        courier_id = HelperCourier.return_courier_id(generate_courier_data['login'], generate_courier_data['password'])
        assert response.status_code == RS.CREATED and response.text == RM.SUCCESSFULL_COURIER_CREATION
        HelperCourier.delete_courier(courier_id)

    @allure.title('Verify that the courier is created successfully if all the mandatory fields are passed.')
    @allure.description(
        'Verify that 201 code is returned for POST request for courier creation if passing valid login and password.')
    def test_create_courier_no_first_name_created_successfully(self, generate_courier_data):
        first_name = ''
        response = CourierAPI.create_courier(generate_courier_data['login'], generate_courier_data['password'],
                                             first_name)
        courier_id = HelperCourier.return_courier_id(generate_courier_data['login'], generate_courier_data['password'])
        assert response.status_code == RS.CREATED and response.text == RM.SUCCESSFULL_COURIER_CREATION
        HelperCourier.delete_courier(courier_id)

    @allure.title(
        'Verify that the courier is not created successfully if any of the the mandatory field is missed in the request.')
    @allure.description(
        'Verify that 400 code is returned for POST request for courier creation if login or password (or both) are missed in the request.')
    @pytest.mark.parametrize(
        'login,password,first_name',
        [
            ['', HelperCourier.generate_random_string(10), ''],
            [HelperCourier.generate_random_string(10), '', ''],
            ['', '', ''],
            ['', '', HelperCourier.generate_random_string(10)]
        ]
    )
    def test_create_courier_missed_mandatory_parameter_not_created(self, login, password, first_name):
        response = CourierAPI.create_courier(login, password, first_name)
        assert response.status_code == RS.BAD_REQUEST and response.json()[
            'message'] == RM.INCOMPLETE_DATA_COURIER_CREATION

    @allure.title(
        'Verify that the courier is not created successfully if trying to create a courier with the same login.')
    @allure.description(
        'Verify that 409 code is returned for POST request for courier creation with the existing login.')
    def test_create_courier_existing_login_not_created(self, create_and_delete_courier, generate_courier_data):
        response_courier_created_second_time = CourierAPI.create_courier(generate_courier_data['login'],
                                                                         generate_courier_data['password'],
                                                                         generate_courier_data['firstName'])
        assert response_courier_created_second_time.status_code == RS.CONFLICT and \
               response_courier_created_second_time.json()['message'] == RM.EXISTING_LOGIN_COURIER_CREATION


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


class TestCourierDeletion:

    @allure.title(
        'Verify that the courier is deleted successfully if passing valid courier id in the request.')
    @allure.description(
        'Verify that 200 code is returned for DELETE request with valid courier id.')
    def test_delete_courier_deleted_successfully(self, create_courier_and_return_courier_id):
        response_delete_courier = CourierAPI.delete_courier(create_courier_and_return_courier_id)
        assert response_delete_courier.status_code == RS.OK and response_delete_courier.text == RM.SUCCESSFULL_COURIER_DELETION

    @allure.title(
        'Verify that the courier is not deleted  if passing invalid courier id in the request.')
    @allure.description(
        'Verify that 404 code is returned for DELETE request with invalid courier id.')
    def test_delete_courier_not_existing_id_not_deleted(self):
        response = CourierAPI.delete_courier(CourierData.NOT_EXISTING_COURIER_ID)
        assert response.status_code == RS.NOT_FOUND and response.json()['message'] == RM.NOT_FOUND_COURIER_ID
