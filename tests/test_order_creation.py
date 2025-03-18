import json
import allure
import pytest

from data import ResponseStatus as RS, OrderData
from api.order_api import OrderApi


class TestOrderCreation:

    @allure.title(
        'Verify that the order is created successfully with different combination of colors.')
    @allure.description(
        'Verify that 201 code is returned for POST request with different colors.')
    @pytest.mark.parametrize('colors', OrderData.COLORS)
    def test_create_order_different_colors_order_created(self, colors):
        order_data_dict = OrderData.ORDER_DATA
        order_data_dict['color'] = colors
        order_data_json = json.dumps(order_data_dict)
        response = OrderApi.create_order(order_data_json)
        assert response.status_code == RS.CREATED and response.json()['track'] > 0
