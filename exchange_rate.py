import json
import requests
from datetime import date

API_KEY = '59e3dbfa627ad4a4d6bcab72936b6ed6'
AVAILABLE_CURRENCIES = ['USD', 'EUR', 'CAD', 'JPY']


class ExchangeRate:
    def __init__(self, base_currency='', amount=0):
        self.base_currency = base_currency
        self.amount = amount
        self.realtime_url = 'http://api.exchangeratesapi.io/v1'

    def setup_amount_and_base_currency(self, base_currency='', amount=0):
        self.base_currency = base_currency
        self.amount = amount

    def exchange_to_destination_currency(self, des_currency=''):
        try:
            if des_currency:
                exchange_url = f'{self.realtime_url}/latest?access_key={API_KEY}&base={self.base_currency}&symbols={des_currency}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'amount': self.amount,
                        'exchangeRateDate': response_result['date'],
                        'exchangeValues': {
                            des_currency: self.amount * response_result['rates'][des_currency]
                        }
                    })
                else:
                    response.raise_for_status()
            else:
                other_currencies = [currency for currency in AVAILABLE_CURRENCIES if currency != self.base_currency]
                exchange_url = f'{self.realtime_url}/latest?access_key={API_KEY}&base={self.base_currency}&symbols={",".join(other_currencies)}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'amount': self.amount,
                        'exchangeRateDate': response_result['date'],
                        'exchangeValues': [{
                            picked_currency: self.amount * response_result['rates'][picked_currency]
                        } for picked_currency in other_currencies]
                    })
                else:
                    response.raise_for_status()
        except requests.exceptions.HTTPError as he:
            print(he)
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except requests.exceptions.Timeout as t:
            print(t)
        except requests.exceptions.RequestException as re:
            print(re)

    def check_exchange_rate(self, day='', des_currency=''):
        specific_day = day if day else date.today().strftime('%Y-%m-%d')
        try:
            if des_currency:
                exchange_url = f'{self.realtime_url}/{specific_day}?access_key={API_KEY}&base={self.base_currency}&symbols={des_currency}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'exchangeRateDate': response_result['date'],
                        'rates': {
                            des_currency: response_result['rates'][des_currency]
                        }
                    })
                else:
                    response.raise_for_status()
            else:
                other_currencies = [currency for currency in AVAILABLE_CURRENCIES if currency != self.base_currency]
                exchange_url = f'{self.realtime_url}/{specific_day}?access_key={API_KEY}&base={self.base_currency}&symbols={",".join(other_currencies)}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'exchangeRateDate': response_result['date'],
                        'rates': [{
                            picked_currency: response_result['rates'][picked_currency]
                        } for picked_currency in other_currencies]
                    })
                else:
                    response.raise_for_status()
        except requests.exceptions.HTTPError as he:
            print(he)
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except requests.exceptions.Timeout as t:
            print(t)
        except requests.exceptions.RequestException as re:
            print(re)


er = ExchangeRate(base_currency='EUR', amount=2)
print('Destination currency is USD:')
print(er.exchange_to_destination_currency('USD'))
print('Destination currency is empty:')
print(er.exchange_to_destination_currency())
print('Exchange rate at 2021-06-01 of CAD:')
print(er.check_exchange_rate(day='2021-06-01', des_currency='CAD'))
print('Exchange rates at 2021-01-01:')
print(er.check_exchange_rate(day='2021-01-01'))
