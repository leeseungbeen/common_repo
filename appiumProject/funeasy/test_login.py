import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from base_code import base_test
from appium.webdriver.common.appiumby import AppiumBy

import time
import unittest

# TestCase 작성
# --[start]CustomTest Class
class LoginTest(base_test.BaseTest):

        def setCapAppPackage(self):
            self.capabilities["appPackage"] = "kr.co.funeasy.app"

        def setCapAppActivity(self):
            self.capabilities["appActivity"] = "kr.co.funeasy.app.MainActivity"

        def tearDown(self) -> None:
            pass

        def login_funeasy_app(self, email_addr, email_pw):
            # email 로그인 화면 클릭 이동
            time.sleep(5)
            el1 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="이메일 로그인")
            el1.click()
            time.sleep(2)

            # email id 입력
            el2 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
            el2.click()
            el2.send_keys(email_addr)

            # email 비번 입력
            el3 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
            el3.click()
            el3.send_keys(email_pw)

            # 로그인하기 버튼 클릭
            el4 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="로그인하기")
            el4.click()
            time.sleep(2)

            # 초기 둘러보기팝업 제거
            try:
                el5 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="나중에 할게요")

                if el5:
                    el5.click()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            #공지 제거
            try:

                dismiss_dialog = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Dismiss")
                noti_ok = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="확인")
                noti_ok.click()

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


        def test_login(self) -> None:

            tmp_cur_idx = 0
            tmp_login_info_arr = [{'email_addr':'zeroandi@naver.com', 'email_pw':"password1!"}]

            self.login_funeasy_app(tmp_login_info_arr[tmp_cur_idx]['email_addr'], tmp_login_info_arr[tmp_cur_idx]['email_pw'])

# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()