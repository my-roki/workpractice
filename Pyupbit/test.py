# #%%
# import pyupbit

# print(pyupbit.get_tickers())  # 업비트에 상장되어 있는 모든 코인
# # print(pyupbit.get_tickers(fiat="KRW"))  # 업비트에 상장되어 있는 krw 코인
# # print(pyupbit.get_current_price("KRW-BTC"))  # 현재가 출력
# # print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))


# # search = "KRW"
# # krw_coin = [word for word in pyupbit.get_tickers() if search in word]
# # print(krw_coin)

# #%%
# import pyupbit

# btc = pyupbit.get_ohlcv("KRW-BTC", count=5, interval="minute")
# print(btc)


# # %%
# import requests
# import json
# from pprint import pprint
# from datetime import datetime
# import time

# url = "https://api.upbit.com/v1/candles/minutes/30"
# btc3_querystring = {"market":"KRW-FCT2","count":"4"}
# btc30_querystring = {"market":"KRW-FCT2","count":"31"}

# btc3_response = requests.request("GET", url, params=btc3_querystring).json()
# btc30_response = requests.request("GET", url, params=btc30_querystring).json()

# # pprint(btc3_response)
# # print()
# # pprint(btc3_response[0])
# # # pprint(btc_response[-1]["high_price"])
# # # pprint(btc_response[-1]["low_price"])
# # print((btc3_response[-2]["high_price"]+btc3_response[-2]["low_price"])/2)



# while url :
#     now = datetime.now()
#     # print(now.strftime("%Y-%m-%d %H:%M:%S"))
#     if now.strftime("%S") == '30' or now.strftime("%S") == '00':
#         btc3_sum = 0
#         btc3_pre_sum = 0
#         for i in range(0, len(btc3_response)-1):
#             btc3_sum += btc3_response[i]["opening_price"]
#             btc3_pre_sum += btc3_response[-i]["opening_price"]
#         pre_MA3 = round(btc3_pre_sum/(len(btc3_response)-1), 0)
#         now_MA3 = round(btc3_sum/(len(btc3_response)-1), 0)

#         btc30_sum = 0
#         btc30_pre_sum = 0
#         for j in range(0, len(btc30_response)-1):
#             btc30_sum += btc30_response[j]["opening_price"]
#             btc30_pre_sum += btc30_response[-j]["opening_price"]
#         pre_MA30 = round(btc30_pre_sum/(len(btc30_response)-1), 0)
#         now_MA30 = round(btc30_sum/(len(btc30_response)-1), 0)

#         print(pre_MA3)
#         print(pre_MA30)

#         print(now_MA3)
#         print(now_MA30)

#         if now_MA3 < now_MA30 :
#             if pre_MA3 > pre_MA30:
#                 print("매도")
#             elif pre_MA3 < pre_MA30:
#                 print("관망")
#             else:
#                 pass
#         elif now_MA3 > now_MA30:
#             if pre_MA3 < pre_MA30:
#                 print("매수")
#             elif pre_MA3 > pre_MA30:
#                 print("관망")
#             else:
#                 pass
#         else:
#             print("같으면 pass")
#         time.sleep(1)
#     else:
#         pass   

# #%%
# from datetime import datetime
# now = datetime.now()
# if now.strftime("%S") == '30' or now.strftime("%S") == '0':
#     print("가자")
# else:
#     print(now.strftime("%Y-%m-%d %H:%M:%S"))



# # %%
# btc3_sum = 0
# btc3_pre_sum = 0
# for i in range(0, len(btc3_response)-1):
#     btc3_sum += btc3_response[i]["opening_price"]
#     btc3_pre_sum += btc3_response[-i]["opening_price"]
# pre_MA3 = round(btc3_pre_sum/(len(btc3_response)-1), 0)
# now_MA3 = round(btc3_sum/(len(btc3_response)-1), 0)

# print(pre_MA3)
# print(now_MA3)


