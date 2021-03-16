import requests
import json
from pprint import pprint
from datetime import datetime
import time
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode


def find_my_ip():
    r = requests.get(r'http://jsonip.com')
    ip= r.json()['ip']
    return ip


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
    return sell_res.json()


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
    return buy_res.json()



access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'


# 계좌 정보
payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

wallte_res = requests.get(server_url + "/v1/accounts", headers=headers).json()


# 전략 구현
market_querystring = {"isDetails":"false"}
market_response = requests.request("GET", server_url + "/v1/market/all", params=market_querystring).json()

coin_lists = []
for i in range(0, len(market_response)):
    coin_lists.append(market_response[i]["market"])
# print(krw_lists)

search = "KRW"
krw_coins = [word for word in coin_lists if search in word]
# print(krw_coin)

while True :
    now = datetime.now()
    # print(now.strftime("%Y-%m-%d %H:%M:%S"))
    if now.strftime("%M") == '35' or now.strftime("%M") == '05':
        start_time = time.time()
        print("\n","<<< {} 매매현황 >>>".format(now.strftime("%Y-%m-%d %H:%M:%S")))

        for coin in krw_coins:
            try:
                MA3_querystring = {"market":coin,"count":"4"}
                MA30_querystring = {"market":coin,"count":"31"}
                time.sleep(1)

                MA3_response = requests.request("GET", server_url + "/v1/candles/minutes/30", params=MA3_querystring).json()
                MA30_response = requests.request("GET", server_url + "/v1/candles/minutes/30", params=MA30_querystring).json()
                time.sleep(1)

                MA3_sum = 0
                MA3_pre_sum = 0
                for i in range(0, len(MA3_response)-1):
                    MA3_sum += MA3_response[i]["trade_price"]
                    MA3_pre_sum += MA3_response[-i]["trade_price"]
                pre_MA3 = round(MA3_pre_sum/(len(MA3_response)-1), 2)
                now_MA3 = round(MA3_sum/(len(MA3_response)-1), 2)

                MA30_sum = 0
                MA30_pre_sum = 0
                for j in range(0, len(MA30_response)-1):
                    MA30_sum += MA30_response[j]["trade_price"]
                    MA30_pre_sum += MA30_response[-j]["trade_price"]
                pre_MA30 = round(MA30_pre_sum/(len(MA30_response)-1), 2)
                now_MA30 = round(MA30_sum/(len(MA30_response)-1), 2)
                time.sleep(1)
                # print(pre_MA3)
                # print(pre_MA30)
                # print(now_MA3)
                # print(now_MA30)
                
                if now_MA3 < now_MA30 :
                    if pre_MA3 > pre_MA30:
                        print(f"        !!! {coin} 매도 !!!")
                        for i in wallte_res:
                            if coin == f"{i['unit_currency']}-{i['currency']}":
                                try:
                                    ask_market(f"{i['unit_currency']}-{i['currency']}", i['balance'], None)
                                except Exception as e:
                                    print(f"{i['unit_currency']}-{i['currency']} has some trouble : ", e)
                                    pass

                elif now_MA3 > now_MA30:
                    if pre_MA3 < pre_MA30:
                        print(f"        !!! {coin} 매수 !!!")
                        try:
                            bid_market(coin, None, '5000')
                        except Exception as e:
                            print(f"{coin} can't buy : ", e)
                            pass

                else:
                    # print("{} 같아서 pass".format(coin))
                    pass                
            except Exception as e:
                print(f"{coin} has problem in the trading strategy : ", e)
                pass
            time.sleep(0.5)   

        print("소요시간 : {}".format(time.time()-start_time))
        time.sleep(60)
    else:
        pass 
