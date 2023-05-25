import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ.get("TOKEN")
headers = {'apikey': os.environ.get("apikey")}

keys = {'биткоин': 'BTC',
        'доллар': 'USD',
        'евро': 'EUR',
        'рубль': 'RUB'
        }



