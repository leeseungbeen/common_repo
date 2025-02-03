# step 1. json 정보 서버에서 읽어와 저장
#import requests

#url = 'https://kauth.kakao.com/oauth/token'
#rest_api_key = 'c444439a0e9b3cf55ade58e35b68cf2e'
#redirect_uri = 'https://example.com/oauth'
#authorize_code = 'XyF7hBn4sl5WzQdxOH0r0qYE-ecrKOFf8ucPpd98GpuXOUYsLNC_DQAAAAQKKwzTAAABlKmAXqTSDh85zpcCzQ'

#data = {
#    'grant_type':'authorization_code',
#    'client_id':rest_api_key,
#    'redirect_uri':redirect_uri,
#    'code': authorize_code,
#    }

#response = requests.post(url, data=data)
#tokens = response.json()
#print(tokens)

# json 저장
#import json
#1.
#with open(r"C:\BizPlatform\store_data\kakao_code.json","w") as fp:
#    json.dump(tokens, fp)

# step 2. json 정보 읽어오기 (위의 코드 주석처리)
import requests
import json
#1.
with open(r"C:\BizPlatform\store_data\kakao_code.json","r") as fp:
    tokens = json.load(fp)
print(tokens)
print(tokens["access_token"])

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

# kapi.kakao.com/v2/api/talk/memo/default/send

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}

data={
    "template_object": json.dumps({
        "object_type":"text",
        "text":"lee seung been!",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    })
}

response = requests.post(url, headers=headers, data=data)
print(response.content)
