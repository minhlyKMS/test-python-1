import json
import requests
import unittest
from unittest import mock
from datetime import date
from exchange_rate import API_KEY, ExchangeRate


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.reason = ''
        self.url = ''

    def json(self):
        return self.json_data


# This method will be used by the mock to replace requests.get
def mocked_request_get_returns_response_data(*args, **kwargs):
    if args[0] == f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base=EUR&symbols=USD':
        return MockResponse({"success": True, "timestamp": 1624254543, "base": "EUR", "date":"2021-06-21", "rates": {"USD": 1.186838}}, 200)

    return MockResponse(None, 404)

def mock_request_get_returns_with_500_error_code(*args, **kwargs):
    if args[0] == f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base=EUR&symbols=USD':
        return MockResponse(None, 500)

def connection_error():
    raise requests.exceptions.ConnectionError


class TestExchangeRate(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_request_get_returns_response_data)
    def test_exchange_to_destination_currency_usd_with_success(self, mock_get):
        er = ExchangeRate(base_currency='EUR', amount=2)

        result = json.loads(er.exchange_to_destination_currency('USD'))

        self.assertEqual(result['baseCurrency'], 'EUR')
        self.assertEqual(result['amount'], 2)
        self.assertEqual(result['exchangeRateDate'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNotNone(result['exchangeValues'])

    @mock.patch('requests.get', side_effect=mock_request_get_returns_with_500_error_code)
    def test_exchange_to_destination_currency_with_500_error_code(self, mock_get):
        er = ExchangeRate(base_currency='EUR', amount=2)
        with self.assertRaises(requests.exceptions.HTTPError):
            er.exchange_to_destination_currency('USD')


if __name__ == '__main__':
    unittest.main()