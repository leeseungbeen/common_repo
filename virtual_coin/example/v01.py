import datetime
import time
import pyupbit  # wrapper class module 사용.


# 목표가 계산 함수 정의
def cal_target(ticker):
    try:
        df = pyupbit.get_ohlcv(ticker,"day")
        yesterday = df.iloc[-2]
        today     = df.iloc[-1]
        yesterday_range = yesterday['high'] - yesterday['low']
        target = today['open'] + yesterday_range * 0.5
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다")

    except AttributeError:
        print("데이터프레임이 None입니다.")

    return target

def get_my_balance():
    return int(upbit.get_balance("KRW"))

def get_cur_fiat_price(param):
    return pyupbit.get_current_price(param)

# upbit 객체 생성
f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()  # access key '\n'
secret = lines[1].strip()  # secret key '\n'
f.close()
upbit = pyupbit.Upbit(access, secret) # class instance, object

#if upbit:
#    print(access + ',' + secret)
first_balance = get_my_balance()
last_balance = first_balance

# 변수 설정
fiat = "KRW-XRP"
today_target = cal_target(fiat)
op_mode = False
hold    = False
is_occur = False
forced_op_true = True

curtick = -1

tmp_fiat_balance = upbit.get_balance(fiat)

if tmp_fiat_balance > 0 :
    hold = True
    op_mode = True
    krw_balance = get_my_balance()
    last_balance = krw_balance
    hold = True
    is_occur = True


# 반복하면서 정보 갱신
while True:
    now = datetime.datetime.now()

    # 매도 시도
    if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59 :
        if op_mode is True and hold is True:
            fiat_balance = upbit.get_balance(fiat)
            upbit.sell_market_order(fiat, fiat_balance)
            last_balance = get_my_balance()
            hold = False
            is_occur = True
            tmp_fiat_balance = fiat_balance

        op_mode = False
        time.sleep(10)


    # 09시 00분 20초 ~ 30초 사이에 목표가 새로 계산
    if forced_op_true or (now.hour == 9 and now.minute == 0 and 20 <= now.second <= 30) :
        today_target = cal_target(fiat)
        forced_op_true = False
        op_mode = True
        last_balance = get_my_balance()

    price = get_cur_fiat_price(fiat)

    # 매초마다 조건을 확인 한 후 매수 시도
    if op_mode is True and price is not None and hold is False and price >= today_target :
        #매수
        krw_balance = get_my_balance()

#        if krw_balance > 1000000 :
#            krw_balance = 1000000

        upbit.buy_market_order(fiat, krw_balance)
        last_balance = krw_balance
        hold = True
        is_occur = True

    # 상태 출력
    if curtick >= (60*10) or curtick < 0 or is_occur:
        print(f"현재시간:{now} 종목:{fiat} 목표가:{today_target} 현재가:{price} 보유상태:{hold} 동작상태:{op_mode} 시작금액:{first_balance} 현재금액:{last_balance} 보유수량:{tmp_fiat_balance}")
        curtick = 0
        is_occur = False

    curtick = curtick + 1

    time.sleep(1)


#while True:     b bbbbbbbbnnnnmmmmnhhhhhhhhhhhhhhhh
#    now = datetime.datetime.now()
#    price = pyupbit.get_current_price("KRW-XRP")
#    print(now,price)
#    time.sleep(1)