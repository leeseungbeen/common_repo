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
class SavePlaceTest(base_test.BaseTest):

        def setUp(self) -> None:
            self.setAppium_server_url()

            # capbilities 초기화
            self.capabilities["platformName"] = "Android"
            self.capabilities["automationName"] = "uiautomator2"
            self.capabilities["deviceName"] = "Android"

            # get driver
            self.driver = webdriver.Remote(self.appium_server_url,
                                           options=UiAutomator2Options().load_capabilities(self.capabilities))

        def tearDown(self) -> None:

            pass

        def save_place(self):
            product_view = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value= '장소담기')
            product_title_view = product_view.find_element(by=AppiumBy.XPATH,
                                                           value='//android.widget.ImageView[@index="3"]')
            content_desc = product_title_view.get_attribute("contentDescription")
            text_title = content_desc.splitlines()[0]

            el3 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="장소 담으러 가기")
            el3.click()

            self.driver.implicitly_wait(time_to_wait = 20)

            time.sleep(2)

            el4 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                      value="new UiSelector().resourceId(\"nx_input_clear\")")
            el4.click()

            time.sleep(2)

            el6 = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            el6.click()

            el6.send_keys(text_title)

            time.sleep(2)

            # 검색버튼 클릭
            el7 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"검색\")")
            el7.click()

            self.driver.implicitly_wait(time_to_wait=20)


            # 검색 장소 진입 -- 플레이스의 경우 처리 고려. 맛집 아닌경우..
            place_text_els = self.driver.find_elements(by=AppiumBy.XPATH,
                                                     value='//android.widget.TextView[@text="플레이스"]')
            if len(place_text_els) > 0:
                place_text_el = self.driver.find_element(by=AppiumBy.XPATH,
                                                         value='//android.widget.TextView[@text="플레이스"]')

                parent_place_title = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                              value='new UiSelector().className("android.view.View").instance(40)')
                place_title = parent_place_title.find_element(by=AppiumBy.XPATH,
                                                              value='//android.widget.Button[@index="0"]')
                place_title.click()
                print('use place')
            else:
                s_el1 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                 value="new UiSelector().resourceId(\"_title\")")

                s_title_btn = s_el1.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@index="0"]')
                s_title_btn.click()
                print('use title')


            self.driver.implicitly_wait(time_to_wait=20)

            # 저장
            el_favorite = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ToggleButton[@text="저장"]')
            el_favorite.click()
            time.sleep(2)

            #플레이스 저장
            el_place_add_base = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                    value="new UiSelector().className(\"android.view.View\").instance(8)")
            el_place_add = el_place_add_base.find_element(by=AppiumBy.XPATH, value='//android.widget.CheckBox[@index="0"]')
            el_place_add.click()
            time.sleep(2)

            el_save = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"저장\")")
            el_save.click()

            self.driver.implicitly_wait(time_to_wait=10)

            #place 결과 클릭
            ico_place = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"플레이스\")")
            ico_place.click()

            time.sleep(5)

            #공유
            share = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                      value="new UiSelector().resourceId(\"com.nhn.android.search.InAppBrowser:id/toolbarIconView\").instance(5)")
            share.click()

            time.sleep(2)

            share_funny = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"퍼니지\")")
            share_funny.click()

            time.sleep(1)

            el7 = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@index="0"]')
            el7.click()



        def test_save_place(self) -> None:

            #loop 횟수
            for i in range(0,5):
                self.save_place()
                print(str(i))
                time.sleep(5)


# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()