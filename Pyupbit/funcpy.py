import hashlib
import time
import uuid
import json
from datetime import datetime
from urllib.parse import urlencode

import jwt
import requests


# 네트워크 ip 찾기
def find_my_ip():
    r = requests.get(r'http://jsonip.com')
    ip = r.json()['ip']
    return ip


# 계좌 정보
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


# 마켓에 올라와 있는 코인의 현재 정보
def ticker_info(markets):
    ticker_info_querystring = {"markets": markets}
    ticker_info_response = requests.request("GET", server_url + "/v1/ticker", params=ticker_info_querystring).json()

    return ticker_info_response


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


# 시장가 매수
def bid_market(market, volume, price):
    buy_query = {
        'market': str(market),
        'side': 'bid',
        # 'volume': str(volume),
        'price': str(price),
        'ord_type': 'price',
    }
    buy_query_string = urlencode(buy_query).encode()

    buy_m = hashlib.sha512()
    buy_m.update(buy_query_string)
    buy_query_hash = buy_m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': buy_query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    buy_res = requests.post(server_url + "/v1/orders", params=buy_query, headers=headers)
    return print(json.dumps(buy_res.json(), indent='\t'))
