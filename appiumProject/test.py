""" unit test 사용, appium 사용 모듈 임포트"""
import unittest, time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# appium 사용하여 전달 될 매개변수 정보
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.android.settings',
    appActivity='.Settings'
)

# 로컬에 러닝중인 appium server 주소
appium_server_url = 'http://localhost:4723'

# TestCase 작성
# --[start]CustomTest Class
class CustomTest(unittest.TestCase):

    # 단순 실행여부 판별
    # def test_runs(self):

    # Fixture Function 테스트 전 수행. appium 드라이버 얻어냄.
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    # Fixture Function 테스트 후 수행.  appium 드라이버 제거.
    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    # test_ 들어가면 기본적으로 테스트 대상 메소드가 됨.
    def test_find_settings(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="연결"]')
        el.click()
        time.sleep(2)
# --[end]CustomTest Class

# unittest 실행.(실행 대상 파일이 main인 경우 유닛테스트 수행시작)
if __name__ == '__main__':
    unittest.main()