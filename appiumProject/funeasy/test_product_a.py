import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from base_code import base_test
from selenium import webdriver as selenium_webdriver
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import unittest

# TestCase 작성
# --[start]CustomTest Class
class ProductATest(base_test.BaseTest):

        def setUp(self) -> None:
            self.setAppium_server_url()

            # capbilities 초기화
            self.capabilities["platformName"] = "Android"
            self.capabilities["automationName"] = "uiautomator2"
            self.capabilities["deviceName"] = "Android"

            # get driver
            self.driver = webdriver.Remote(self.appium_server_url,
                                           options=UiAutomator2Options().load_capabilities(self.capabilities))
            selenium_options = selenium_webdriver.ChromeOptions()
            self.selenium_driver  = selenium_webdriver.Chrome(options=selenium_options)

        def tearDown(self) -> None:

           #if self.selenium_driver:
            #    self.selenium_driver.quit()

            pass

        def find_product(self):
            # 1.상품 찾으러 가기 버튼 클릭.
            to_go_find_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="상품 찾으러 가기")
            to_go_find_btn.click()

            # 2.다시 퍼니지 앱으로 돌아오기.
            time.sleep(2)
            self.driver.execute_script('mobile: pressKey', {"keycode": 187})
            time.sleep(2)
            cur_app = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="퍼니지 ")
            cur_app.click()

            # 3.크롬브라우저로 관련 내용 검색
            product_view = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="상품찾기 B")
            product_title_view = product_view.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@index="3"]')
            content_desc  = product_title_view.get_attribute("contentDescription")
            lines = content_desc.splitlines()

            print(lines[0])

            try:
                self.selenium_driver.get("https://www.naver.com")
                self.naver_search_box = self.selenium_driver.find_element(By.NAME, "query")
                self.naver_search_box.send_keys(lines[0])
                self.naver_search_box.send_keys(Keys.RETURN)
            finally:
                pass
                # driver 정리

            # 4.구매 추가 정보에서 상품번호 얻어서 정답입력.

            # email 로그인 화면 클릭 이동
            time.sleep(5)




        def test_find_product(self) -> None:
            self.find_product()

# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()