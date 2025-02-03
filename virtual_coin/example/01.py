# REST API
import requests

url = "https://api.upbit.com/v1/market/all"
params = {
    "isDetails":"false"
}
response = requests.get(url, params)
data = response.json() # JSON
#print(len(data))
#print(data)

krw_tickers = []
for coin in data:
    ticker = coin['market'] # coin is dict

    if ticker.startswith("KRW"):    # "KRW-BTC"
        krw_tickers.append(ticker)

print(krw_tickers)
print(len(krw_tickers))
