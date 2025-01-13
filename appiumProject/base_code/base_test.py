""" unit test 사용, appium 사용 모듈 임포트"""
import unittest, time
from appium import webdriver
from appium.options.android import UiAutomator2Options


# capabilities 초기화

appium_server_url = 'http://localhost:4723'

# TestCase 작성
# --[start]CustomTest Class
class BaseTest(unittest.TestCase):

    capabilities = {}

    # 단순 실행여부 판별
    # def test_runs(self):

    # custom hook point 함수
    def setAppium_server_url(self):
            self.appium_server_url = 'http://localhost:4723'

    def setCapAppPackage(self):
        if self.capabilities:
            self.capabilities["appPackage"] = "com.android.settings"

    def setCapAppActivity(self):
        if self.capabilities:
            self.capabilities["appActivity"] =  ".Settings"


    """
     Fixture Function 테스트 전 수행.
     appium 드라이버 얻어냄.
     capabilities 설정
    """
    def setUp(self) -> None:

        self.setAppium_server_url()

        # capbilities 초기화
        self.capabilities["platformName"] = "Android"
        self.capabilities["automationName"] = "uiautomator2"
        self.capabilities["deviceName"] = "Android"
        self.capabilities["ensureWebviewsHavePages"] = True
        self.capabilities["nativeWebScreenshot"] = True
        self.capabilities["newCommandTimeout"] = 3600
        self.capabilities["connectHardwareKeyboard"] = True
        self.setCapAppPackage()
        self.setCapAppActivity()

        # get driver
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(self.capabilities))

       # selenium_options = selenium_webdriver.ChromeOptions()
       # self.selenium_driver  = selenium_webdriver.Chrome(options=selenium_options)

    # Fixture Function 테스트 후 수행.  appium 드라이버 제거.
    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        if self.selenium_driver:
            self.selenium_driver.quit()

# --[end]CustomTest Class
