import json
import requests
from config import keys


class ConvertException(Exception):
    pass


class Convertation:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f'Невозможно конвертировать одинаковые валюты {quote}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/fixer/latest?symbols={base_ticker}&base={quote_ticker}"
        payload = {}
        headers = {
            "apikey": "b1Pmc32XuyleqyLASrLbYCRXIbGVc2pW"
        }
        responce = requests.request("GET", url, headers=headers, data=payload)
        r = json.loads(responce.content)
        total_base = r['rates'][f'{base_ticker}']

        return total_base
