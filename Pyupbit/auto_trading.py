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


#######################################################################################################################

access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'

acc_trade_price_24h = 30000000000
append_lists = []
remove_lists = ["KRW-SNT"]

# access_key : 업비트에서 받은 본인의 API Access Key
# secret_key : 업비트에서 받은 본인의 API Secret Key
# server_url : 업비트 서버 주소, 'https://api.upbit.com'

# acc_trade_price_24h : 기준이 되는 거래대금, 해당 거래대금 이하의 상품들은 분석하지 않음 
# append_lists : 개별적으로 추가하고 싶은 코인
# remove_lists : 개별적으로 삭제하고 싶은 코인

#######################################################################################################################

# 전략 구현
# 업비트에 상장되어 있는 모든 코인의 종류를 로딩
market_querystring = {"isDetails": "false"}
market_response = requests.request("GET", server_url + "/v1/market/all", params=market_querystring).json()

coin_lists = []
for i in range(0, len(market_response)):
    coin_lists.append(market_response[i]["market"])
# print(coin_lists)

# 원화로 거래되고 있는 코인들의 리스트를 출력
search = "KRW"
krw_coins = [word for word in coin_lists if search in word]

# 사용자가 조건에 따라 직접 코인을 추가하거나 삭제할 수 있습니다
krw_coins_final = list()
for i in krw_coins:
    time.sleep(0.2)
    if ticker_info(i)[0]['acc_trade_price_24h'] > acc_trade_price_24h:
        krw_coins_final.append(i)
# print(krw_coins_final)

for j in append_lists:
    krw_coins_final.append(j)
# print(krw_coins_final)

for k in remove_lists:
    krw_coins_final.remove(k)
# print(krw_coins_final)

# 자동매매 시작
while True:
    now = datetime.now()
    # print(now.strftime("%Y-%m-%d %H:%M:%S"))
    if now.strftime("%M") == '30' or now.strftime("%M") == '00':  # 매시 정각, 30분 마다 분석 후 매매
        start_time = time.time()
        print("\n", "<<< {} 매매현황 >>>".format(now.strftime("%Y-%m-%d %H:%M:%S")))
        time.sleep(0.5)

        for coin in krw_coins_final:           
            try:
                MA4_querystring = {"market": coin, "count": "5"}
                MA48_querystring = {"market": coin, "count": "49"}
                time.sleep(0.5)

                MA4_response = requests.request("GET", server_url + "/v1/candles/minutes/30", params=MA4_querystring).json()
                MA48_response = requests.request("GET", server_url + "/v1/candles/minutes/30", params=MA48_querystring).json()
                time.sleep(1)

                MA4_now_sum = 0
                MA4_pre_sum = 0
                for i in range(1, len(MA4_response)):
                    MA4_now_sum += MA4_response[-i]["trade_price"]
                    MA4_pre_sum += MA4_response[-i]["opening_price"]

                pre_MA4 = round(MA4_pre_sum / (len(MA4_response) - 1), 2)
                now_MA4 = round(MA4_now_sum / (len(MA4_response) - 1), 2)

                MA48_now_sum = 0
                MA48_pre_sum = 0
                for j in range(1, len(MA48_response)):
                    MA48_now_sum += MA48_response[-j]["trade_price"]
                    MA48_pre_sum += MA48_response[-j]["opening_price"]

                pre_MA48 = round(MA48_pre_sum / (len(MA48_response) - 1), 2)
                now_MA48 = round(MA48_now_sum / (len(MA48_response) - 1), 2)
                # print(pre_MA3)
                # print(pre_MA30)
                # print(now_MA3)
                # print(now_MA30)

                if now_MA4 < now_MA48:  # 현재 차트가 음봉을 띄움
                    if pre_MA4 > pre_MA48:  # 차트의 흐름이 하락장 초입이라고 판단
                        my_wallet = coin_wallet()
                        for i in my_wallet:
                            if coin == f"{i['unit_currency']}-{i['currency']}":  # 내 지갑에 해당 코인이 있음
                                try:
                                    print(f"!!! {coin} 매도 !!!")
                                    ask_market(f"{i['unit_currency']}-{i['currency']}", i['balance'], None)
                                except Exception as e:
                                    print(f"{i['unit_currency']}-{i['currency']} has some trouble : ", e)
                                    pass

                elif now_MA4 > now_MA48:  # 현재 차트가 양봉을 띄움
                    if pre_MA4 < pre_MA48:  # 차트의 흐름이 상승장 초입이라고 판단                           
                        try:
                            print(f"!!! {coin} 매수 !!!")
                            bid_market(coin, None, '50000')
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

        print(f"소요시간(sec) : {round(time.time() - start_time, 2)}")
    else:
        pass
