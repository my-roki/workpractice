import json
import random
import time
from datetime import datetime

import requests

from upbitlib.upbit import Upbit


# 네트워크 ip 찾기
def find_my_ip():
    r = requests.get(r'http://jsonip.com')
    ip = r.json()['ip']
    return ip


def get_MA(time,market,to='',count=1):
    response = upbit.get_candles_per_minutes(time, market, to, count+1)
    opening_MA_sum = 0
    trading_MA_sum = 0
    for i in range(1, len(response)):
        opening_MA_sum += response[-i]["opening_price"]
        trading_MA_sum += response[-i]["trade_price"]          
    MA = {
        'opening_MA' : round(opening_MA_sum / (len(response) - 1), 2),
        'trading_MA' : round(trading_MA_sum / (len(response) - 1), 2)
        }

    return MA


def fix_price(price):
    _unit = {
        10: 0.01,  # 10
        10**1: 0.1,  # 100
        10**2: 1,
        10**3: 5,
        10**4: 10,
        5*10**4: 50,
        10**5: 100,
        10**6: 500,
        2*10**6: 1000
    }

    for p in _unit:
        if price > p:
            price = (price // _unit[p]) * _unit[p]
    return price


def buy(market, budget):
    for retry in range(3):
        ticker = upbit.get_ticker(market)
        last_price = fix_price(ticker[0]['trade_price'] * (1 + SPREAD_GAP))
        amount = round((budget / last_price),2)

        result = upbit.place_order(market, 'bid', amount, last_price)
        if result and result['uuid']:
            for i in range(5):
                order_info = upbit.get_order(result['uuid'])
                if order_info and float(order_info['remaining_volume']) <= 0.0:
                    return
                time.sleep(1)

            upbit.cancel_order(result['uuid'])


def sell(market, amount):
    for retry in range(3):
        ticker = upbit.get_ticker(market)
        if not ticker:
            return

        total_price = float(amount) * float(ticker[0]['trade_price'])
        if total_price < 10000:
            return

        last_price = fix_price(ticker[0]['trade_price'] * (1 - SPREAD_GAP))
        result = upbit.place_order(market, 'ask', amount, last_price)

        if result and result['uuid']:
            for i in range(5):
                order_info = upbit.get_order(result['uuid'])
                if order_info and float(order_info['remaining_volume']) <= 0.0:
                    return
                time.sleep(1)

            upbit.cancel_order(result['uuid'])

#######################################################################################################################

UPBIT_ACESS_KEY = 'NeC5CQaIHC1Jzslk9RXF77R1Q2gJCpFaQJINgxpj'  # 업비트에서 발급 받은 Key 입력
UPBIT_SECRET_KEY = 'q8gCWTxOStFU7N2aK2HGpCcON5LSrQAalWH6EGGe'  # 업비트에서 발급 받은 Secret 입력
SPREAD_GAP = 0.002

acc_trade_price_24h = 25000000000
append_lists = []
remove_lists = ['KRW-BTT', 'KRW-DKA', 'KRW-CHZ', 'KRW-STRAX']

#######################################################################################################################

upbit = Upbit(UPBIT_ACESS_KEY, UPBIT_SECRET_KEY)

if __name__ == '__main__':
    # 업비트에 상장되어 있는 모든 코인의 종류를 로딩
    markets_all = upbit.get_markets()

    coin_lists = []
    for i in range(0, len(markets_all)):
        coin_lists.append(markets_all[i]["market"])
    # print(coin_lists)

    # 원화로 거래되고 있는 코인들의 리스트를 출력
    search = "KRW"
    krw_coins = [word for word in coin_lists if search in word]
    # print(krw_coins)



    print("Auto Trading bot v2 is running")
    # 자동매매 시작
    while True:
        now = datetime.now()
        # print(now.strftime("%Y-%m-%d %H:%M:%S"))
        if int(now.strftime("%H")) % 4 == 1:
            if str(now.strftime("%M")) == "00":
                start_time = time.time()

                krw_coins_final = list()
                for i in krw_coins:
                    time.sleep(0.05)
                    if upbit.get_ticker(i)[0]['acc_trade_price_24h'] > acc_trade_price_24h:
                        krw_coins_final.append(i)
                # print(krw_coins_final)
            
                for j in append_lists:
                    if j not in krw_coins_final:
                        krw_coins_final.append(j)
                # print(krw_coins_final)

                for k in remove_lists:
                    if k in krw_coins_final:
                        krw_coins_final.remove(k)
                # print(krw_coins_final)

                for coin in krw_coins:
                    pre_short_MA = get_MA(240, 'KRW-BTC','',1)['opening_MA']
                    now_short_MA = get_MA(240, 'KRW-BTC','',1)['trading_MA']
                    pre_long_MA = get_MA(240, 'KRW-BTC','',24)['opening_MA']
                    now_long_MA = get_MA(240, 'KRW-BTC','',24)['trading_MA']
                    # print(pre_short_MA)
                    # print(now_short_MA)
                    # print(pre_long_MA)
                    # print(now_long_MA)
                    
                    
                    if now_short_MA < now_long_MA:  # 현재 차트가 음봉을 띄움
                        if pre_short_MA >= pre_long_MA:  # 차트의 흐름이 하락장 초입이라고 판단
                            my_wallet = upbit.get_accounts()
                            for i in my_wallet:
                                if coin == f"{i['unit_currency']}-{i['currency']}":  # 내 지갑에 해당 코인이 있음
                                    try:
                                        print(f"!!! {coin} 매도 !!!")
                                        sell(f"{i['unit_currency']}-{i['currency']}", i['balance'])
                                    except Exception as e:
                                        print(f"{i['unit_currency']}-{i['currency']} has some trouble : ", e)
                                        pass

                    elif now_short_MA >= now_long_MA:  # 현재 차트가 양봉을 띄움
                        if pre_short_MA <= pre_long_MA:  # 차트의 흐름이 상승장 초입이라고 판단
                            for bid_coin in krw_coins_final:  # 사용자가 매수를 원하는 코인 일치 여부 확인
                                if coin == bid_coin:
                                    try:
                                        print(f"!!! {bid_coin} 매수 !!!")
                                        buy(bid_coin,'100000')
                                    except Exception as e:
                                        print(f"{bid_coin} can't buy : ", e)
                                        pass

                print(f"소요시간(sec) : {round(time.time() - start_time, 2)}")
                # time.sleep(60 * 25)


    # # 추세를 araboza
    # for i in krw_coins:
    #     if ticker_info(i)[0]['change'] == 'EVEN':
    #         print(f"{ticker_info(i)[0]['change']} : {ticker_info(i)[0]['market']}")
    #     time.sleep(0.2)
    #
    # for i in krw_coins:
    #     if ticker_info(i)[0]['change'] == 'RISE ':
    #         print(f"{ticker_info(i)[0]['change']} : {ticker_info(i)[0]['market']}")
    #     time.sleep(0.2)


