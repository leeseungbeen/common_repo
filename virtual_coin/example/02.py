import pyupbit  # wrapper class module 사용.
import pandas as pd

# 1. 종목 불러오기
# tickers = pyupbit.get_tickers(fiat="KRW") #fiat에 해당하는 중목 목록 얻어오기 . KRW, BTC, USDT

# print(tickers)
# print(len(tickers))


# 2. 세세캔들 1분봉 조회. open, high, low, close, volume
# df = pyupbit.get_ohlcv("KRW-BTC","minute1") # data frame 형태, 시계열 데이터.
# print(df)

# 3. 세세캔들 week 조회. open, high, low, close, volume
#df = pyupbit.get_ohlcv("KRW-BTC","week") # data frame 형태, 시계열 데이터.
#print(df)

# 4. 세세캔들 일봉 조회. open, high, low, close, volume
#df = pyupbit.get_ohlcv("KRW-BTC",interval="day",count=100) # data frame 형태, 시계열 데이터.
#print(df)

# 5. 세세캔들 월봉 조회. open, high, low, close, volume
#pd.options.display.float_format = "{:.1f}".format  #값 범위 넘어가기땜에 표시 포맷 변경
#df = pyupbit.get_ohlcv("KRW-BTC",interval="month",count=100) # data frame 형태, 시계열 데이터.
#print(df)


# excel로 종목 정보 뽑아오기 (변동성 돌파 매매 -- 시가 >= (전일고가 - 전일 저가) * 0.5 이면 매수하여 종가에 매도)
df = pyupbit.get_ohlcv("KRW-XRP")
df.to_excel("xrp.xlsx")
