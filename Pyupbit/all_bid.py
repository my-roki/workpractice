import hashlib
import uuid
import json
from urllib.parse import urlencode

import jwt
import requests


def coin_wallet():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    wallet_resp = requests.get(server_url + "/v1/accounts", headers=headers).json()

    return wallet_resp


# 시장가 매도
def ask_market(market, volume, price):
    sell_query = {
        'market': str(market),
        'side': 'ask',
        'volume': str(volume),
        # 'price': str(price),
        'ord_type': 'market',
    }
    sell_query_string = urlencode(sell_query).encode()

    sell_m = hashlib.sha512()
    sell_m.update(sell_query_string)
    sell_query_hash = sell_m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': sell_query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    sell_res = requests.post(server_url + "/v1/orders", params=sell_query, headers=headers)
    return print(json.dumps(sell_res.json(), indent='\t'))


access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'

my_wallet = coin_wallet()
# print(my_wallet)

while True:
    for i in my_wallet:
        try:
            print(f"!!! {i['unit_currency']}-{i['currency']} 매도 !!!")
           # ask_market(f"{i['unit_currency']}-{i['currency']}", i['balance'], None)
        except Exception as e:
            print(f"{i['unit_currency']}-{i['currency']} has some trouble : ", e)
            pass
    if len(my_wallet) == 0:
        print("%%% All Sold Out %%%")
        break
