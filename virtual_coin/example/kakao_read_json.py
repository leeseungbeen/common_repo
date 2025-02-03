# step 1. json 정보 서버에서 읽어와 저장
import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = 'c444439a0e9b3cf55ade58e35b68cf2e'
redirect_uri = 'https://example.com/oauth'
authorize_code = '1KfHleuiSwWjRykIEuX7qnHtuM4Uv3Q5Q1rSZOs4VuTeCyRr46IaFwAAAAQKPCRZAAABlLFI7hgWphHJzwXJqw'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
#1.
with open(r"C:\BizPlatform\store_data\kakao_code.json","w") as fp:
    json.dump(tokens, fp)