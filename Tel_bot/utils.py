import requests
import json
from collections import defaultdict
from config import keys


class ConvertionExseption(Exception):
    pass


class UserInfo:
    def __init__(self):
        self.f = 'RUB'
        self.t = 'USD'


class UserDB:
    def __init__(self):
        self.db = defaultdict(UserInfo)

    def change_from(self, user_id, val):
        self.db[user_id].f = val

    def change_to(self, user_id, val):
        self.db[user_id].t = val

    def get_pair(self,user_id):
        user = self.db[user_id]
        return user.f, user.t


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):


        if quote == base:
            raise ConvertionExseption(f'Невозможно перевести одинаковаые валюты {base}.')
        quote_ticker = quote
        base_ticker = base

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