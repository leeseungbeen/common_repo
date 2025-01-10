from base_code import base_test
from appium.webdriver.common.appiumby import AppiumBy

import time
import unittest

# TestCase 작성
# --[start]CustomTest Class
class CustomTest(base_test.BaseTest):

        def setCapAppPackage(self):
            self.capabilities["appPackage"] = "kr.co.funeasy.app"


        def setCapAppActivity(self):
            self.capabilities["appActivity"] = "kr.co.funeasy.app.MainActivity"

        def login_funeasy_app(self):
            # email 로그인 화면 클릭 이동
            time.sleep(5)
            el1 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="이메일 로그인")
            el1.click()
            time.sleep(2)

            # email id 입력
            el2 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
            el2.click()
            el2.send_keys("zeroandi@naver.com")

            # email 비번 입력
            el3 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
            el3.click()
            el3.send_keys("password1!")

            # 로그인하기 버튼 클릭
            el4 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="로그인하기")
            el4.click()
            time.sleep(2)

            # 초기 둘러보기팝업 제거
            el5 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="나중에 할게요")
            el5.click()


        def test_funeasy_macro(self) -> None:
            self.login_funeasy_app()
            time.sleep(10000)

# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()