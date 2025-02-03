import datetime
import time
import pyupbit  # wrapper class module 사용.
import math
import pandas as pd
import matplotlib.pyplot as plt

LOCAL_UPBIT_TXT_LOC = "C:/BizPlatform/store_data/upbit.txt"
CURRRENT_FIAT = "KRW-XRP"
BALANCE_RATE  = 0.75

# upbit 객체 생성
def create_upbit_instance():

    f = open(LOCAL_UPBIT_TXT_LOC)
    lines = f.readlines()
    access = lines[0].strip()  # access key '\n'
    secret = lines[1].strip()  # secret key '\n'
    f.close()
    upbit_inst = pyupbit.Upbit(access, secret)  # class instance, object

    return upbit_inst

# 설정된 FIAT
def get_current_setting_fiat():
    return CURRRENT_FIAT;

# 목표가 계산 함수 정의
def calc_target_price():
    try:
        df = pyupbit.get_ohlcv(CURRRENT_FIAT,"day")
        yesterday = df.iloc[-2]
        today     = df.iloc[-1]
        yesterday_range = yesterday['high'] - yesterday['low']
        target = today['open'] + yesterday_range * 0.5
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다")

    except AttributeError:
        print("데이터프레임이 None입니다.")

    return target

# 내 잔고 확인
def get_my_balance(upbit):
#    return int(upbit.get_balance("KRW"))
    balance = upbit.get_balance("KRW")
    balance = math.floor(balance)
    return balance

# 내 평균 매수 금액 확인
def get_my_buy_avg(upbit):
    return upbit.get_avg_buy_price(CURRRENT_FIAT)

# 내 fiat 보유 수량 확인
def get_my_quantity(upbit):
    return upbit.get_balance(CURRRENT_FIAT)

# 현재 fiat 가격 확인
def get_cur_fiat_price():
    return pyupbit.get_current_price(CURRRENT_FIAT)

# 현재 fiat 매수
def buy_fiat(upbit):
    balance = get_my_balance(upbit)

    if balance is None or balance <= 0:
        print("user balance is empty!")
        return -1
    else:
        try:
            upbit.buy_market_order(CURRRENT_FIAT, balance * BALANCE_RATE) # 시장가 전량 매수 안되서 75% 매수 되게 함//
            print("sucess buy market order!")
            return 0
        except :
            print("occur exception for buy fiat!")
            return -2

# 보유 fiat 매도
def sell_fiat(upbit):
    fiat_quantity =  get_my_quantity(upbit)

    if fiat_quantity is None or fiat_quantity <= 0:
        print("user quantity is empty!")
        return -1
    else:
        try:
            upbit.sell_market_order(CURRRENT_FIAT, fiat_quantity)
            print("sucess sell market order!")
            return 0
        except :
            print("occur exception for sell fiat!")
            return -2

# rsi 지표값 얻어 오기
def get_rsi(df, period=14):
    # 전일 대비 변동 평균
    df['change'] = df['close'].diff()

    # 상승한 가격과 하락한 가격
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    # 상승 평균과 하락 평균
    df['avg_up'] = df['up'].ewm(alpha=1 / period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1 / period).mean()

    # 상대강도지수(RSI) 계산
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    rsi = df['rsi']

    return rsi

# check rsi 수치(어제 보다 오늘 높으면 매수 가능)
def available_buy_with_rsi():
    try:
        df = pyupbit.get_ohlcv(CURRRENT_FIAT, "day")
        yesterday_rsi = get_rsi(df, 14).iloc[-2]
        today_rsi = get_rsi(df, 14).iloc[-1]
        print("yesterday rsi:" + str(yesterday_rsi))
        print("today rsi:" + str(today_rsi))
        if yesterday_rsi < today_rsi:
            return True
        else:
            return False
    except :
        print(f"rsi 체크 에러")

    return False

# 최소매도조건에 부합하는지 여부 체크(수수료 감당 0.05%)
def check_available_sell_min(upbit):

     return_val = {}
     return_val["is_available"]   = False
     return_val["cur_fiat_price"]   = 0
     return_val["avg_buy_price"]    = 0
     return_val["total_buy_price"]  = 0
     return_val["total_sell_price"] = 0
     return_val["charge"]   = 0
     return_val["proceeds"] = 0
     return_val["min_get_money"] = 0
     return_val["lose_sell_money"] = 0

     my_quantity    = get_my_quantity(upbit)

     if my_quantity > 0 :
        cur_fiat_price = get_cur_fiat_price()   # 현재 종목 가격
        avg_buy_price  = get_my_buy_avg(upbit)  # 평균 매수 가격
        total_buy_price  = (my_quantity * avg_buy_price) # 총 매수 가격
        total_sell_price = (my_quantity * cur_fiat_price) # 총 매도 가격
        charge   = total_sell_price * 0.0005 # 수수료
        min_get_money  = total_sell_price * 0.005  # 최소 수익기준
        lose_sell_money = (total_buy_price - (total_buy_price * 0.03))    # 손절 기준 (3% 제외금액)
        proceeds = total_sell_price - total_buy_price


        return_val["cur_fiat_price"] = cur_fiat_price
        return_val["avg_buy_price"] = avg_buy_price
        return_val["total_buy_price"] = total_buy_price
        return_val["total_sell_price"] = total_sell_price
        return_val["charge"] = charge
        return_val["proceeds"] = proceeds
        return_val["min_get_money"] = min_get_money
        return_val["lose_sell_money"] = lose_sell_money

        print(f"[CHECK_SELL_INFO]: 종목가격{cur_fiat_price} 매수평균가격:{avg_buy_price} 총 매수금액:{int(total_buy_price)} 총 매도금액:{int(total_sell_price)} 수수료:{int(charge)} 수익금:{int(proceeds)} 순수 수익금:{int(proceeds) - int(charge)} 기준수익금:{int(min_get_money)}")

        if cur_fiat_price > avg_buy_price and proceeds > 0 and proceeds > charge and proceeds > min_get_money:
            return_val["is_available"] = True

     return return_val
