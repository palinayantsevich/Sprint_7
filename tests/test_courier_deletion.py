import pytest
import allure

from data import ResponseMessage as RM, ResponseStatus as RS, CourierData
from api.courier_api import CourierAPI


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
