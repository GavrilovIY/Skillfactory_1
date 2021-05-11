import requests
import json
from config import keys


class ConvertionExseption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):


        if quote == base:
            raise ConvertionExseption(f'Невозможно перевести одинаковаые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExseption(f'Не удалось обработать количество {amount}')
        if quote == 'евро':
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=ce50c7879328421581a05b35583391b9&symbols={base_ticker}')
            total_base = json.loads(r.content)['rates'][base_ticker] * amount
        elif base == 'евро':
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=ce50c7879328421581a05b35583391b9&symbols={quote_ticker}')
            total_base = amount/json.loads(r.content)['rates'][quote_ticker]
        else:
            r = requests.get(
                f'http://api.exchangeratesapi.io/v1/latest?access_key=ce50c7879328421581a05b35583391b9&symbols={base_ticker}')
            first_price = json.loads(r.content)['rates'][base_ticker]
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=ce50c7879328421581a05b35583391b9&symbols={quote_ticker}')
            second_price = json.loads(r.content)['rates'][quote_ticker]
            total_base = first_price/second_price*amount
        return total_base