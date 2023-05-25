import json
import requests
from config import keys, headers

class ConvertionException(Exception):
    pass


class СurrencyConverter:
    @staticmethod
    def get_price(quote=str, base=str, amount=str):
        if quote == base:
            raise ConvertionException('Невозможно конвертировать одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} не найдена')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта {base} не найдена')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}", headers=headers)

        total_base = json.loads(r.content)
        rate = round(total_base['info']['quote'], 3)
        total_base = round(total_base['result'], 3)

        return total_base, rate


