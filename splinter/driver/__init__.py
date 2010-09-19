from selenium.firefox.webdriver import WebDriver as firefox

class WebDriver(object):
    
    def __init__(self):
        self.driver = firefox()
    
    def visit(self, url):
        self.driver.get(url)
    
    @property
    def title(self):
        return self.driver.get_title()
        
    def quit(self):
        self.driver.quit()