# btc30_sum = 0
# btc30_pre_sum = 0
# for j in range(0, len(btc30_response)-1):
#     btc30_sum += btc30_response[j]["opening_price"]
#     btc30_pre_sum += btc30_response[-j]["opening_price"]
# pre_MA30 = round(btc30_pre_sum/(len(btc30_response)-1), 0)
# now_MA30 = round(btc30_sum/(len(btc30_response)-1), 0)

# print(pre_MA30)
# print(now_MA30)


# #%%
# from datetime import datetime
# now = datetime.now()
# print(type(now.strftime("%S")))


# #%%
# import schedule
# import time
 
# #특정 함수 정의
# def printhello():
#     print("Hello!")
 
 
# schedule.every(30).seconds.do(printhello)
# # schedule.every(30).seconds.do(printhello)

 
# #실제 실행하게 하는 코드
# while True:
#     schedule.run_pending()
#     time.sleep(30)


# #%%
# import pyupbit
# import requests
# import json
# from pprint import pprint
# from datetime import datetime
# import time


# # print(pyupbit.get_tickers())  # 업비트에 상장되어 있는 모든 코인
# # print(pyupbit.get_tickers(fiat="KRW"))  # 업비트에 상장되어 있는 krw 코인
# # print(pyupbit.get_current_price("KRW-BTC"))  # 현재가 출력
# # print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))

# url = "https://api.upbit.com/v1/candles/minutes/30"

# for list in pyupbit.get_tickers(fiat="KRW"):
#     print(list)

#     querystring = {"market":list,"count":"1"}
#     response = requests.request("GET", url, params=querystring).text
#     print(json.loads(response))



# #%%
# import requests

# market_url = "https://api.upbit.com/v1/market/all"
# candles_url = "https://api.upbit.com/v1/candles/minutes/30"

# market_querystring = {"isDetails":"false"}
# market_response = requests.request("GET", market_url, params=market_querystring).json()

# krw_lists = []
# for i in range(0, len(market_response)):
#     krw_lists.append(market_response[i]["market"])
# # print(krw_lists)

# search = "KRW"
# krw_coin = [word for word in krw_lists if search in word]
# # print(krw_coin)

# cnt = 0
# for list in krw_coin:
#     try:
#         candles_querystring = {"market":list,"count":"1"}
#         time.sleep(0.07)
#         candles_response = requests.request("GET", candles_url, params=candles_querystring).json()
#         print(candles_response)
#         cnt += 1
#     except:
#         pass
# print("--------------")
# print(cnt)
# print("--------------")

# #%%
# # %%
# import requests
# import json
# from pprint import pprint
# from datetime import datetime
# import time


# market_url = "https://api.upbit.com/v1/market/all"
# candles_url = "https://api.upbit.com/v1/candles/minutes/30"

# market_querystring = {"isDetails":"false"}
# market_response = requests.request("GET", market_url, params=market_querystring).json()


# krw_lists = []
# for i in range(0, len(market_response)):
#     krw_lists.append(market_response[i]["market"])
# # print(krw_lists)

# search = "KRW"
# krw_coin = [word for word in krw_lists if search in word]
# # print(krw_coin)

# while True :
#     now = datetime.now()
#     # print(now.strftime("%Y-%m-%d %H:%M:%S"))
#     if now.strftime("%M") == '30' or now.strftime("%M") == '00':
#     # if int(now.strftime("%M")) % 6 != 0 :
#         start_time = time.time()
#         print("\n","<<< {} 매매현황 >>>".format(now.strftime("%Y-%m-%d %H:%M:%S")))
#         for list in krw_coin:
#             try:
#                 MA3_querystring = {"market":list,"count":"4"}
#                 MA30_querystring = {"market":list,"count":"31"}
#                 time.sleep(0.07)
#                 MA3_response = requests.request("GET", candles_url, params=MA3_querystring).json()
#                 MA30_response = requests.request("GET", candles_url, params=MA30_querystring).json()


