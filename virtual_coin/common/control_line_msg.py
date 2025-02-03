import requests

#keys
line_target_url = 'https://notify-api.line.me/api/notify'
line_token      = 'Cey7ltkw3fLQ6ordR7Cy5sHdbAFhKxCCA5lVecTcWq0'


# -----------------------------------------------------------------------------
# - Name : send_to_me_msg
# - Desc : 라인 메세지 전송
# - Input
#   1) message : 메세지
# - Output
#   1) response : 발송결과(200:정상)
# -----------------------------------------------------------------------------
def send_to_me_msg(message):
    try:
        headers = {'Authorization': 'Bearer ' + line_token}
        data = {'message': message}

        response = requests.post(line_target_url, headers=headers, data=data)

        return response

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise