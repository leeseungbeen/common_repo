from base_code import base_test
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

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

            if el5:
                el5.click()

            # 공지 팝업 제거
            popNoti = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="[공지] 신규 랜덤미션 오픈🎉")

            if popNoti:
                noti_ok = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="확인")
                noti_ok.click()

        def move_to_mission_page(self):
            to_go_mission_el = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                      value="new UiSelector().description(\"쉽고 재미있는 미션\n무료 미션 시작하기!\")")
            if to_go_mission_el:
                to_go_mission_el.click()

            time.sleep(2)
            quiz_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="퀴즈")
            if quiz_btn:
                quiz_btn.click()


        def test_funeasy_macro(self) -> None:
            self.login_funeasy_app()
            self.move_to_mission_page()

            if self.selenium_driver:
                self.selenium_driver.get("https://www.google.com")
                search_box = self.selenium_driver.find_element(By.NAME, "q")
                search_box.send_keys("Appium and Selenium integration")
                search_box.submit()

            time.sleep(10000)

# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()