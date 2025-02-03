import requests
import json

LOCAL_JSON_LOCATION = "C:\BizPlatform\store_data\kakao_code.json"
KAKAO_SEND_MSG_URL  ="https://kapi.kakao.com/v2/api/talk/memo/default/send"

def get_my_tokens():
    with open(r"" + LOCAL_JSON_LOCATION, "r") as fp:
        tokens = json.load(fp)

    if tokens is not None:
#        print(tokens)
#        print(tokens["access_token"])

        return tokens
    else:
        print("token is None~")
        return None

def send_to_me_msg(msg):

    tokens = get_my_tokens()

    if tokens is not None:
        headers = {
            "Authorization": "Bearer " + tokens["access_token"]
        }

        data = {
            "template_object": json.dumps({
                "object_type": "text",
                "text": msg,
                "link": {
                    "web_url": "www.naver.com"
                }
            })
        }

        response = requests.post(KAKAO_SEND_MSG_URL, headers=headers, data=data)
        print("kakao send code: " + str(response.status_code))
        return response.status_code