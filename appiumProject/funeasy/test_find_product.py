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
class ProductFindTest(base_test.BaseTest):

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

        def find_product(self, menu_name):
            # 1.상품 찾으러 가기 버튼 클릭.
            to_go_find_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="상품 찾으러 가기")
            to_go_find_btn.click()

            # 2.다시 퍼니지 앱으로 돌아오기.
            time.sleep(2)
            self.driver.execute_script('mobile: pressKey', {"keycode": 187})
            time.sleep(2)
            cur_app = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="퍼니지 ")
            cur_app.click()

            time.sleep(2)
            # 3.크롬브라우저로 관련 내용 검색
            product_view = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value= menu_name)
            product_title_view = product_view.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@index="3"]')
            content_desc  = product_title_view.get_attribute("contentDescription")
            lines = content_desc.splitlines()

            print(lines[0])
            time.sleep(10)
            try:
                self.selenium_driver.get("https://shopping.naver.com/search/all?query=" + lines[0])
                first_product_element = self.selenium_driver.find_element(by=AppiumBy.XPATH,value='//*[@id="content"]/div[1]/div[2]/div/div[1]')
                first_product_icon_element = first_product_element.find_element(by=AppiumBy.XPATH,value='//*[@id="content"]/div[1]/div[2]/div/div[1]/div/div[1]/div/a')
                first_product_icon_element.click()

                self.selenium_driver.implicitly_wait(time_to_wait=10)

                print("before-" + self.selenium_driver.current_url)
                self.selenium_driver.switch_to.window(self.selenium_driver.window_handles[-1])
                print("after-" + self.selenium_driver.current_url)

                base_text_pos  = self.selenium_driver.current_url.find('/products/')
                base_text_pos2 = self.selenium_driver.current_url.find('?')

                if base_text_pos > -1 and base_text_pos2 > -1 :
                    product_num_text = self.selenium_driver.current_url[(base_text_pos+10): base_text_pos2]
                    print("p_num-" + str(product_num_text))

                    # 4.구매 추가 정보에서 상품번호 얻어서 정답입력.
                    result_edit_el = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                    result_edit_el.click()
                    result_edit_el.clear()
                    result_edit_el.send_keys(str(product_num_text))
                    result_go_btn_el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="입력완료")
                    result_go_btn_el.click()

            finally:
                pass
                # driver 정리
            time.sleep(5)
            # 5.화면 종료 후 미션 계속하기 팝업 노출
            complete_pop_el = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.ImageView")
            content_desc = complete_pop_el.get_attribute("contentDescription")

            last_cnt_base_loc = content_desc.rfind('/')
            else_cnt = content_desc[(last_cnt_base_loc + 1):]
            print('elsecnt:' + str(else_cnt))


            #content_desc.rfind('')

            #tmp_base_one     = content_desc.rfind('\n')
            #tmp_content_desc = content_desc[0:(tmp_base_one-1)]
            #print(str(tmp_content_desc))
            #tmp_base_two     = tmp_content_desc.rfind('\n')
            #tmp_content_desc = tmp_content_desc[(tmp_base_two+1):]
            #print(str(tmp_content_desc))


        def test_find_product(self) -> None:

            #"상품찾기 A"

            for i in range(0,10):
                print(str(i))
                self.find_product("상품찾기 B")
                time.sleep(1)

# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()