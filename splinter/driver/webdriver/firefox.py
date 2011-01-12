from selenium.firefox.webdriver import WebDriver as firefox_driver
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement

class WebDriver(BaseWebDriver):

    def __init__(self):
        self.driver = firefox_driver()
        self.element_class = WebDriverElement