#                 MA3_sum = 0
#                 MA3_pre_sum = 0
#                 for i in range(0, len(MA3_response)-1):
#                     MA3_sum += MA3_response[i]["trade_price"]
#                     MA3_pre_sum += MA3_response[-i]["trade_price"]
#                 pre_MA3 = round(MA3_pre_sum/(len(MA3_response)-1), 2)
#                 now_MA3 = round(MA3_sum/(len(MA3_response)-1), 2)

#                 MA30_sum = 0
#                 MA30_pre_sum = 0
#                 for j in range(0, len(MA30_response)-1):
#                     MA30_sum += MA30_response[j]["trade_price"]
#                     MA30_pre_sum += MA30_response[-j]["trade_price"]
#                 pre_MA30 = round(MA30_pre_sum/(len(MA30_response)-1), 2)
#                 now_MA30 = round(MA30_sum/(len(MA30_response)-1), 2)

#                 # print(pre_MA3)
#                 # print(pre_MA30)

#                 # print(now_MA3)
#                 # print(now_MA30)

#                 if now_MA3 < now_MA30 :
#                     if pre_MA3 > pre_MA30:
#                         print("{} 매도!!!!!!!!!!!!!!!!".format(list))
#                     elif pre_MA3 < pre_MA30:
#                         # print("{} 관망".format(list))
#                         pass
#                     else:
#                         pass
#                 elif now_MA3 > now_MA30:
#                     if pre_MA3 < pre_MA30:
#                         print("{} 매수!!!!!!!!!!!!!!!".format(list))
#                     elif pre_MA3 > pre_MA30:
#                         # print("{} 관망".format(list))
#                         pass
#                     else:
#                         pass
#                 else:
#                     # print("{} 같아서 pass".format(list))
#                     pass                
#             except:
#                 pass
#         print("소요시간 : {}".format(time.time()-start_time))
#         time.sleep(60)
#     else:
#         pass

#%%
import jwt   # PyJWT 
import uuid

payload = {
    'access_key': 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe')
authorization_token = 'Bearer {}'.format(jwt_token) 

#%%
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers).json()
print(res)


#%%
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']


market = f"KRW-{res[0]['currency']}"
volume = res[0]['balance']


# 매도
try:
    sell_query = {
        'market': market,
        'side': 'ask',
        'volume': volume,
        'price': None,
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
except Exception as e:
    print(f"{market} is not in your wallet...", e)
    pass


# 매수
try:
    buy_query = {
        'market': market,
        'side': 'bid',
        'volume': None,
        'price': 5000,
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
except Exception as e:
    print(f"{market} can't buy...", e)
    pass


#%%
lists = "KRW-SPND"

for i in res:
    if lists == f"KRW-{i['currency']}":
        print(f"{lists} : {i['balance']}")
    else:
        print("없졍!!")


#%%
import requests
r = requests.get(r'http://jsonip.com')
ip= r.json()['ip']
print(ip)


#%%
for i in range(10):
    if i % 2 == 0:
        print(f"{i}는 짝수")


#%%
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



access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

wallte_res = requests.get(server_url + "/v1/accounts", headers=headers).json()


market_querystring = {"isDetails":"false"}
market_response = requests.request("GET", server_url + "/v1/market/all", params=market_querystring).json()

coin_lists = []
for i in range(0, len(market_response)):
    coin_lists.append(market_response[i]["market"])
# print(krw_lists)

search = "KRW"
krw_coins = [word for word in coin_lists if search in word]

# print(krw_coins)
print(wallte_res)


# for coin in krw_coins:
#     for i in wallte_res:
#         if coin == f"KRW-{i['currency']}":
#             ask_market("KRW-XLM", volume, None)


for i in wallte_res:
    if "KRW-XLM" == f"{i['unit_currency']}-{i['currency']}":
        ask_market(f"{i['unit_currency']}-{i['currency']}", i['balance'], None)
        print(f"{i['unit_currency']}-{i['currency']} 매도")
    else:
        print("문제")


#%%
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'
secret_key = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'
server_url = 'https://api.upbit.com'

query = {
    'uuid': '9ca023a5-851b-4fec-9f0a-48cd83c2eaae',
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/order", params=query, headers=headers)

print(res.json())