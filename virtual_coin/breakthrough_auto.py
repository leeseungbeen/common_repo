import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#from common import control_kakao as ctrl_kakao
from common import control_line_msg as ctrl_line_msg
from common import control_upbit as ctrl_upbit
import datetime
import time


# upbit instance 생성
upbit_inst    = ctrl_upbit.create_upbit_instance()

# user balance 및 보유 fiat 수량 저장.
user_first_balance = user_balance = ctrl_upbit.get_my_balance(upbit_inst)
user_quantity  = ctrl_upbit.get_my_quantity(upbit_inst)

# 오늘의 목표가 설정
today_target_price = ctrl_upbit.calc_target_price()

# 변수 설정
OP_MODE_WATING  = 0
OP_MODE_SELLING = 1
OP_MODE_BUYING  = 2
OP_MODE_REFRESH = 3

op_mode =  OP_MODE_WATING # 명령 처리 가능 상태

current_tick  = -1
refresh_tick  = 0
five_min_tick = 0

cur_fiat = ctrl_upbit.get_current_setting_fiat()

# test 매수
#return_val = ctrl_upbit.buy_fiat(upbit_inst)
#if return_val >= 0 :
#    user_balance = ctrl_upbit.get_my_balance(upbit_inst)
#    user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)
#    print("balance: " + str(user_balance) + ',quantity: ' + str(user_quantity))

# test 매도
#return_val = ctrl_upbit.sell_fiat(upbit_inst)
#if return_val >= 0 :
#    user_balance = ctrl_upbit.get_my_balance(upbit_inst)
#    user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)
#    print("balance: " + str(user_balance) + ',quantity: ' + str(user_quantity))


# 반복하면서 정보 갱신
while True:

    # 시간 갱신
    now = datetime.datetime.now()

    # 현재 종목 가격 갱신
    cur_fiat_price = ctrl_upbit.get_cur_fiat_price()

    # 매도 시도 오전 9시 10초전, 명령 처리상태, 종목 보유상태
    if op_mode == OP_MODE_WATING and now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
        op_mode = OP_MODE_SELLING
        user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)

        if  user_quantity > 0:
#            return_val = ctrl_upbit.sell_fiat(upbit_inst)
#            time.sleep(10)
#            curtick += 10
            return_val = 0 # 임시
            ctrl_line_msg.send_to_me_msg("[매도신호] 오전9시전!")

            if return_val >= 0:
#                op_mode = OP_MODE_WATING
                user_balance  = ctrl_upbit.get_my_balance(upbit_inst)
                user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)

    # 9시 20초에서 30초 사이 목표가 갱신
    elif op_mode != OP_MODE_REFRESH and now.hour == 9 and now.minute == 0 and 20 <= now.second <= 30 :
        today_target_price = ctrl_upbit.calc_target_price()
        op_mode = OP_MODE_REFRESH
        user_balance = ctrl_upbit.get_my_balance(upbit_inst)
        user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)

        ctrl_line_msg.send_to_me_msg("[목표가갱신] " + str(today_target_price))

    elif op_mode != OP_MODE_WATING and now.hour == 9 and now.minute == 0 and 40 <= now.second <= 45 :
        op_mode = OP_MODE_WATING

    # 종목가격이 있고, op 모드가 대기상태이고, 종목가격이 목표가 이상 올라갔을 때 매수처리
    elif op_mode == OP_MODE_WATING and cur_fiat_price is not None and cur_fiat_price >= today_target_price:
        op_mode = OP_MODE_BUYING
        user_balance = ctrl_upbit.get_my_balance(upbit_inst)
        user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)

        #if user_quantity <= 0 and user_balance > 0 : # 수량이 없고 보유 금액 있을때 매수
#            return_val = ctrl_upbit.buy_fiat(upbit_inst)
#            time.sleep(10)
#            curtick += 10

        if True:  # 수량이 없고 보유 금액 있을때 매수
            is_available_rsi = ctrl_upbit.available_buy_with_rsi()
            return_val = 0  # 임시
            buy_msg    = "[매수신호] 돌파매매신호!"

            if is_available_rsi is True :
                buy_msg += " RSI!!"

            ctrl_line_msg.send_to_me_msg(buy_msg)

            if return_val >= 0:
                op_mode = OP_MODE_WATING
                user_balance = ctrl_upbit.get_my_balance(upbit_inst)
                user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)
        else:
            op_mode = OP_MODE_WATING
        
        
    # 60분마다 유저 보유 BALANCE, 종목 보유갯수 갱신
#    if refresh_tick >= 6:
#        user_balance = ctrl_upbit.get_my_balance(upbit_inst)
#        user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)
#        refresh_tick = 0

    # 5분마다 체크 (5분봉)
    if five_min_tick >= (60 * 5) or five_min_tick <= 0:
        five_min_tick = 0

        print(f"현재시간:{now} 종목:{cur_fiat} 목표가:{today_target_price} 현재가:{cur_fiat_price}  시작금액:{user_first_balance} 현재금액:{user_balance} 보유수량:{user_quantity}")

        #매도 최소조건 체크
        sell_return_val = ctrl_upbit.check_available_sell_min(upbit_inst)

        if sell_return_val["is_available"] is True:
            ctrl_line_msg.send_to_me_msg("[매도신호]최소가능 " + str(sell_return_val["cur_fiat_price"]))

        # 유저 보유 BALANCE, 종목 보유갯수 갱신
        user_balance  = ctrl_upbit.get_my_balance(upbit_inst)
        user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)


    # 10분마다 상태 출력
#    if current_tick >= (60 * 10) or current_tick < 0:
#        print(f"현재시간:{now} 종목:{cur_fiat} 목표가:{today_target_price} 현재가:{cur_fiat_price}  시작금액:{user_first_balance} 현재금액:{user_balance} 보유수량:{user_quantity}")
#        current_tick = 0
#        is_occur = False
#        refresh_tick = refresh_tick + 1



#    current_tick  = current_tick + 1
    five_min_tick = five_min_tick + 1

    # 1초에 한 번 돌게..
    time.sleep(1)

#print("balance: " + str(user_balance) + ',quantity: ' + str(user_quantity))