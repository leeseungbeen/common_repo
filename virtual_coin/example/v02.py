import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from common import control_kakao as ctrl_kakao
from common import control_upbit as ctrl_upbit
from common import control_line_msg as ctrl_line_msg
import datetime
import time

# upbit instance 생성
upbit_inst    = ctrl_upbit.create_upbit_instance()

#ctrl_upbit.available_buy_with_rsi()

today_target_price = ctrl_upbit.calc_target_price()
user_balance = ctrl_upbit.get_my_balance(upbit_inst)
user_quantity = ctrl_upbit.get_my_quantity(upbit_inst)

#ctrl_kakao.send_to_me_msg("[목표가갱신] " + str(today_target_price))
#ctrl_kakao.send_to_me_msg("[매도신호] 오전9시전!")
ctrl_line_msg.send_to_me_msg("[매도신호] 오전9시전!")